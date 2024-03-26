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
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
import time
from typing import Dict, Optional, Set

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


def log_call(fcn):
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


class DataStoreMgr:
    """Manage the local data-store acquisition/updates for all workflows.

    Args:
        workflows_mgr:
            Service that scans for workflows.
        log:
            Application logger.
        max_threads:
            Max number of threads to use for subscriptions.

            Note, this determines the maximum number of active workflows that
            can be updated.

            This should be overridden for real use in the UIS app. The
            default is here for test purposes.

    """

    INIT_DATA_WAIT_TIME = 5.  # seconds
    INIT_DATA_RETRY_DELAY = 0.5  # seconds
    RECONCILE_TIMEOUT = 5.  # seconds
    PENDING_DELTA_CHECK_INTERVAL = 0.5

    def __init__(self, workflows_mgr, log, max_threads=10):
        self.workflows_mgr = workflows_mgr
        self.log = log
        self.data = {}
        self.w_subs: Dict[str, WorkflowSubscriber] = {}
        self.topics = {ALL_DELTAS.encode('utf-8'), b'shutdown'}
        self.loop = None
        self.executor = ThreadPoolExecutor(max_threads)
        self.delta_queues = {}

    @log_call
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

    @log_call
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

    @log_call
    async def connect_workflow(self, w_id, contact_data):
        """Initiate workflow subscriptions.

        Call this when a workflow has started.

        Subscriptions and sync management is instantiated and run in
        a separate thread for each workflow. This is to avoid the sync loop
        blocking the main loop.

        """
        if self.loop is None:
            self.loop = asyncio.get_running_loop()

        # don't sync if subscription exists
        if w_id in self.w_subs:
            return

        self.delta_queues[w_id] = {}

        # Might be options other than threads to achieve
        # non-blocking subscriptions, but this works.
        self.executor.submit(
            self._start_subscription,
            w_id,
            contact_data['name'],
            contact_data[CFF.HOST],
            contact_data[CFF.PUBLISH_PORT]
        )
        successful_updates = await self._entire_workflow_update(ids=[w_id])

        if w_id not in successful_updates:
            # something went wrong, undo any changes to allow for subsequent
            # connection attempts
            self.log.info(f'failed to connect to {w_id}')
            self.disconnect_workflow(w_id)
            return False
        else:
            # don't update the contact data until we have successfully updated
            self._update_contact(w_id, contact_data)

    @log_call
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
        if w_id in self.w_subs:
            self.w_subs[w_id].stop()
            del self.w_subs[w_id]

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

    @log_call
    def _purge_workflow(self, w_id):
        """Purge the manager of a workflow's subscription and data."""
        # Ensure no old/new subscriptions exist on purge,
        # this shouldn't happen if disconnect is run before unregister.
        self.disconnect_workflow(w_id, update_contact=False)
        if w_id in self.data:
            del self.data[w_id]
        if w_id in self.delta_queues:
            del self.delta_queues[w_id]

    def _start_subscription(self, w_id, reg, host, port):
        """Instantiate and run subscriber data-store sync.

        Args:
            w_id (str): Workflow external ID.
            reg (str): Registered workflow name.
            host (str): Hostname of target workflow.
            port (int): Port of target workflow.

        """
        self.w_subs[w_id] = WorkflowSubscriber(
            reg,
            host=host,
            port=port,
            context=self.workflows_mgr.context,
            topics=self.topics
        )
        self.w_subs[w_id].loop.run_until_complete(
            self.w_subs[w_id].subscribe(
                process_delta_msg,
                func=self._update_workflow_data,
                w_id=w_id))

    def _update_workflow_data(self, topic, delta, w_id):
        """Manage and apply incoming data-store deltas.

        Args:
            topic (str): topic of published data.
            delta (object): Published protobuf message data container.
            w_id (str): Workflow external ID.

        """
        # wait until data-store is populated for this workflow
        if w_id not in self.data:
            loop_cnt = 0
            while loop_cnt < self.INIT_DATA_WAIT_TIME:
                if w_id in self.data:
                    break
                time.sleep(self.INIT_DATA_RETRY_DELAY)
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
                future = asyncio.run_coroutine_threadsafe(
                    workflow_request(
                        self.workflows_mgr.workflows[w_id]['req_client'],
                        'pb_data_elements',
                        args={'element_type': topic}
                    ),
                    self.loop
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
        self, ids: Optional[list] = None
    ) -> Set[str]:
        """Update entire local data-store of workflow(s).

        Args:
            ids: List of workflow external IDs.

        """
        if ids is None:
            ids = []

        # Request new data
        req_method = 'pb_entire_workflow'

        requests = {
            w_id: workflow_request(
                client=info['req_client'], command=req_method, log=self.log
            )
            for w_id, info in self.workflows_mgr.workflows.items()
            if info.get('req_client')  # skip stopped workflows
            and (not ids or w_id in ids)
        }
        results = await asyncio.gather(
            *requests.values(), return_exceptions=True
        )
        successes: Set[str] = set()
        for w_id, result in zip(requests, results):
            if isinstance(result, Exception):
                if not isinstance(result, WorkflowStopped):
                    self.log.error(
                        'Failed to update entire local data-store '
                        f'of a workflow: {result}'
                    )
                continue
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
            successes.add(w_id)
        return successes

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
