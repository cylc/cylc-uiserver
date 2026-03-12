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
from typing import Dict, Iterable, List, Optional, Set, cast, TYPE_CHECKING

from cylc.flow.data_store_mgr import (
    FAMILIES, FAMILY_PROXIES, JOBS, TASKS, TASK_PROXIES,
    EDGES, DATA_TEMPLATE, ALL_DELTAS, DELTAS_MAP, WORKFLOW,
    apply_delta, generate_checksum, create_delta_store
)
from cylc.flow.exceptions import WorkflowStopped
from cylc.flow.id import Tokens
from cylc.flow.network.graphql import extract_ast_fields
from cylc.flow.network.server import PB_METHOD_MAP
from cylc.flow.network.subscriber import WorkflowSubscriber, process_delta_msg
from cylc.flow.workflow_files import (
    ContactFileFields as CFF,
    WorkflowFiles,
    get_workflow_srv_dir,
)
from cylc.flow.workflow_status import WorkflowStatus

from .utils import fmt_call
from .workflows_mgr import workflow_request


if TYPE_CHECKING:
    from cylc.flow.data_messages_pb2 import PbWorkflow


SUBSCRIPTION_CATALOGUE = {
    EDGES: {
        'criteria': {
            'edges',
            'nodesEdges',
        },
        'request': 'pb_data_elements',
    },
    FAMILIES: {
        'criteria': {
            'ancestors',
            'childFamilies',
            'family',
            'families',
            'firstParent',
            'parents',
        },
        'request': 'pb_data_elements',
    },
    FAMILY_PROXIES: {
        'criteria': {
            'ancestors',
            'childFamilies',
            'familyProxy',
            'familyProxies',
            'firstParent',
            'nodes',
            'parents',
        },
        'request': 'pb_data_elements',
    },
    JOBS: {
        'criteria': {
            'job',
            'jobs',
        },
        'request': 'pb_data_elements',
    },
    TASKS: {
        'criteria': {
            'childTasks',
            'task',
            'tasks',
        },
        'request': 'pb_data_elements',
    },
    TASK_PROXIES: {
        'criteria': {
            'childTasks',
            'nodes',
            'sourceNode',
            'targetNode',
            'taskProxy',
            'taskProxies',
        },
        'request': 'pb_data_elements',
    },
    WORKFLOW: {
        'criteria': {
            'workflow',
            'workflows',
            'deltas',
        },
        'request': 'pb_data_elements',
    },
    ALL_DELTAS: {
        'criteria': {
            EDGES,
            FAMILIES,
            FAMILY_PROXIES,
            JOBS,
            TASKS,
            TASK_PROXIES,
            WORKFLOW,
        },
        'request': 'pb_entire_workflow',
    },
}
# expiry interval post query
QUERY_SYNC_EXPIRY = 60


def generate_level_topics(level) -> set:
    """Produce the subscription topics from the workflow sync level."""
    selection = set()
    all_criteria = SUBSCRIPTION_CATALOGUE[ALL_DELTAS]['criteria']
    if all_criteria.issubset(level):
        selection.update(level.difference(all_criteria))
        selection.add(ALL_DELTAS)
    else:
        selection = level
    return {item.encode('utf-8') for item in selection}


def log_call(fcn):
    """Decorator for data store methods we want to log."""
    fcn_name = f'[data-store] {fcn.__name__}'

    def _inner(*args, **kwargs):  # works for serial & async calls
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

    INIT_DATA_WAIT_CHECKS = 30  # check attempts
    INIT_DATA_RETRY_DELAY = 0.5  # seconds
    RECONCILE_TIMEOUT = 5.  # seconds
    PENDING_DELTA_CHECK_INTERVAL = 0.5
    SYNC_LEVEL_TIMER_INTERVAL = 30

    def __init__(self, workflows_mgr, log, max_threads=10):
        self.workflows_mgr = workflows_mgr
        self.log = log
        self.data = {}
        self.w_subs: Dict[str, WorkflowSubscriber] = {}
        # graphql subscription level
        self.sync_level_graphql_subs = {
            'minimal': {WORKFLOW, 'shutdown'},
        }
        # workflow graphql subscriptions
        self.workflow_sync_graphql_subs = {}
        # workflow graphql query timers
        self.workflow_query_sync_timers = {}
        # resultant workflow sync level
        self.workflow_sync_level = {}
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

        # setup sync subscriber level sets
        self.workflow_sync_graphql_subs[w_id] = {'minimal'}

        # set query sync timer
        self.workflow_query_sync_timers[w_id] = {
            'expiry': 0.0,
            'level': set(),
        }

        # set workflow sync level
        self.workflow_sync_level[w_id] = self._get_sync_level(w_id)

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

        level = self.workflow_sync_level[w_id]

        # Might be options other than threads to achieve
        # non-blocking subscriptions, but this works.
        self.executor.submit(
            self._start_subscription,
            w_id,
            contact_data['name'],
            contact_data[CFF.HOST],
            contact_data[CFF.PUBLISH_PORT],
            generate_level_topics(level)
        )

        result = await self.workflow_data_update(w_id, level)

        if result:
            # don't update the contact data until we have successfully updated
            self._update_contact(w_id, contact_data)

    @log_call
    async def workflow_data_update(
        self,
        w_id: str,
        level: Set[str],
    ):
        requests = set()
        if ALL_DELTAS in level:
            requests.add(SUBSCRIPTION_CATALOGUE[ALL_DELTAS]["request"])
        else:
            requests.update(
                {
                    SUBSCRIPTION_CATALOGUE[topic]["request"]
                    for topic in level
                    if topic in SUBSCRIPTION_CATALOGUE
                }
            )
        for request in requests:
            successful_updates = await self._workflow_update(
                [w_id],
                request,
                elements=[
                    element
                    for element in level
                    if element in DATA_TEMPLATE
                ]
            )

        if w_id not in successful_updates:
            # something went wrong, undo any changes to allow for subsequent
            # connection attempts
            self.log.info(f'failed to connect to {w_id}')
            self.disconnect_workflow(w_id)
            return False
        return True

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
        if w_id in self.workflow_sync_level_graphql_subs:
            del self.workflow_sync_graphql_subs[w_id]
        if w_id in self.workflow_query_sync_timers:
            del self.workflow_query_sync_timers[w_id]
        if w_id in self.workflow_sync_level:
            del self.workflow_sync_level[w_id]

    def _start_subscription(self, w_id, reg, host, port, topics):
        """Instantiate and run subscriber data-store sync.

        Args:
            w_id (str): Workflow external ID.
            reg (str): Registered workflow name.
            host (str): Hostname of target workflow.
            port (int): Port of target workflow.
            topics set(str): set of topics to subscribe to.

        """
        self.w_subs[w_id] = WorkflowSubscriber(
            reg,
            host=host,
            port=port,
            context=self.workflows_mgr.context,
            topics=topics
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
        # Wait until data-store is populated for this workflow,
        # carry on otherwise, errors will be reconciled with data validation.
        if self.data[w_id][WORKFLOW].last_updated == 0:
            loop_cnt = 0
            while loop_cnt < self.INIT_DATA_WAIT_CHECKS:
                if self.data[w_id][WORKFLOW].last_updated > 0:
                    break
                time.sleep(self.INIT_DATA_RETRY_DELAY)
                loop_cnt += 1
                continue
        if topic == 'shutdown':
            self._delta_store_to_queues(w_id, topic, delta)
            # close connections
            self.disconnect_workflow(w_id)
            return
        elif topic == ALL_DELTAS:
            self._apply_all_delta(w_id, delta)
            self._delta_store_to_queues(w_id, topic, delta)
        else:
            self._apply_delta(w_id, topic, delta)
            # might seem clunky, but as with contact update, making it look
            # like an ALL_DELTA avoids changing the resolver in cylc-flow
            all_deltas = DELTAS_MAP[ALL_DELTAS]()
            getattr(all_deltas, topic).CopyFrom(delta)
            self._delta_store_to_queues(w_id, ALL_DELTAS, all_deltas)

    def _clear_data_field(self, w_id, field_name):
        if field_name == WORKFLOW:
            self.data[w_id][field_name].Clear()
        else:
            self.data[w_id][field_name].clear()

    def _apply_all_delta(self, w_id, delta):
        """Apply the AllDeltas delta."""
        for field, sub_delta in delta.ListFields():
            self._apply_delta(w_id, field.name, sub_delta)

    def _apply_delta(self, w_id, name, delta):
        """Apply delta."""
        delta_times = self.data[w_id]['delta_times']
        delta_time = getattr(delta, 'time', 0.0)
        # If the workflow has reloaded clear the data before
        # delta application.
        if delta.reloaded:
            self._clear_data_field(w_id, name)
            delta_times[name] = 0.0
        # hard to catch errors in a threaded async app, so use try-except.
        try:
            # Apply the delta if newer than the previously applied.
            if delta_time >= delta_times.get(name, 0.0):
                apply_delta(name, delta, self.data[w_id])
                delta_times[name] = delta_time
                if not delta.reloaded:
                    self._reconcile_update(name, delta, w_id)
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
                        'pb_delta_elements',
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

    async def _workflow_update(
        self, ids: List[str], req_method: str, **kwargs
    ) -> Set[str]:
        """Update entire local data-store of workflow(s).

        Args:
            ids: List of workflow external IDs.

        """
        # Request new data
        req_time = time.time()

        requests = {
            w_id: workflow_request(
                client=info['req_client'],
                command=req_method,
                log=self.log,
                args=kwargs
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
                    # If the workflow is still loading this initial dump will
                    # be empty, so use time immediately before request.
                    value.last_updated = value.last_updated or req_time
                    cast('PbWorkflow', new_data[field.name]).CopyFrom(value)
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

    def _get_sync_level(self, w_id) -> set:
        """Return the sync level in the form of a set of catalogue items."""
        level = set()
        if (
            w_id in self.workflow_query_sync_timers
            and self.workflow_query_sync_timers[w_id]['expiry'] > 0
        ):
            level.update(self.workflow_query_sync_timers[w_id]['level'])
        for sub_id in self.workflow_sync_graphql_subs[w_id]:
            level.update(self.sync_level_graphql_subs.get(sub_id, ()))
        return level

    async def _update_subscription_level(self, w_id):
        """Update level of data subscribed to."""
        new_level = self._get_sync_level(w_id)
        if new_level == self.workflow_sync_level[w_id]:
            return
        self.workflow_sync_level[w_id] = new_level
        sub = self.w_subs.get(w_id)
        if sub:
            new_topics = generate_level_topics(new_level)
            stop_topics = sub.topics.difference(new_topics)
            start_topics = new_topics.difference(sub.topics)
            for stop_topic in stop_topics:
                sub.unsubscribe_topic(stop_topic)
            # Doing this after unsubscribe and before subscribe
            # to make sure old topics stop and new data is in place.
            await self.workflow_data_update(w_id, new_level)
            for start_topic in start_topics:
                sub.subscribe_topic(start_topic)

    def graphql_sub_interrogate(self, sub_id, info):
        """Scope data requirements."""
        fields = set()
        extract_ast_fields(info.operation, fields)
        for frag in getattr(info, 'fragments', {}).values():
            extract_ast_fields(frag, fields)
        self.sync_level_graphql_subs[sub_id] = {'shutdown'}
        sync_level_subs = self.sync_level_graphql_subs[sub_id]
        for category in DATA_TEMPLATE:
            if fields.intersection(
                SUBSCRIPTION_CATALOGUE[category]['criteria']
            ):
                sync_level_subs.add(category)

    async def graphql_sub_data_match(self, w_id, sub_id):
        """Match store data level to requested graphql subscription."""
        sync_level_wsubs = self.workflow_sync_graphql_subs[w_id]
        sync_level_wsubs.add(sub_id)

        # set new sync level
        await self._update_subscription_level(w_id)

    async def graphql_sub_discard(self, sub_id):
        """Discard graphql subscription references."""
        if sub_id in self.sync_level_graphql_subs:
            del self.sync_level_graphql_subs[sub_id]
        for w_id in self.workflow_sync_graphql_subs:
            if sub_id not in self.workflow_sync_graphql_subs[w_id]:
                continue
            self.workflow_sync_graphql_subs[w_id].discard(sub_id)
            await self._update_subscription_level(w_id)

    async def set_query_sync_levels(
        self,
        w_ids: Iterable[str],
        level: Optional[Iterable[str]] = None,
        expire_delay: Optional[float] = None,
    ):
        """Set a workflow sync level."""
        if level is None:
            level = set(DATA_TEMPLATE.keys())
        if expire_delay is None:
            expire_delay = QUERY_SYNC_EXPIRY
        expire_time = time.time() + expire_delay
        for w_id in w_ids:
            if self.workflow_sync_level[w_id] == level:
                # Already required level
                continue
            self.workflow_query_sync_timers[w_id]['expiry'] = expire_time
            self.workflow_query_sync_timers[w_id]['level'].update(level)
            await self._update_subscription_level(w_id)

    async def check_query_sync_level_expiries(self):
        """Check for and downgrade expired sub levels."""
        for w_id, items in self.workflow_query_sync_timers.items():
            if items['expiry'] < time.time():
                items['expiry'] = 0.0
                items['level'].clear()
                await self._update_subscription_level(w_id)
