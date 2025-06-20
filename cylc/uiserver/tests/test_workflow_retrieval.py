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

"""This file tests the ability for the cylc UI to retrieve workflow information
and perform simple statistical calculations for the analysis tab"""

from typing import Union
import pytest
import sqlite3

from cylc.flow.id import Tokens
from cylc.uiserver.schema import (
    run_task_query,
    run_jobs_query,
    list_elements,
    get_elements,
)


def make_db(task_entries, task_events=None):
    """Create a DB and populate the task_jobs table."""
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    conn.execute(
        '''
        CREATE TABLE
            task_jobs(
                cycle TEXT,
                name TEXT,
                submit_num INTEGER,
                flow_nums TEXT,
                is_manual_submit INTEGER,
                try_num INTEGER,
                time_submit TEXT,
                time_submit_exit TEXT,
                submit_status INTEGER,
                time_run TEXT,
                time_run_exit TEXT,
                run_signal TEXT,
                run_status INTEGER,
                platform_name TEXT,
                job_runner_name TEXT,
                job_id TEXT,
                PRIMARY KEY(cycle, name, submit_num)
            );
    '''
    )

    conn.execute(
        '''
        CREATE TABLE 
            task_events(
                cycle TEXT, 
                name TEXT, 
                submit_num INTEGER,
                time TEXT, 
                event TEXT, 
                message TEXT);''')

    conn.executemany(
        'INSERT into task_jobs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        task_entries
    )
    if task_events:
        conn.executemany(
            'INSERT into task_events VALUES (?,?,?,?,?,?)',
            task_events
        )
    conn.commit()
    return conn


def test_make_task_query_1():
    conn = make_db(
        task_entries=[(
            '1',
            'Task_1',
            1,
            '[1]',
            0,
            1,
            '2022-12-14T15:00:00Z',
            '2022-12-14T15:01:00Z',
            0,
            '2022-12-14T15:01:00Z',
            '2022-12-14T15:10:00Z',
            None,
            0,
            'MyPlatform',
            'User',
            'UsersJob',
        )],
        task_events=[
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:00:00Z',
                'submitted',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:01:00Z',
                'started',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:10:00Z',
                'succeeded',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:10:00Z',
                'message_debug',
                '{    "max_rss": 40064,    "cpu_time": 994}'
            )
        ]
    )
    workflow = Tokens('~user/workflow')

    return_value = run_task_query(conn, workflow)

    assert return_value[0]['count'] == 1
    assert return_value[0]['cycle_point'] == '1'
    assert return_value[0]['finished_time'] == '2022-12-14T15:10:00Z'
    assert return_value[0]['queue_quartiles'][0] == 60
    assert return_value[0]['run_quartiles'][0] == 540
    assert return_value[0]['total_quartiles'][0] == 600
    assert return_value[0]['max_rss_quartiles'][0] == 40064
    assert return_value[0]['cpu_time_quartiles'][0] == 994
    assert return_value[0]['id'].id == '~user/workflow//1/Task_1/01'
    assert return_value[0]['job_ID'] == 'UsersJob'
    assert return_value[0]['max_queue_time'] == 60
    assert return_value[0]['max_run_time'] == 540
    assert return_value[0]['max_total_time'] == 600
    assert return_value[0]['max_max_rss'] == 40064
    assert return_value[0]['max_cpu_time'] == 994
    assert return_value[0]['mean_queue_time'] == pytest.approx(60.0, 0.01)
    assert return_value[0]['mean_run_time'] == pytest.approx(540.0, 0.01)
    assert return_value[0]['mean_total_time'] == pytest.approx(600.0, 0.01)
    assert return_value[0]['mean_max_rss'] == pytest.approx(40064.0, 0.01)
    assert return_value[0]['mean_cpu_time'] == pytest.approx(994.0, 0.01)
    assert return_value[0]['min_queue_time'] == 60
    assert return_value[0]['min_run_time'] == 540
    assert return_value[0]['min_total_time'] == 600
    assert return_value[0]['min_max_rss'] == 40064
    assert return_value[0]['min_cpu_time'] == 994
    assert return_value[0]['name'] == 'Task_1'
    assert return_value[0]['platform'] == 'MyPlatform'
    assert return_value[0]['queue_quartiles'][1] == 60
    assert return_value[0]['run_quartiles'][1] == 540
    assert return_value[0]['total_quartiles'][1] == 600
    assert return_value[0]['max_rss_quartiles'][1] == 40064
    assert return_value[0]['cpu_time_quartiles'][1] == 994
    assert return_value[0]['started_time'] == '2022-12-14T15:01:00Z'
    assert return_value[0]['state'] == 'succeeded'
    assert return_value[0]['std_dev_queue_time'] == pytest.approx(0.0, 0.01)
    assert return_value[0]['std_dev_run_time'] == pytest.approx(0.0, 0.01)
    assert return_value[0]['std_dev_total_time'] == pytest.approx(0.0, 0.01)
    assert return_value[0]['std_dev_max_rss'] == pytest.approx(0.0, 0.01)
    assert return_value[0]['std_dev_cpu_time'] == pytest.approx(0.0, 0.01)
    assert return_value[0]['submit_num'] == 1
    assert return_value[0]['submitted_time'] == '2022-12-14T15:00:00Z'
    assert return_value[0]['queue_quartiles'][2] == 60
    assert return_value[0]['run_quartiles'][2] == 540
    assert return_value[0]['total_quartiles'][2] == 600
    assert return_value[0]['max_rss_quartiles'][2] == 40064
    assert return_value[0]['cpu_time_quartiles'][2] == 994
    assert return_value[0]['total_of_totals'] == 994


def test_make_task_query_2():
    conn = make_db(
        task_entries=[
            (
                '1',
                'Task_1',
                1,
                '[1]',
                0,
                1,
                '2022-12-14T15:00:00Z',
                '2022-12-14T15:01:00Z',
                0,
                '2022-12-14T15:01:00Z',
                '2022-12-14T15:10:00Z',
                None,
                0,
                'MyPlatform',
                'User',
                'UsersJob',
            ),
            (
                '2',
                'Task_1',
                1,
                '[1]',
                0,
                1,
                '2022-12-15T15:00:00Z',
                '2022-12-15T15:01:15Z',
                0,
                '2022-12-15T15:01:16Z',
                '2022-12-15T15:12:00Z',
                None,
                0,
                'MyPlatform',
                'User',
                'UsersJob',
            )
        ],
        task_events=[
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:00:00Z',
                'submitted',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:01:00Z',
                'started',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:10:00Z',
                'succeeded',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:10:00Z',
                'message_debug',
                '{    "max_rss": 40064,    "cpu_time": 994}'
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:00:00Z',
                'submitted',
                ''
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:01:00Z',
                'started',
                ''
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:10:00Z',
                'succeeded',
                ''
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:10:00Z',
                'message_debug',
                '{    "max_rss": 50064,    "cpu_time": 1994}'
            ),
        ]
    )
    conn.commit()
    workflow = Tokens('~user/workflow')

    return_value = run_task_query(conn, workflow)

    assert return_value[0]['count'] == 2
    assert return_value[0]['cycle_point'] == '2'
    assert return_value[0]['finished_time'] == '2022-12-15T15:12:00Z'
    assert return_value[0]['queue_quartiles'][0] == 60
    assert return_value[0]['run_quartiles'][0] == 540
    assert return_value[0]['total_quartiles'][0] == 600
    assert return_value[0]['max_rss_quartiles'][0] == 40064
    assert return_value[0]['cpu_time_quartiles'][0] == 994
    assert return_value[0]['id'].id == '~user/workflow//2/Task_1/01'
    assert return_value[0]['job_ID'] == 'UsersJob'
    assert return_value[0]['max_queue_time'] == 76
    assert return_value[0]['max_run_time'] == 644
    assert return_value[0]['max_total_time'] == 720
    assert return_value[0]['max_max_rss'] == 50064
    assert return_value[0]['max_cpu_time'] == 1994
    assert return_value[0]['mean_queue_time'] == pytest.approx(68.0, 0.01)
    assert return_value[0]['mean_run_time'] == pytest.approx(592.0, 0.01)
    assert return_value[0]['mean_total_time'] == pytest.approx(660.0, 0.01)
    assert return_value[0]['mean_max_rss'] == pytest.approx(45064.0, 0.01)
    assert return_value[0]['mean_cpu_time'] == pytest.approx(1494.0, 0.01)
    assert return_value[0]['min_queue_time'] == 60
    assert return_value[0]['min_run_time'] == 540
    assert return_value[0]['min_total_time'] == 600
    assert return_value[0]['min_max_rss'] == 40064
    assert return_value[0]['min_cpu_time'] == 994
    assert return_value[0]['name'] == 'Task_1'
    assert return_value[0]['platform'] == 'MyPlatform'
    assert return_value[0]['queue_quartiles'][1] == 76
    assert return_value[0]['run_quartiles'][1] == 644
    assert return_value[0]['total_quartiles'][1] == 720
    assert return_value[0]['max_rss_quartiles'][1] == 50064
    assert return_value[0]['cpu_time_quartiles'][1] == 1994
    assert return_value[0]['started_time'] == '2022-12-15T15:01:16Z'
    assert return_value[0]['state'] == 'succeeded'
    assert return_value[0]['std_dev_queue_time'] == pytest.approx(8.00, 0.01)
    assert return_value[0]['std_dev_run_time'] == pytest.approx(52.0, 0.01)
    assert return_value[0]['std_dev_total_time'] == pytest.approx(60.0, 0.01)
    assert return_value[0]['std_dev_max_rss'] == pytest.approx(5000.0, 0.01)
    assert return_value[0]['std_dev_cpu_time'] == pytest.approx(500.0, 0.01)
    assert return_value[0]['submit_num'] == 1
    assert return_value[0]['submitted_time'] == '2022-12-15T15:00:00Z'
    assert return_value[0]['queue_quartiles'][2] == 60
    assert return_value[0]['run_quartiles'][2] == 540
    assert return_value[0]['total_quartiles'][2] == 600
    assert return_value[0]['max_rss_quartiles'][2] == 40064
    assert return_value[0]['cpu_time_quartiles'][2] == 994
    assert return_value[0]['total_of_totals'] == 1994


def test_make_task_query_3():
    conn = make_db(
        task_entries=[
            (
                '1',
                'Task_1',
                1,
                '[1]',
                0,
                1,
                '2022-12-14T15:00:00Z',
                '2022-12-14T15:01:00Z',
                0,
                '2022-12-14T15:01:00Z',
                '2022-12-14T15:10:00Z',
                None,
                0,
                'MyPlatform',
                'User',
                'UsersJob',
            ),
            (
                '2',
                'Task_1',
                1,
                '[1]',
                0,
                1,
                '2022-12-15T15:00:00Z',
                '2022-12-15T15:01:15Z',
                0,
                '2022-12-15T15:01:16Z',
                '2022-12-15T15:12:00Z',
                None,
                0,
                'MyPlatform',
                'User',
                'UsersJob',
            ),
            (
                '3',
                'Task_1',
                1,
                '[1]',
                0,
                1,
                '2022-12-16T15:00:00Z',
                '2022-12-16T15:01:15Z',
                0,
                '2022-12-16T15:01:16Z',
                '2022-12-16T15:12:00Z',
                None,
                0,
                'MyPlatform',
                'User',
                'UsersJob',
            )
        ],
        task_events=[
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:00:00Z',
                'submitted',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:01:00Z',
                'started',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:10:00Z',
                'succeeded',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:10:00Z',
                'message_debug',
                '{    "max_rss": 40064,    "cpu_time": 994}'
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:00:00Z',
                'submitted',
                ''
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:01:00Z',
                'started',
                ''
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:10:00Z',
                'succeeded',
                ''
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:10:00Z',
                'message_debug',
                '{    "max_rss": 50064,    "cpu_time": 1994}'
            ),
            (
                '3',
                'Task_1',
                1,
                '2022-12-14T17:00:00Z',
                'submitted',
                ''
            ),
            (
                '3',
                'Task_1',
                1,
                '2022-12-14T17:01:00Z',
                'started',
                ''
            ),
            (
                '3',
                'Task_1',
                1,
                '2022-12-14T17:10:00Z',
                'succeeded',
                ''
            ),
            (
                '3',
                'Task_1',
                1,
                '2022-12-14T17:10:00Z',
                'message_debug',
                '{    "max_rss": 60064,    "cpu_time": 2994}'
            ),
        ]
    )
    conn.commit()
    workflow = Tokens('~user/workflow')

    return_value = run_task_query(conn, workflow)

    assert len(return_value) == 1
    assert return_value[0]['count'] == 3
    assert return_value[0]['cycle_point'] == '3'
    assert return_value[0]['finished_time'] == '2022-12-16T15:12:00Z'
    assert return_value[0]['queue_quartiles'][0] == 60
    assert return_value[0]['run_quartiles'][0] == 540
    assert return_value[0]['total_quartiles'][0] == 600
    assert return_value[0]['max_rss_quartiles'][0] == 40064
    assert return_value[0]['cpu_time_quartiles'][0] == 994
    assert return_value[0]['id'].id == '~user/workflow//3/Task_1/01'
    assert return_value[0]['job_ID'] == 'UsersJob'
    assert return_value[0]['max_queue_time'] == 76
    assert return_value[0]['max_run_time'] == 644
    assert return_value[0]['max_total_time'] == 720
    assert return_value[0]['max_max_rss'] == 60064
    assert return_value[0]['max_cpu_time'] == 2994
    assert return_value[0]['mean_queue_time'] == pytest.approx(70.66, 0.01)
    assert return_value[0]['mean_run_time'] == pytest.approx(609.33, 0.01)
    assert return_value[0]['mean_total_time'] == pytest.approx(680.0, 0.01)
    assert return_value[0]['mean_max_rss'] == pytest.approx(50064.0, 0.01)
    assert return_value[0]['min_queue_time'] == 60
    assert return_value[0]['min_run_time'] == 540
    assert return_value[0]['min_total_time'] == 600
    assert return_value[0]['min_max_rss'] == 40064
    assert return_value[0]['min_cpu_time'] == 994
    assert return_value[0]['name'] == 'Task_1'
    assert return_value[0]['platform'] == 'MyPlatform'
    assert return_value[0]['queue_quartiles'][1] == 76
    assert return_value[0]['run_quartiles'][1] == 644
    assert return_value[0]['total_quartiles'][1] == 720
    assert return_value[0]['max_rss_quartiles'][1] == 50064
    assert return_value[0]['cpu_time_quartiles'][1] == 1994
    assert return_value[0]['started_time'] == '2022-12-16T15:01:16Z'
    assert return_value[0]['state'] == 'succeeded'
    assert return_value[0]['std_dev_queue_time'] == pytest.approx(7.54, 0.01)
    assert return_value[0]['std_dev_run_time'] == pytest.approx(49.02, 0.01)
    assert return_value[0]['std_dev_total_time'] == pytest.approx(56.56, 0.01)
    assert return_value[0]['std_dev_max_rss'] == pytest.approx(8164.0, 0.01)
    assert return_value[0]['std_dev_cpu_time'] == pytest.approx(816.4, 0.01)
    assert return_value[0]['submit_num'] == 1
    assert return_value[0]['submitted_time'] == '2022-12-16T15:00:00Z'
    assert return_value[0]['queue_quartiles'][2] == 76
    assert return_value[0]['run_quartiles'][2] == 644
    assert return_value[0]['total_quartiles'][2] == 720
    assert return_value[0]['max_rss_quartiles'][2] == 60064
    assert return_value[0]['cpu_time_quartiles'][2] == 2994
    assert return_value[0]['total_of_totals'] == 2994


def test_make_jobs_query_1():
    conn = make_db(
        task_entries=[
            (
                '1',
                'Task_1',
                1,
                '[1]',
                0,
                1,
                '2022-12-14T15:00:00Z',
                '2022-12-14T15:01:00Z',
                0,
                '2022-12-14T15:01:00Z',
                '2022-12-14T15:10:00Z',
                None,
                0,
                'MyPlatform',
                'User',
                'UsersJob',
            ),
            (
                '2',
                'Task_1',
                1,
                '[1]',
                0,
                1,
                '2022-12-15T15:00:00Z',
                '2022-12-15T15:01:15Z',
                0,
                '2022-12-15T15:01:16Z',
                '2022-12-15T15:12:00Z',
                None,
                0,
                'MyPlatform',
                'User',
                'UsersJob',
            ),
            (
                '3',
                'Task_1',
                1,
                '[1]',
                0,
                1,
                '2022-12-16T15:00:00Z',
                '2022-12-16T15:01:15Z',
                0,
                '2022-12-16T15:01:16Z',
                '2022-12-16T15:12:00Z',
                None,
                0,
                'MyPlatform',
                'User',
                'UsersJob',
            )
        ],
        task_events=[
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:00:00Z',
                'submitted',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:01:00Z',
                'started',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:10:00Z',
                'succeeded',
                ''
            ),
            (
                '1',
                'Task_1',
                1,
                '2022-12-14T15:10:00Z',
                'message_debug',
                '{    "max_rss": 40064,    "cpu_time": 994}'
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:00:00Z',
                'submitted',
                ''
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:01:00Z',
                'started',
                ''
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:10:00Z',
                'succeeded',
                ''
            ),
            (
                '2',
                'Task_1',
                1,
                '2022-12-14T16:10:00Z',
                'message_debug',
                '{    "max_rss": 50064,    "cpu_time": 1994}'
            ),
            (
                '3',
                'Task_1',
                1,
                '2022-12-14T17:00:00Z',
                'submitted',
                ''
            ),
            (
                '3',
                'Task_1',
                1,
                '2022-12-14T17:01:00Z',
                'started',
                ''
            ),
            (
                '3',
                'Task_1',
                1,
                '2022-12-14T17:10:00Z',
                'succeeded',
                ''
            ),
            (
                '3',
                'Task_1',
                1,
                '2022-12-14T17:10:00Z',
                'message_debug',
                '{    "max_rss": 60064,    "cpu_time": 2994}'
            ),
        ]
    )
    conn.commit()
    workflow = Tokens('~user/workflow')
    tasks = []

    return_value = run_jobs_query(conn, workflow, tasks)

    assert len(return_value) == 3
    assert return_value[0]['cycle_point'] == '1'
    assert return_value[0]['finished_time'] == '2022-12-14T15:10:00Z'
    assert return_value[0]['id'].id == '~user/workflow//1/Task_1/01'
    assert return_value[0]['job_ID'] == 'UsersJob'
    assert return_value[0]['name'] == 'Task_1'
    assert return_value[0]['platform'] == 'MyPlatform'
    assert return_value[0]['started_time'] == '2022-12-14T15:01:00Z'
    assert return_value[0]['state'] == 'succeeded'
    assert return_value[0]['submit_num'] == 1
    assert return_value[0]['submitted_time'] == '2022-12-14T15:00:00Z'

    assert return_value[1]['cycle_point'] == '2'
    assert return_value[1]['finished_time'] == '2022-12-15T15:12:00Z'
    assert return_value[1]['id'].id == '~user/workflow//2/Task_1/01'
    assert return_value[1]['job_ID'] == 'UsersJob'
    assert return_value[1]['name'] == 'Task_1'
    assert return_value[1]['platform'] == 'MyPlatform'
    assert return_value[1]['started_time'] == '2022-12-15T15:01:16Z'
    assert return_value[1]['state'] == 'succeeded'
    assert return_value[1]['submit_num'] == 1
    assert return_value[1]['submitted_time'] == '2022-12-15T15:00:00Z'


async def test_list_elements(monkeypatch):
    with pytest.raises(Exception) as e_info:
        await list_elements('tasks', stuff=[1, 2, 3], workflows=[])

    exception_raised = e_info.value
    assert (
        exception_raised.args[0] == 'At least one workflow must be provided.'
    )


@pytest.mark.parametrize(
    'field_ids, kwargs, expected',
    [
        pytest.param(
            [],
            {
                'ids': ['//1/t/01'],
                'workflows': ['~u/w'],
            },
            [],
            id='field_ids = empty list',
        ),
        pytest.param(
            None,
            {
                'ids': ['//1/t/01'],
                'exids': ['//1/t/01'],
                'workflows': ['~u/w'],
                'exworkflows': ['~u2/w'],
            },
            {
                'live': False,
                'ids': [Tokens('//1/t/01')],
                'exids': [Tokens('//1/t/01')],
                'workflows': [Tokens('~u/w')],
                'exworkflows': [Tokens('~u2/w')],
            },
            id='field_ids = None',
        ),
        pytest.param(
            '//2/t/01',
            {
                'ids': ['//1/t/01'],
                'exids': [],
                'workflows': ['~u/w'],
                'exworkflows': [],
            },
            {
                'live': False,
                'ids': [Tokens('//2/t/01')],
                'exids': [],
                'workflows': [Tokens('~u/w')],
                'exworkflows': [],
            },
            id='field_ids = str',
        ),
        pytest.param(
            {
                '//2/t/01': 'something',
                '//2/t/02': 'something else',
            },
            {
                'ids': ['//1/t/01'],
                'exids': [],
                'workflows': ['~u/w'],
                'exworkflows': [],
            },
            {
                'live': False,
                'ids': [Tokens('//2/t/01'), Tokens('//2/t/02')],
                'exids': [],
                'workflows': [Tokens('~u/w')],
                'exworkflows': [],
            },
            id='field_ids = dict',
        ),
    ],
)
async def test_get_elements(
    monkeypatch: pytest.MonkeyPatch, field_ids, kwargs, expected
):
    # get_elements takes 2 args, root and info and kwargs.
    # Root always seems to be none
    root = None
    # info is a graphql object that only gets used to pass on other
    # functions that I'm not testing
    info = None

    async def mock_return_list_elements(_query_type, **kwargs):
        return kwargs

    def mock_process_resolver_info(*args):
        return None, field_ids

    monkeypatch.setattr(
        'cylc.uiserver.schema.list_elements',
        mock_return_list_elements,
    )
    monkeypatch.setattr(
        'cylc.uiserver.schema.process_resolver_info',
        mock_process_resolver_info,
    )

    assert await get_elements(
        'tasks',
        root,
        info,
        live=False,
        **kwargs
    ) == expected


async def test_job_query_filter():
    def make_job(task_name, submit_status, run_status, started):
        submit_start = submit_end = run_start = run_end = None
        if submit_status:
            submit_start = '2022-12-14T15:00:00Z'
            submit_end = '2022-12-14T15:01:00Z'
        if started:
            run_start = '2022-12-14T15:02:00Z'
        if run_status:
            run_end = '2022-12-14T15:03:00Z'

        return (
            '1',
            task_name,
            1,
            '[1]',
            0,
            0,
            submit_start,
            submit_end,
            submit_status,
            run_start,
            run_end,
            run_status,  # run signal
            run_status,
            'MyPlatform',
            'User',
            'UsersJob',
        )

    # define a workflow with one job in each state
    conn = make_db(
        task_entries=[
            make_job('waiting', None, None, None),
            make_job('submitted', 0, None, False),
            make_job('submit-failed', 1, None, False),
            make_job('running', 0, None, True),
            make_job('succeeded', 0, 0, True),
            make_job('failed', 0, 1, True)],
    )
    workflow = Tokens('~user/workflow')

    # all jobs should appear by default (no filters)
    # Note: The waiting task has no associated job
    assert {
        item['id']['task'] for item in run_jobs_query(conn, workflow)
    } == {
        'submitted',
        'submit-failed',
        'running',
        'succeeded',
        'failed',
    }

    # filter by ids
    assert {
        item['id']['task']
        for item in run_jobs_query(conn, workflow, ids=[Tokens('//*/s*/01')])
    } == {
        'submitted',
        'submit-failed',
        'succeeded',
    }

    # filter by exids
    assert {
        item['id']['task']
        for item in run_jobs_query(conn, workflow, exids=[Tokens('//*/s*/01')])
    } == {
        'running',
        'failed',
    }

    # filter by overlapping ids & exids
    assert {
        item['id']['task']
        for item in run_jobs_query(
            conn,
            workflow,
            ids=[Tokens('//*/submitted'), Tokens('//*/succeeded')],
            exids=[Tokens('//*/succeeded'), Tokens('//*/submit-failed')],
        )
    } == {
        'submitted',
    }

    # filter by states
    assert {
        item['id']['task']
        for item in run_jobs_query(conn, workflow, states=['succeeded'])
    } == {
        'succeeded',
    }

    # quirk: cannot filter for waiting jobs (no such thing) so the filter is
    # ignored
    assert {
        item['id']['task']
        for item in run_jobs_query(conn, workflow, states=['waiting'])
    } == {
        'submitted',
        'submit-failed',
        'running',
        'succeeded',
        'failed',
    }

    # filter by exstates
    assert {
        item['id']['task']
        for item in run_jobs_query(conn, workflow, exstates=['succeeded'])
    } == {
        'submitted',
        'submit-failed',
        'running',
        'failed',
    }
    # quirk: cannot filter for waiting jobs (no such thing) so the filter is
    # ignored
    assert {
        item['id']['task']
        for item in run_jobs_query(conn, workflow, exstates=['waiting'])
    } == {
        'submitted',
        'submit-failed',
        'running',
        'succeeded',
        'failed',
    }

    # filter by overlapping states and exstates
    assert {
        item['id']['task']
        for item in run_jobs_query(
            conn,
            workflow,
            states=['submitted', 'succeeded'],
            exstates=['succeeded', 'submit-failed']
        )
    } == {
        'submitted',
    }

    # filter by namespace name
    assert {
        item['id']['task']
        for item in run_jobs_query(
            conn,
            workflow,
            tasks=['submit-failed', 'failed']
        )
    } == {
        'submit-failed',
        'failed',
    }


@pytest.mark.parametrize('jobs, query, expected', [
    pytest.param(
        [
            (2025, 'a', 2),
            (2025, 'a', 3),
            (2025, 'a', 1),
            (2025, 'b', 1),
        ],
        ['2025/*/NN'],
        {'2025/a/03', '2025/b/01'},
        id="selects-latest-jobs"
    )
])
async def test_jobNN_query(jobs, query, expected):
    """Jobs query should handle job 'NN'."""
    def make_job(cycle: Union[str, int], name: str, submit_num: int):
        return (
            str(cycle),
            name,
            submit_num,
            '[1]',
            0,
            1,
            '2022-12-14T15:00:00Z',
            '2022-12-14T15:00:03Z',
            1,
            '',
            '',
            '',
            0,
            'enterprise-bg',
            'background',
            '1701',
        )
    conn = make_db(task_entries=(make_job(*job) for job in jobs))
    workflow = Tokens('~user/workflow')
    result = run_jobs_query(
        conn, workflow, ids=[Tokens(i, relative=True) for i in query]
    )
    assert {item['id'].relative_id for item in result} == expected
