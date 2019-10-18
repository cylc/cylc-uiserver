# -*- coding: utf-8 -*-
# Copyright (C) 2019 NIWA & British Crown (Met Office) & Contributors.
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

"""Create and update the data structure for all workflow services."""

import asyncio
import logging

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from time import sleep

from cylc.flow.network.server import PB_METHOD_MAP
from cylc.flow.network.scan import MSG_TIMEOUT
from cylc.flow.network.subscriber import WorkflowSubscriber, process_delta_msg
from cylc.flow.ws_data_mgr import (
    EDGES, FAMILIES, FAMILY_PROXIES, JOBS, TASKS, TASK_PROXIES, WORKFLOW,
    DELTAS_MAP, apply_delta, generate_checksum
)
from .workflows_mgr import workflow_request

logger = logging.getLogger(__name__)


class DataManager:
    """Manage the local data-store acquisition/updates from all workflows."""

    def __init__(self, workfloworkflows_mgr):
        self.workflows_mgr = workfloworkflows_mgr
        self.data = {}
        self.w_subs = {}
        self.topics = {topic.encode('utf-8') for topic in DELTAS_MAP}
        self.loop = None

    async def sync_workflows(self):
        """Run data store sync with workflow services.

        Subscriptions and sync management is instantiated and run in
        a separate thread for each workflow. This is to avoid the sync loop
        blocking the main loop.
        """
        self.loop = asyncio.get_running_loop()
        # Might be options other than threads to achieve
        # non-blocking subscriptions, but this works.
        with ThreadPoolExecutor() as pool:
            while True:
                for w_id, info in self.workflows_mgr.workflows.items():
                    if w_id not in self.w_subs:
                        pool.submit(
                            partial(
                                self._start_subscription,
                                w_id,
                                info['host'],
                                info['pub_port']))
                        await self.entire_workflow_update(ids=[w_id])
                for w_id in list(self.w_subs):
                    if w_id not in self.workflows_mgr.workflows:
                        self.w_subs[w_id].stop()
                        del self.w_subs[w_id]
                        if w_id in self.data:
                            del self.data[w_id]

                await asyncio.sleep(1.0)

    def _start_subscription(self, w_id, host, port):
        """Instatiate and run subscriber and data-store management."""
        self.w_subs[w_id] = WorkflowSubscriber(
            host, port,
            context=self.workflows_mgr.context, topics=self.topics)
        self.w_subs[w_id].loop.run_until_complete(
            self.w_subs[w_id].subscribe(
                process_delta_msg,
                func=self.update_workflow_data,
                w_id=w_id))

    def update_workflow_data(self, topic, delta, w_id):
        """Manage and apply incomming data-store deltas."""
        loop_cnt = 0
        while loop_cnt < 5:
            if w_id not in self.data:
                sleep(0.5)
                loop_cnt += 1
                continue
            break
        if w_id not in self.data:
            return
        delta_time = getattr(
                delta, 'time', getattr(delta, 'last_updated', 0.0))
        # If the workflow has reloaded recreate the data
        if delta.reloaded:
            self.data[w_id][topic] = {ele.id: ele for ele in delta.deltas}
            self.data[w_id]['delta_times'][topic] = delta_time
        elif delta_time >= self.data[w_id]['delta_times'][topic]:
            apply_delta(topic, delta, self.data[w_id])
            self.data[w_id]['delta_times'][topic] = delta_time
            self.reconcile_update(topic, delta, w_id)

    def reconcile_update(self, topic, delta, w_id):
        """Reconcile local with workflow data-store.

        Verify data-store is in sync by topic/element-type
        and on failure request entire set of respective data elements.

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
            future = asyncio.run_coroutine_threadsafe(
                workflow_request(
                    self.workflows_mgr.workflows[w_id]['req_client'],
                    'pb_data_elements',
                    args={'element_type': topic}
                ),
                self.loop
            )
            try:
                _, new_delta_msg = future.result(5.0)
            except asyncio.TimeoutError:
                logger.info(f'The reconcile update coroutine {w_id} {topic}'
                            f'took too long, cancelling the task...')
                future.cancel()
            except Exception as exc:
                logger.exception(exc)
            else:
                new_delta = DELTAS_MAP[topic]()
                new_delta.ParseFromString(new_delta_msg)
                apply_delta(topic, new_delta, self.data[w_id])
                self.data[w_id]['delta_times'][topic] = new_delta.time

    # Data syncing
    async def entire_workflow_update(self, ids=None):
        """Update all data of workflow(s) from associated WS."""
        if ids is None:
            ids = []

        # Prune old data
        for w_id in list(self.data):
            if w_id not in self.workflows_mgr.workflows:
                del self.data[w_id]

        # Request new data
        req_method = 'pb_entire_workflow'
        req_kwargs = (
            {'client': info['req_client'],
             'command': req_method,
             'req_context': w_id}
            for w_id, info in self.workflows_mgr.workflows.items())
        gathers = ()
        for kwargs in req_kwargs:
            if not ids or kwargs['req_context'] in ids:
                gathers += (workflow_request(**kwargs),)
        items = await asyncio.gather(*gathers)
        new_data = {}
        for w_id, result in items:
            if result is not None and result != MSG_TIMEOUT:
                pb_data = PB_METHOD_MAP[req_method]()
                pb_data.ParseFromString(result)
                new_data[w_id] = {
                    EDGES: {e.id: e for e in getattr(pb_data, EDGES)},
                    FAMILIES: {f.id: f for f in getattr(pb_data, FAMILIES)},
                    FAMILY_PROXIES: {
                        n.id: n
                        for n in getattr(pb_data, FAMILY_PROXIES)},
                    JOBS: {j.id: j for j in getattr(pb_data, JOBS)},
                    TASKS: {t.id: t for t in getattr(pb_data, TASKS)},
                    TASK_PROXIES: {
                        n.id: n
                        for n in getattr(pb_data, TASK_PROXIES)},
                    WORKFLOW: getattr(pb_data, WORKFLOW),
                    'delta_times': {
                        topic: getattr(pb_data, WORKFLOW).last_updated
                        for topic in DELTAS_MAP.keys()}
                }

        self.data.update(new_data)
