# Copyright (C) NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Manage a local data-store replica of all workflow service data-stores.

A local data-store is created and synced for all workflows established by
the workflow service manager.

The workflows publish the updated fields of the updated data elements (deltas),
and these elements are grouped by type/topic. Once subscribed to, the publisher
queues these messages until the are received, if the delta creation time is
newer than that of the last update then it is applied (updates merged, pruned
deleted) then a checksum is generated from the time stamped IDs and compared to
the published one.

Reconciliation on failed verification is done by requesting all elements of a
topic, and replacing the respective data-store elements with this.

Subscriptions are currently run in a different thread (via ThreadPoolExecutor).

"""

import asyncio
from copy import deepcopy
from functools import wraps
from pathlib import Path
import time
from typing import Dict, NamedTuple

from cylc.flow.exceptions import WorkflowStopped
from cylc.flow.id import Tokens
from cylc.flow.network.server import PB_METHOD_MAP
from cylc.flow.network.subscriber import WorkflowSubscriber, process_delta_msg
from cylc.flow.data_store_mgr import (
    EDGES, DATA_TEMPLATE, ALL_DELTAS, DELTAS_MAP, WORKFLOW,
    apply_delta, generate_checksum, create_delta_store
)
from cylc.flow.workflow_files import (
    ContactFileFields as CFF,
    WorkflowFiles,
    get_workflow_srv_dir,
)
from cylc.flow.workflow_status import WorkflowStatus

from .utils import fmt_call
from .workflows_mgr import workflow_request


def _log_call(fcn):
    """Decorator for data store methods we want to log."""
    fcn_name = f'[data-store] {fcn.__name__}'

    def _inner(*args, **kwargs):  # works for serial & async calls
        nonlocal fcn
        self = args[0]
        # log this method call
        self.log.info(fmt_call(fcn_name, args[1:], kwargs))
        # then do it
        return fcn(*args, **kwargs)

    return _inner


def _call_to_tuple(fcn):
    """Turns function calls into an (args, kwargs) tuple.

    Examples:
        >>> _call_to_tuple(list)(1, 2, a=3, b=4)
        [(1, 2), {'a': 3, 'b': 4}]

    """
    @wraps(fcn)
    def _inner(*args, **kwargs):
        nonlocal fcn
        return fcn((args, kwargs))

    return _inner


class ActiveSubscription(NamedTuple):
    """Represents an active subscription.

    Args:
        subscriber: The subscriber client object.
        task: The asyncio task running the client.

    """
    subscriber: WorkflowSubscriber
    task: asyncio.Task


class DataStoreMgr:
    """Manage the local data-store acquisition/updates for all workflows.

    Args:
        workflows_mgr:
            Service that scans for workflows.
        log:
            Application logger.

    """

    INIT_DATA_WAIT_TIME = 5.  # seconds
    INIT_DATA_RETRY_DELAY = 0.5  # seconds
    RECONCILE_TIMEOUT = 5.  # seconds
    PENDING_DELTA_CHECK_INTERVAL = 0.5

    def __init__(self, workflows_mgr, log):
        self.workflows_mgr = workflows_mgr
        self.log = log
        self.data = {}
        self.active_subscriptions: Dict[str, ActiveSubscription] = {}
        self.topics = {ALL_DELTAS.encode('utf-8'), b'shutdown'}
        self.delta_queues = {}
        self.message_queue = asyncio.Queue()

    def startup(self):
        """Start the data store manager.

        Note: Call this after the asyncio event loop has been opened.
        """
        self.message_processor_task = asyncio.create_task(
            self._process_message_queues()
        )

    def shutdown(self):
        """Stop the data store manager.

        This will stop any active subscribers.

        Note: It will not wait for pending messages to be processed.
        """
        for w_id in self.active_subscriptions:
            self._stop_subscription(w_id)
        self.message_processor_task.cancel()

    @_log_call
    async def register_workflow(self, w_id: str, is_active: bool) -> None:
        """Register a new workflow with the data store.

        Call this when a new workflow is discovered on the file system
        (e.g. installed).
        """
        self.delta_queues[w_id] = {}

        # create new entry in the data store
        data = deepcopy(DATA_TEMPLATE)
        self.data[w_id] = data

        # create new entry in the delta store
        self._update_contact(
            w_id,
            status=WorkflowStatus.STOPPED.value,
            status_msg=self._get_status_msg(w_id, is_active),
        )

    @_log_call
    async def unregister_workflow(self, w_id):
        """Remove a workflow from the data store entirely.

        Call this when a workflow is deleted.
        """
        if w_id in self.data:
            self._update_contact(w_id, pruned=True)
        while any(
            not delta_queue.empty()
            for delta_queue in self.delta_queues.get(w_id, {}).values()
        ):
            await asyncio.sleep(self.PENDING_DELTA_CHECK_INTERVAL)
        self._purge_workflow(w_id)

    @_log_call
    async def connect_workflow(self, w_id, contact_data):
        """Initiate workflow subscriptions.

        Call this when a workflow has started.

        Subscriptions and sync management is instantiated and run in
        a separate thread for each workflow. This is to avoid the sync loop
        blocking the main loop.

        """
        # don't sync if subscription exists
        if w_id in self.active_subscriptions:
            return

        self.delta_queues[w_id] = {}

        try:
            # start the subscriber to keep this store updated
            self._start_subscription(
                w_id,
                contact_data['name'],
                contact_data[CFF.HOST],
                contact_data[CFF.PUBLISH_PORT],
            )
            # make a one-off request to provide the initial data
            await self._entire_workflow_update(w_id)
        except WorkflowStopped:
            self.disconnect_workflow(w_id)
        except Exception as exc:
            self.log.error(f'Failed to connect to {w_id}: {exc}')
            self.disconnect_workflow(w_id)
        else:
            # don't update the contact data until we have successfully updated
            self._update_contact(w_id, contact_data)

    @_log_call
    def disconnect_workflow(self, w_id, update_contact=True):
        """Terminate workflow subscriptions.

        Call this when a workflow has stopped.
        """
        disconnect_msg = self._get_status_msg(w_id, False)
        if (
            update_contact
            and w_id in self.data
            and (
                self.data[w_id][WORKFLOW].status != (
                    WorkflowStatus.STOPPED.value
                )
                or self.data[w_id][WORKFLOW].status_msg != disconnect_msg
            )
        ):
            self._update_contact(
                w_id,
                status=WorkflowStatus.STOPPED.value,
                status_msg=disconnect_msg,
            )
        self._stop_subscription(w_id)

    def get_workflows(self):
        """Return all workflows the data store is currently tracking.

        Returns:
            (active, inactive)
                active: Set of active (running, paused, stopping) workflows.
                inactive: Set of (stopped) workflows.
        """
        active = set()
        inactive = set()
        for w_id, workflow in self.data.items():
            status = getattr(workflow.get('workflow'), 'status', 'stopped')
            if status == 'stopped':
                inactive.add(w_id)
            else:
                active.add(w_id)
        return active, inactive

    @_log_call
    def _purge_workflow(self, w_id):
        """Purge the manager of a workflow's subscription and data."""
        # Ensure no old/new subscriptions exist on purge,
        # this shouldn't happen if disconnect is run before unregister.
        self.disconnect_workflow(w_id, update_contact=False)
        if w_id in self.data:
            del self.data[w_id]
        if w_id in self.delta_queues:
            del self.delta_queues[w_id]

    def _start_subscription(
        self,
        w_id: str,
        reg: str,
        host: str,
        port: int,
    ) -> None:
        """Instantiate and run subscriber data-store sync.

        Args:
            w_id: Workflow external ID.
            reg: Registered workflow name.
            host: Hostname of target workflow.
            port: Port of target workflow.

        Raises:
            WorkflowStoppedError

        """
        # create the subscription client
        subscriber = WorkflowSubscriber(
            reg,
            host=host,
            port=port,
            context=self.workflows_mgr.context,
            topics=self.topics,
        )

        # start the subscription task
        subscriber_task = asyncio.create_task(
            subscriber.subscribe(
                process_delta_msg,
                func=_call_to_tuple(self.message_queue.put_nowait),
                w_id=w_id,
            )
        )
        self.active_subscriptions[w_id] = ActiveSubscription(
            subscriber, subscriber_task
        )

    def _stop_subscription(self, w_id: str) -> None:
        """Stop an active subscription.

        Args:
            w_id: Workflow external ID.

        """
        if w_id in self.active_subscriptions:
            self.active_subscriptions[w_id].subscriber.stop()
            del self.active_subscriptions[w_id]

    async def _process_message_queues(self):
        """Wait for new messages, call the update method then they arrive."""
        while True:
            args, kwargs = await self.message_queue.get()
            await self._update_workflow_data(*args, **kwargs)

    async def _update_workflow_data(
        self,
        topic: str,
        delta,
        w_id: str,
    ) -> None:
        """Manage and apply incoming data-store deltas.

        Args:
            topic: topic of published data.
            delta: Published protobuf message data container.
            w_id: Workflow external ID.

        """
        # wait until data-store is populated for this workflow
        if w_id not in self.data:
            loop_cnt = 0
            while loop_cnt < self.INIT_DATA_WAIT_TIME:
                if w_id in self.data:
                    break
                await asyncio.sleep(self.INIT_DATA_RETRY_DELAY)
                loop_cnt += 1
                continue
        if topic == 'shutdown':
            self._delta_store_to_queues(w_id, topic, delta)
            # close connections
            self.disconnect_workflow(w_id)
            return
        self._apply_all_delta(w_id, delta)
        self._delta_store_to_queues(w_id, topic, delta)

    def _clear_data_field(self, w_id, field_name):
        if field_name == WORKFLOW:
            self.data[w_id][field_name].Clear()
        else:
            self.data[w_id][field_name].clear()

    def _apply_all_delta(self, w_id, delta):
        """Apply the AllDeltas delta."""
        for field, sub_delta in delta.ListFields():
            delta_time = getattr(sub_delta, 'time', 0.0)
            # If the workflow has reloaded clear the data before
            # delta application.
            if sub_delta.reloaded:
                self._clear_data_field(w_id, field.name)
                self.data[w_id]['delta_times'][field.name] = 0.0
            # hard to catch errors in a threaded async app, so use try-except.
            try:
                # Apply the delta if newer than the previously applied.
                if delta_time >= self.data[w_id]['delta_times'][field.name]:
                    apply_delta(field.name, sub_delta, self.data[w_id])
                    self.data[w_id]['delta_times'][field.name] = delta_time
                    if not sub_delta.reloaded:
                        self._reconcile_update(field.name, sub_delta, w_id)
            except Exception as exc:
                self.log.exception(exc)

    def _delta_store_to_queues(self, w_id, topic, delta):
        # Queue delta for graphql subscription resolving
        if self.delta_queues[w_id]:
            delta_store = create_delta_store(delta, w_id)
            for delta_queue in self.delta_queues[w_id].values():
                delta_queue.put((w_id, topic, delta_store))

    def _reconcile_update(self, topic, delta, w_id):
        """Reconcile local with workflow data-store.

        Verify data-store is in sync by topic/element-type
        and on failure request entire set of respective data elements.

        Args:
            topic (str): topic of published data.
            delta (object): Published protobuf message data container.
            w_id (str): Workflow external ID.

        """
        if topic == WORKFLOW:
            return
        if topic == EDGES:
            s_att = 'id'
        else:
            s_att = 'stamp'
        local_checksum = generate_checksum(
            [getattr(e, s_att)
             for e in self.data[w_id][topic].values()])
        if local_checksum != delta.checksum:
            self.log.debug(
                f'Out of sync with {topic} of {w_id}... Reconciling.')
            try:
                # use threadsafe as client socket is in main loop thread.
                # NOTE: we don't think the "threadsafe" bit is needed now
                # https://github.com/cylc/cylc-uiserver/pull/574/files#r1557294509
                future = asyncio.run_coroutine_threadsafe(
                    workflow_request(
                        self.workflows_mgr.workflows[w_id]['req_client'],
                        'pb_data_elements',
                        args={'element_type': topic}
                    ),
                )
                new_delta_msg = future.result(self.RECONCILE_TIMEOUT)
                new_delta = DELTAS_MAP[topic]()
                new_delta.ParseFromString(new_delta_msg)
                self._clear_data_field(w_id, topic)
                apply_delta(topic, new_delta, self.data[w_id])
                self.data[w_id]['delta_times'][topic] = new_delta.time
            except asyncio.TimeoutError:
                self.log.debug(
                    f'The reconcile update coroutine {w_id} {topic}'
                    f'took too long, cancelling the subscription/sync.'
                )
                future.cancel()
            except Exception as exc:
                self.log.exception(exc)

    async def _entire_workflow_update(
        self,
        w_id: str,
        req_method: str = 'pb_entire_workflow',
    ) -> None:
        """Call "req_method" on a workflow and put the data in the store.

        Args:
            w_id:
                The workflow ID to fetch data from.
            req_method:
                The protobuf data endpoint to call on the workflow.

        Raises:
            WorkflowStoppedError

        """
        # get the workflow client
        client = self.workflows_mgr.workflows.get(w_id, {}).get(
            'req_client', None
        )
        if not client:
            raise WorkflowStopped(w_id)

        # request data
        result = await workflow_request(
            client=client,
            command=req_method,
            log=self.log,
        )

        # update the store
        pb_data = PB_METHOD_MAP[req_method]()
        pb_data.ParseFromString(result)
        new_data = deepcopy(DATA_TEMPLATE)
        for field, value in pb_data.ListFields():
            if field.name == WORKFLOW:
                new_data[field.name].CopyFrom(value)
                new_data['delta_times'] = {
                    key: value.last_updated
                    for key in DATA_TEMPLATE
                }
                continue
            new_data[field.name] = {n.id: n for n in value}
        self.data[w_id] = new_data

    def _update_contact(
        self,
        w_id,
        contact_data=None,
        status=None,
        status_msg=None,
        pruned=False,
    ):
        """Update the data store with information from the contact file.

        Args:
            w_id: Workflow ID.
            contact_data: Contact file data dictionary.
            status: Workflow status (e.g. "running").
            status_msg: Workflow status message (e.g. "will stop at 2000").
            pruned: ?

        Returns:
            True if the contact data is successfully updated or False if
            the workflow is no longer in the store (e.g. has been removed).

        """
        if w_id not in self.data:
            # workflow has been removed - do nothing
            return False

        delta = DELTAS_MAP[ALL_DELTAS]()
        delta.workflow.time = time.time()
        flow = delta.workflow.updated
        flow.id = w_id
        flow.stamp = f'{w_id}@{delta.workflow.time}'
        if contact_data:
            # update with contact file data
            flow.name = contact_data['name']
            flow.owner = contact_data['owner']
            flow.host = contact_data[CFF.HOST]
            flow.port = int(contact_data[CFF.PORT])
            flow.api_version = int(contact_data[CFF.API])
        else:
            # wipe pre-existing contact-file data
            w_tokens = Tokens(w_id)
            flow.owner = w_tokens['user']
            flow.name = w_tokens['workflow']
            flow.host = ''
            flow.port = 0
            flow.api_version = 0

        if status is not None:
            flow.status = status
        if status_msg is not None:
            flow.status_msg = status_msg
        if pruned:
            flow.pruned = True
            delta.workflow.pruned = w_id

        # Apply to existing workflow data
        if 'delta_times' not in self.data[w_id]:
            self.data[w_id]['delta_times'] = {WORKFLOW: 0.0}
        self._apply_all_delta(w_id, delta)
        # Queue delta for subscription push
        self._delta_store_to_queues(w_id, ALL_DELTAS, delta)

        return True

    def _get_status_msg(self, w_id: str, is_active: bool) -> str:
        """Derive a status message for the workflow.

        Running schedulers provide their own status messages.

        We must derive a status message for stopped workflows.
        """
        if is_active:
            # this will get overridden when we sync with the workflow
            # set a sensible default here incase the sync takes a while
            return 'running'
        w_id = Tokens(w_id)['workflow']
        db_file = Path(get_workflow_srv_dir(w_id), WorkflowFiles.Service.DB)
        if db_file.exists():
            # the workflow has previously run
            return 'stopped'
        else:
            # the workflow has not yet run
            return 'not yet run'
