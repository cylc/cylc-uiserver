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

import pytest
import sqlite3
from typing import List

from cylc.flow.id import Tokens
from cylc.uiserver.schema import run_task_query, run_jobs_query, \
    list_elements, get_elements


'''This file tests the ability for the cylc UI to retrieve workflow information
and perform simple statistical calculations for the analysis tab'''


def test_make_task_query_1():
    conn = sqlite3.connect(':memory:')
    conn.execute('''CREATE TABLE task_jobs(cycle TEXT, name TEXT,
    submit_num INTEGER, flow_nums TEXT, is_manual_submit INTEGER,
    try_num INTEGER, time_submit TEXT, time_submit_exit TEXT,
    submit_status INTEGER, time_run TEXT, time_run_exit TEXT,
    run_signal TEXT, run_status INTEGER, platform_name TEXT,
    job_runner_name TEXT, job_id TEXT,
    PRIMARY KEY(cycle, name, submit_num));''')

    conn.executemany(
        'INSERT into task_jobs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        [('1', 'Task_1', '01', '{1}', 0, 1,
          '2022-12-14T15:00:00Z', '2022-12-14T15:01:00Z', 0,
          '2022-12-14T15:01:00Z', '2022-12-14T15:10:00Z', None, 0,
          'MyPlatform', 'User', 'UsersJob')
         ])
    conn.commit()
    workflow = Tokens('~user/workflow')

    return_value = run_task_query(conn, workflow)

    assert return_value[0]['count'] == 1
    assert return_value[0]['cycle_point'] == '1'
    assert return_value[0]['finished_time'] == '2022-12-14T15:10:00Z'
    assert return_value[0]['queue_quartiles'][0] == 60
    assert return_value[0]['run_quartiles'][0] == 540
    assert return_value[0]['total_quartiles'][0] == 600
    assert return_value[0]['id'].id == '~user/workflow//1/Task_1/01'
    assert return_value[0]['job_ID'] == 'UsersJob'
    assert return_value[0]['max_queue_time'] == 60
    assert return_value[0]['max_run_time'] == 540
    assert return_value[0]['max_total_time'] == 600
    assert return_value[0]['mean_queue_time'] == pytest.approx(60.0, 0.01)
    assert return_value[0]['mean_run_time'] == pytest.approx(540.0, 0.01)
    assert return_value[0]['mean_total_time'] == pytest.approx(600.0, 0.01)
    assert return_value[0]['min_queue_time'] == 60
    assert return_value[0]['min_run_time'] == 540
    assert return_value[0]['min_total_time'] == 600
    assert return_value[0]['name'] == 'Task_1'
    assert return_value[0]['platform'] == 'MyPlatform'
    assert return_value[0]['queue_quartiles'][1] == 60
    assert return_value[0]['run_quartiles'][1] == 540
    assert return_value[0]['total_quartiles'][1] == 600
    assert return_value[0]['started_time'] == '2022-12-14T15:01:00Z'
    assert return_value[0]['state'] == 0
    assert return_value[0]['std_dev_queue_time'] == pytest.approx(0.0, 0.01)
    assert return_value[0]['std_dev_run_time'] == pytest.approx(0.0, 0.01)
    assert return_value[0]['std_dev_total_time'] == pytest.approx(0.0, 0.01)
    assert return_value[0]['submit_num'] == 1
    assert return_value[0]['submitted_time'] == '2022-12-14T15:00:00Z'
    assert return_value[0]['queue_quartiles'][2] == 60
    assert return_value[0]['run_quartiles'][2] == 540
    assert return_value[0]['total_quartiles'][2] == 600


def test_make_task_query_2():
    conn = sqlite3.connect(':memory:')
    conn.execute('''CREATE TABLE task_jobs(cycle TEXT, name TEXT,
    submit_num INTEGER, flow_nums TEXT, is_manual_submit INTEGER,
    try_num INTEGER, time_submit TEXT, time_submit_exit TEXT,
    submit_status INTEGER, time_run TEXT, time_run_exit TEXT,
    run_signal TEXT, run_status INTEGER, platform_name TEXT,
    job_runner_name TEXT, job_id TEXT,
    PRIMARY KEY(cycle, name, submit_num));''')

    conn.executemany(
        'INSERT into task_jobs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        [('1', 'Task_1', '01', '{1}', 0, 1,
          '2022-12-14T15:00:00Z', '2022-12-14T15:01:00Z', 0,
          '2022-12-14T15:01:00Z', '2022-12-14T15:10:00Z', None, 0,
          'MyPlatform', 'User', 'UsersJob'),
         ('2', 'Task_1', '01', '{1}', 0, 1,
          '2022-12-15T15:00:00Z', '2022-12-15T15:01:15Z', 0,
          '2022-12-15T15:01:16Z', '2022-12-15T15:12:00Z', None, 0,
          'MyPlatform', 'User', 'UsersJob')
         ])
    conn.commit()
    workflow = Tokens('~user/workflow')

    return_value = run_task_query(conn, workflow)

    assert return_value[0]['count'] == 2
    assert return_value[0]['cycle_point'] == '2'
    assert return_value[0]['finished_time'] == '2022-12-15T15:12:00Z'
    assert return_value[0]['queue_quartiles'][0] == 60
    assert return_value[0]['run_quartiles'][0] == 540
    assert return_value[0]['total_quartiles'][0] == 600
    assert return_value[0]['id'].id == '~user/workflow//2/Task_1/01'
    assert return_value[0]['job_ID'] == 'UsersJob'
    assert return_value[0]['max_queue_time'] == 76
    assert return_value[0]['max_run_time'] == 644
    assert return_value[0]['max_total_time'] == 720
    assert return_value[0]['mean_queue_time'] == pytest.approx(68.0, 0.01)
    assert return_value[0]['mean_run_time'] == pytest.approx(592.0, 0.01)
    assert return_value[0]['mean_total_time'] == pytest.approx(660.0, 0.01)
    assert return_value[0]['min_queue_time'] == 60
    assert return_value[0]['min_run_time'] == 540
    assert return_value[0]['min_total_time'] == 600
    assert return_value[0]['name'] == 'Task_1'
    assert return_value[0]['platform'] == 'MyPlatform'
    assert return_value[0]['queue_quartiles'][1] == 76
    assert return_value[0]['run_quartiles'][1] == 644
    assert return_value[0]['total_quartiles'][1] == 720
    assert return_value[0]['started_time'] == '2022-12-15T15:01:16Z'
    assert return_value[0]['state'] == 0
    assert return_value[0]['std_dev_queue_time'] == pytest.approx(8.00, 0.01)
    assert return_value[0]['std_dev_run_time'] == pytest.approx(52.0, 0.01)
    assert return_value[0]['std_dev_total_time'] == pytest.approx(60.0, 0.01)
    assert return_value[0]['submit_num'] == 1
    assert return_value[0]['submitted_time'] == '2022-12-15T15:00:00Z'
    assert return_value[0]['queue_quartiles'][2] == 60
    assert return_value[0]['run_quartiles'][2] == 540
    assert return_value[0]['total_quartiles'][2] == 600


def test_make_task_query_3():
    conn = sqlite3.connect(':memory:')
    conn.execute('''CREATE TABLE task_jobs(cycle TEXT, name TEXT,
    submit_num INTEGER, flow_nums TEXT, is_manual_submit INTEGER,
    try_num INTEGER, time_submit TEXT, time_submit_exit TEXT,
    submit_status INTEGER, time_run TEXT, time_run_exit TEXT,
    run_signal TEXT, run_status INTEGER, platform_name TEXT,
    job_runner_name TEXT, job_id TEXT,
    PRIMARY KEY(cycle, name, submit_num));''')

    conn.executemany(
        'INSERT into task_jobs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        [('1', 'Task_1', '01', '{1}', 0, 1,
          '2022-12-14T15:00:00Z', '2022-12-14T15:01:00Z', 0,
          '2022-12-14T15:01:00Z', '2022-12-14T15:10:00Z', None, 0,
          'MyPlatform', 'User', 'UsersJob'),
         ('2', 'Task_1', '01', '{1}', 0, 1,
          '2022-12-15T15:00:00Z', '2022-12-15T15:01:15Z', 0,
          '2022-12-15T15:01:16Z', '2022-12-15T15:12:00Z', None, 0,
          'MyPlatform', 'User', 'UsersJob'),
         ('3', 'Task_1', '01', '{1}', 0, 1,
          '2022-12-16T15:00:00Z', '2022-12-16T15:01:15Z', 0,
          '2022-12-16T15:01:16Z', '2022-12-16T15:12:00Z', None, 0,
          'MyPlatform', 'User', 'UsersJob')
         ])
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
    assert return_value[0]['id'].id == '~user/workflow//3/Task_1/01'
    assert return_value[0]['job_ID'] == 'UsersJob'
    assert return_value[0]['max_queue_time'] == 76
    assert return_value[0]['max_run_time'] == 644
    assert return_value[0]['max_total_time'] == 720
    assert return_value[0]['mean_queue_time'] == pytest.approx(70.66, 0.01)
    assert return_value[0]['mean_run_time'] == pytest.approx(609.33, 0.01)
    assert return_value[0]['mean_total_time'] == pytest.approx(680.0, 0.01)
    assert return_value[0]['min_queue_time'] == 60
    assert return_value[0]['min_run_time'] == 540
    assert return_value[0]['min_total_time'] == 600
    assert return_value[0]['name'] == 'Task_1'
    assert return_value[0]['platform'] == 'MyPlatform'
    assert return_value[0]['queue_quartiles'][1] == 76
    assert return_value[0]['run_quartiles'][1] == 644
    assert return_value[0]['total_quartiles'][1] == 720
    assert return_value[0]['started_time'] == '2022-12-16T15:01:16Z'
    assert return_value[0]['state'] == 0
    assert return_value[0]['std_dev_queue_time'] == pytest.approx(7.54, 0.01)
    assert return_value[0]['std_dev_run_time'] == pytest.approx(49.02, 0.01)
    assert return_value[0]['std_dev_total_time'] == pytest.approx(56.56, 0.01)
    assert return_value[0]['submit_num'] == 1
    assert return_value[0]['submitted_time'] == '2022-12-16T15:00:00Z'
    assert return_value[0]['queue_quartiles'][2] == 76
    assert return_value[0]['run_quartiles'][2] == 644
    assert return_value[0]['total_quartiles'][2] == 720


def test_make_jobs_query_1():
    conn = sqlite3.connect(':memory:')
    conn.execute('''CREATE TABLE task_jobs(cycle TEXT, name TEXT,
    submit_num INTEGER, flow_nums TEXT, is_manual_submit INTEGER,
    try_num INTEGER, time_submit TEXT, time_submit_exit TEXT,
    submit_status INTEGER, time_run TEXT, time_run_exit TEXT,
    run_signal TEXT, run_status INTEGER, platform_name TEXT,
    job_runner_name TEXT, job_id TEXT,
    PRIMARY KEY(cycle, name, submit_num));''')

    conn.executemany(
        'INSERT into task_jobs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        [('1', 'Task_1', '01', '{1}', 0, 1,
          '2022-12-14T15:00:00Z', '2022-12-14T15:01:00Z', 0,
          '2022-12-14T15:01:00Z', '2022-12-14T15:10:00Z', None, 0,
          'MyPlatform', 'User', 'UsersJob'),
         ('2', 'Task_1', '01', '{1}', 0, 1,
          '2022-12-15T15:00:00Z', '2022-12-15T15:01:15Z', 0,
          '2022-12-15T15:01:16Z', '2022-12-15T15:12:00Z', None, 0,
          'MyPlatform', 'User', 'UsersJob'),
         ('3', 'Task_1', '01', '{1}', 0, 1,
          '2022-12-16T15:00:00Z', '2022-12-16T15:01:15Z', 0,
          '2022-12-16T15:01:16Z', '2022-12-16T15:12:00Z', None, 0,
          'MyPlatform', 'User', 'UsersJob')
         ])
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
    assert return_value[0]['state'] == 0
    assert return_value[0]['submit_num'] == 1
    assert return_value[0]['submitted_time'] == '2022-12-14T15:00:00Z'

    assert return_value[1]['cycle_point'] == '2'
    assert return_value[1]['finished_time'] == '2022-12-15T15:12:00Z'
    assert return_value[1]['id'].id == '~user/workflow//2/Task_1/01'
    assert return_value[1]['job_ID'] == 'UsersJob'
    assert return_value[1]['name'] == 'Task_1'
    assert return_value[1]['platform'] == 'MyPlatform'
    assert return_value[1]['started_time'] == '2022-12-15T15:01:16Z'
    assert return_value[1]['state'] == 0
    assert return_value[1]['submit_num'] == 1
    assert return_value[1]['submitted_time'] == '2022-12-15T15:00:00Z'


async def test_list_elements(monkeypatch):

    with pytest.raises(Exception) as e_info:
        await list_elements({'stuff': [1, 2, 3], 'workflows': []})

    exception_raised = e_info.value
    assert exception_raised.args[0] == \
           'At least one workflow must be provided.'


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
            id="field_ids = empty list"
        ),
        pytest.param(
            None,
            {
                'ids': ['//1/t/01'],
                'exids': ['//1/t/01'],
                'workflows': ['~u/w'],
                'exworkflows': ['~u2/w']
            },
            {
                'live': False,
                'ids': [Tokens('//1/t/01')],
                'exids': [Tokens('//1/t/01')],
                'workflows': [Tokens('~u/w')],
                'exworkflows': [Tokens('~u2/w')]
            },
            id="field_ids = None"
        ),
        pytest.param(
            '//2/t/01',
            {
                'ids': ['//1/t/01'],
                'exids': [],
                'workflows': ['~u/w'],
                'exworkflows': []
            },
            {
                'live': False,
                'ids': [Tokens('//2/t/01')],
                'exids': [],
                'workflows': [Tokens('~u/w')],
                'exworkflows': []
            },
            id="field_ids = str"
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
                'exworkflows': []
            },
            {
                'live': False,
                'ids': [Tokens('//2/t/01'), Tokens('//2/t/02')],
                'exids': [],
                'workflows': [Tokens('~u/w')],
                'exworkflows': []
            },
            id="field_ids = dict"
        )
    ]
)
async def test_get_elements(
    monkeypatch: pytest.MonkeyPatch,
    field_ids, kwargs, expected
):

    # get_elements takes 2 args, root and info and kwargs.
    # Root always seems to be none
    root = None
    # info is a graphql object that only gets used to pass on other
    # functions that I'm not testing
    info = None

    async def mock_return_list_elements(kwargs):
        return kwargs

    def mock_process_resolver_info(*args):
        return None, field_ids

    monkeypatch.setattr('cylc.uiserver.schema.list_elements',
                        mock_return_list_elements)
    monkeypatch.setattr('cylc.uiserver.schema.process_resolver_info',
                        mock_process_resolver_info)

    assert await get_elements(
        root,
        info,
        live=False,
        **kwargs
    ) == expected
