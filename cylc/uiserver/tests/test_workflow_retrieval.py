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

from cylc.flow.id import Tokens
from cylc.uiserver.schema import make_query

'''This file tests the ability for the cylc UI to retrieve workflow information
and perform simple statistical calculations for the analysis tab'''


def test_make_query_1():
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

    return_value = make_query(conn, workflow)

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


def test_make_query_2():
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

    return_value = make_query(conn, workflow)

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


def test_make_query_3():
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

    return_value = make_query(conn, workflow)

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
