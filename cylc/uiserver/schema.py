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
"""GraphQL Schema.

This is a strict superset of the Cylc Flow schema that includes
extra functionality specific to the UIS.

"""

from functools import partial
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

import graphene
from graphene.types.generic import GenericScalar

from cylc.flow.id import Tokens
from cylc.flow.data_store_mgr import JOBS, TASKS
from cylc.flow.rundb import CylcWorkflowDAO
from cylc.flow.pathutil import get_workflow_run_dir
from cylc.flow.workflow_files import WorkflowFiles
from cylc.flow.network.schema import (
    NODE_MAP,
    CyclePoint,
    GenericResponse,
    SortArgs,
    Task,
    Job,
    Mutations,
    Queries,
    process_resolver_info,
    STRIP_NULL_DEFAULT,
    Subscriptions,
    WorkflowID,
    WorkflowRunMode as RunMode,
    _mut_field,
    get_nodes_all
)
from cylc.flow.task_state import (
    TASK_STATUS_FAILED,
    TASK_STATUS_RUNNING,
    TASK_STATUS_SUBMITTED,
    TASK_STATUS_SUBMIT_FAILED,
    TASK_STATUS_SUCCEEDED,
    TASK_STATUS_WAITING,
)
from cylc.flow.util import sstrip

from cylc.uiserver.resolvers import (
    Resolvers,
    list_log_files,
    stream_log,
)

if TYPE_CHECKING:
    from graphql import ResolveInfo


async def mutator(
    root: Optional[Any],
    info: 'ResolveInfo',
    *,
    command: str,
    workflows: Optional[List[str]] = None,
    **kwargs: Any
):
    """Call the resolver method that act on the workflow service
    via the internal command queue."""
    if workflows is None:
        workflows = []
    parsed_workflows = [Tokens(w_id) for w_id in workflows]
    if kwargs.get('args', False):
        kwargs.update(kwargs.get('args', {}))
        kwargs.pop('args')

    resolvers: 'Resolvers' = (
        info.context.get('resolvers')  # type: ignore[union-attr]
    )
    res = await resolvers.service(info, command, parsed_workflows, kwargs)
    return GenericResponse(result=res)


class CylcVersion(graphene.String):
    """A Cylc version identifier e.g. 8.0.0"""


class Play(graphene.Mutation):
    class Meta:
        description = sstrip('''
            Start, resume or restart a workflow run.

            Valid for: stopped workflows.
        ''')
        # Note we have the "resume" mutation for paused workflows.
        resolver = partial(mutator, command='play')

    class Arguments:
        workflows = graphene.List(WorkflowID, required=True)
        cylc_version = CylcVersion(
            description=sstrip('''
                Set the Cylc version that the workflow starts with.
            ''')
        )
        initial_cycle_point = CyclePoint(
            description=sstrip('''
                Set the initial cycle point.

                Required if not defined in flow.cylc.
            ''')
        )
        start_cycle_point = CyclePoint(
            description=sstrip('''
                Set the start cycle point, which may be after the initial
                cycle point.

                If the specified start point is not in the sequence, the next
                on-sequence point will be used.

                (Not to be confused with the initial cycle point).

                This replaces the Cylc 7 --warm option.
            ''')
        )
        final_cycle_point = CyclePoint(
            description=sstrip('''
                Set the final cycle point. This command line option overrides
                the workflow config option `[scheduling]final cycle point`.
            ''')
        )
        stop_cycle_point = CyclePoint(
            description=sstrip('''
                Set the stop cycle point. Shut down after all tasks have PASSED
                this cycle point. (Not to be confused with the final cycle
                point.) This command line option overrides the workflow config
                option `[scheduling]stop after cycle point`.
            ''')
        )
        pause = graphene.Boolean(
            description=sstrip('''
                Pause workflow immediately on starting.
            ''')
        )
        hold_cycle_point = CyclePoint(
            description=sstrip('''
                Hold all tasks after this cycle point.
            ''')
        )
        mode = RunMode(
            default_value=RunMode.Live.name
        )
        host = graphene.String(
            description=sstrip('''
                Specify the host on which to start-up the workflow. If not
                specified, a host will be selected using the
                `[scheduler]run hosts` global config.
            ''')
        )
        main_loop = graphene.List(
            graphene.String,
            description=sstrip('''
                Specify an additional plugin to run in the main loop. These
                are used in combination with those specified in
                `[scheduler][main loop]plugins`. Can be used multiple times.
            ''')
        )
        upgrade = graphene.Boolean(
            default_value=False,
            description=sstrip('''
                Allow the workflow to be restarted with a newer
                version of Cylc.
            ''')
        )
        abort_if_any_task_fails = graphene.Boolean(
            default_value=False,
            description=sstrip('''
                If set workflow will abort with status 1 if any task fails.
            ''')
        )
        debug = graphene.Boolean(
            default_value=False,
            description=sstrip('''
                Output developer information and show exception tracebacks.
            ''')
        )
        no_timestamp = graphene.Boolean(
            default_value=False,
            description=sstrip('''
                Don't timestamp logged messages.
            ''')
        )
        set = graphene.List(  # noqa: A003 (graphql field name)
            graphene.String,
            description=sstrip('''
                Set the value of a Jinja2 template variable in the workflow
                definition. Values should be valid Python literals so strings
                must be quoted e.g. `STR="string"`, `INT=43`, `BOOL=True`.
                This option can be used multiple  times on the command line.
                NOTE: these settings persist across workflow restarts, but can
                be set again on the `cylc play` command line if they need to be
                overridden.
            ''')
        )
        set_file = graphene.String(
            description=sstrip('''
                Set the value of Jinja2 template variables in the workflow
                definition from a file containing NAME=VALUE pairs (one per
                line). As with "set" values should be valid Python literals so
                strings must be quoted e.g.  `STR='string'`. NOTE: these
                settings persist across workflow restarts, but can be set again
                on the `cylc play` command line if they need to be overridden.
            ''')
        )

    result = GenericScalar()


class Clean(graphene.Mutation):
    class Meta:
        description = sstrip('''
            Clean a workflow from the run directory.

            Valid for: stopped workflows.
        ''')
        resolver = partial(mutator, command='clean')

    class Arguments:
        workflows = graphene.List(WorkflowID, required=True)
        rm = graphene.String(
            default_value='',
            description=sstrip('''
                Only clean the specified subdirectories or files in
                the run directory, rather than the whole run.

                A colon separated list that accepts globs,
                e.g. ``.service/db:log:share:work/2020*``.
            ''')
        )
        local_only = graphene.Boolean(
            default_value=False,
            description=sstrip('''
                Only clean on the local filesystem (not remote hosts).
            ''')
        )
        remote_only = graphene.Boolean(
            default_value=False,
            description=sstrip('''
                Only clean on remote hosts (not the local filesystem).
            ''')
        )

    result = GenericScalar()


class Scan(graphene.Mutation):
    class Meta:
        description = sstrip('''
            Scan the filesystem for file changes.

            Valid for: stopped workflows.
        ''')
        resolver = partial(mutator, command='scan')
    result = GenericScalar()


async def get_elements(query_type, root, info, **kwargs):
    if kwargs['live']:
        return await get_nodes_all(root, info, **kwargs)

    _, field_ids = process_resolver_info(root, info, kwargs)

    if field_ids:
        if isinstance(field_ids, str):
            field_ids = [field_ids]
        elif isinstance(field_ids, dict):
            field_ids = list(field_ids)
        kwargs['ids'] = field_ids
    elif field_ids == []:
        return []

    for arg in ('ids', 'exids'):
        # live objects can be represented by a universal ID
        kwargs[arg] = [Tokens(n_id, relative=True) for n_id in kwargs[arg]]
    kwargs['workflows'] = [
        Tokens(w_id) for w_id in kwargs['workflows']]
    kwargs['exworkflows'] = [
        Tokens(w_id) for w_id in kwargs['exworkflows']]

    return await list_elements(query_type, kwargs)


async def list_elements(query_type, args):
    if not args['workflows']:
        raise Exception('At least one workflow must be provided.')
    elements = []
    for workflow in args['workflows']:
        db_file = get_workflow_run_dir(
            workflow['workflow'],
            WorkflowFiles.LogDir.DIRNAME,
            "db"
        )
        with CylcWorkflowDAO(db_file, is_public=True) as dao:
            conn = dao.connect()
            if query_type == 'jobs':
                elements.extend(
                    run_jobs_query(
                        conn,
                        workflow,
                        ids=args.get('ids'),
                        exids=args.get('exids'),
                        states=args.get('states'),
                        exstates=args.get('exstates'),
                        tasks=args.get('tasks'),
                    )
                )
            else:
                elements.extend(run_task_query(conn, workflow))
    return elements


def run_task_query(conn, workflow):

    # TODO: support all arguments including states
    # https://github.com/cylc/cylc-uiserver/issues/440
    tasks = []
    total_of_totals = 0
    for row in conn.execute('''
WITH data AS (
  SELECT
    tj.name,
    tj.cycle,
    tj.submit_num,
    tj.submit_status,
    tj.time_run,
    tj.time_run_exit,
    tj.job_id,
    tj.platform_name,
    tj.time_submit,
    tj.run_status,
    te.message as max_rss,
    STRFTIME('%s', time_run_exit) - STRFTIME('%s', time_submit) AS total_time,
    STRFTIME('%s', time_run_exit) - STRFTIME('%s', time_run) AS run_time,
    STRFTIME('%s', time_run) - STRFTIME('%s', time_submit) AS queue_time
  FROM task_jobs tj
  LEFT JOIN task_events te ON tj.name = te.name AND tj.cycle = te.cycle
  AND tj.submit_num = te.submit_num
  WHERE te.message LIKE 'max_rss%'
),
data1 AS (
  SELECT *,
    te.message as cpu_time
  FROM data
  LEFT JOIN task_events te ON data.name = te.name AND data.cycle = te.cycle
  AND data.submit_num = te.submit_num
  WHERE te.message LIKE 'cpu_time%'
),
data2 AS (
  SELECT
    name,
    cycle,
    submit_num,
    submit_status,
    run_status,
    time_run,
    time_run_exit,
    job_id,
    platform_name,
    time_submit,
    queue_time,
    run_time,
    total_time,
    NTILE(4) OVER (PARTITION BY name ORDER BY queue_time)
    AS queue_time_quartile,
    NTILE(4) OVER (PARTITION BY name ORDER BY run_time)
    AS run_time_quartile,
    NTILE(4) OVER (PARTITION BY name ORDER BY total_time)
    AS total_time_quartile,
    NTILE(4) OVER (PARTITION BY name ORDER BY CAST
    (TRIM(REPLACE(max_rss, 'max_rss ', '')) AS INT)) AS max_rss_quartile,
    CAST(TRIM(REPLACE(max_rss, 'max_rss ', '')) AS INT) AS max_rss,
    NTILE(4) OVER (PARTITION BY name ORDER BY CAST
    (TRIM(REPLACE(cpu_time, 'cpu_time ', '')) AS INT)) AS cpu_time_quartile,
    CAST(TRIM(REPLACE(cpu_time, 'cpu_time ', '')) AS INT) AS cpu_time
  FROM data1
)
SELECT
  name,
  cycle,
  submit_num,
  submit_status,
  time_run,
  time_run_exit,
  job_id,
  platform_name,
  time_submit,

  -- Calculate Queue time stats
  MIN(queue_time) AS min_queue_time,
  CAST(AVG(queue_time) AS FLOAT) AS mean_queue_time,
  MAX(queue_time) AS max_queue_time,
  CAST(AVG(queue_time * queue_time) AS INT) AS mean_squares_queue_time,
  MAX(CASE WHEN queue_time_quartile = 1 THEN queue_time END)
  AS queue_quartile_1,
  MAX(CASE WHEN queue_time_quartile = 2 THEN queue_time END)
  AS queue_quartile_2,
  MAX(CASE WHEN queue_time_quartile = 3 THEN queue_time END)
  AS queue_quartile_3,

  -- Calculate Run time stats
  MIN(run_time) AS min_run_time,
  CAST(AVG(run_time) AS FLOAT) AS mean_run_time,
  MAX(run_time) AS max_run_time,
  CAST(AVG(run_time * run_time) AS INT) AS mean_squares_run_time,
  MAX(CASE WHEN run_time_quartile = 1 THEN run_time END) AS run_quartile_1,
  MAX(CASE WHEN run_time_quartile = 2 THEN run_time END) AS run_quartile_2,
  MAX(CASE WHEN run_time_quartile = 3 THEN run_time END) AS run_quartile_3,

  -- Calculate Total time stats
  MIN(total_time) AS min_total_time,
  CAST(AVG(total_time) AS FLOAT) AS mean_total_time,
  MAX(total_time) AS max_total_time,
  CAST(AVG(total_time * total_time) AS INT) AS mean_squares_total_time,
  MAX(CASE WHEN total_time_quartile = 1 THEN total_time END)
  AS total_quartile_1,
  MAX(CASE WHEN total_time_quartile = 2 THEN total_time END)
  AS total_quartile_2,
  MAX(CASE WHEN total_time_quartile = 3 THEN total_time END)
  AS total_quartile_3,

  -- Calculate RSS stats
  MIN(max_rss) AS min_max_rss,
  CAST(AVG(max_rss) AS INT) AS mean_max_rss,
  MAX(max_rss) AS max_max_rss,
  CAST(AVG(max_rss * max_rss) AS INT) AS mean_squares_max_rss,
  MAX(CASE WHEN max_rss_quartile = 1 THEN max_rss END) AS max_rss_quartile_1,
  MAX(CASE WHEN max_rss_quartile = 2 THEN max_rss END) AS max_rss_quartile_2,
  MAX(CASE WHEN max_rss_quartile = 3 THEN max_rss END) AS max_rss_quartile_3,

  -- Calculate CPU time
  MIN(cpu_time) AS min_cpu_time,
  CAST(AVG(cpu_time) AS INT) AS mean_cpu_time,
  MAX(cpu_time) AS max_cpu_time,
  CAST(TOTAL(cpu_time) AS INT) AS total_cpu_time,
  CAST(AVG(cpu_time * cpu_time) AS INT) AS mean_squares_cpu_time,
  MAX(CASE WHEN cpu_time_quartile = 1 THEN cpu_time END)
  AS cpu_time_quartile_1,
  MAX(CASE WHEN cpu_time_quartile = 2 THEN cpu_time END)
  AS cpu_time_quartile_2,
  MAX(CASE WHEN cpu_time_quartile = 3 THEN cpu_time END)
  AS cpu_time_quartile_3,

  COUNT(*) AS n
FROM data2
GROUP BY name;
'''):
        total_of_totals += row[40]
        tasks.append({
            'id': workflow.duplicate(
                cycle=row[1],
                task=row[0],
                job=row[2]
            ),
            'name': row[0],
            'cycle_point': row[1],
            'submit_num': row[2],
            'state': _state_to_status(row[3], row[4], row[5]),
            'started_time': row[4],
            'finished_time': row[5],
            'job_ID': row[6],
            'platform': row[7],
            'submitted_time': row[8],
            # Queue time stats
            'min_queue_time': row[9],
            'mean_queue_time': row[10],
            'max_queue_time': row[11],
            'std_dev_queue_time': (row[12] - row[10]**2)**0.5,
            # Prevents null entries when there are too few tasks for quartiles
            'queue_quartiles': [row[13],
                                row[13] if row[14] is None else row[14],
                                row[13] if row[15] is None else row[15]],
            # Run time stats
            'min_run_time': row[16],
            'mean_run_time': row[17],
            'max_run_time': row[18],
            'std_dev_run_time': (row[19] - row[17]**2)**0.5,
            # Prevents null entries when there are too few tasks for quartiles
            'run_quartiles': [row[20],
                              row[20] if row[21] is None else row[21],
                              row[20] if row[22] is None else row[22]],
            # Total
            'min_total_time': row[23],
            'mean_total_time': row[24],
            'max_total_time': row[25],
            'std_dev_total_time': (row[26] - row[24] ** 2) ** 0.5,
            # Prevents null entries when there are too few tasks for quartiles
            'total_quartiles': [row[27],
                                row[27] if row[28] is None else row[28],
                                row[27] if row[29] is None else row[29]],
            # Max RSS stats
            'min_max_rss': row[30],
            'mean_max_rss': row[31],
            'max_max_rss': row[32],
            'std_dev_max_rss': (row[33] - row[31] ** 2) ** 0.5,
            # Prevents null entries when there are too few tasks for quartiles
            'max_rss_quartiles': [row[34],
                                  row[34] if row[35] is None else row[35],
                                  row[34] if row[36] is None else row[36]],
            # CPU time stats
            'min_cpu_time': row[37],
            'mean_cpu_time': row[38],
            'max_cpu_time': row[39],
            'total_cpu_time': row[40],
            'std_dev_cpu_time': (row[41] - row[38] ** 2) ** 0.5,
            # Prevents null entries when there are too few tasks for quartiles
            'cpu_time_quartiles': [row[42],
                                   row[42] if row[43] is None else row[43],
                                   row[42] if row[44] is None else row[44]],
            'count': row[45]
        })

    for task in tasks:
        task['total_of_totals'] = total_of_totals
    return tasks


_JOB_STATUS_TO_STATE = {
    # task_status: (submit_status, run_status, time_run)
    TASK_STATUS_SUBMITTED: (0, None, None),
    TASK_STATUS_SUBMIT_FAILED: (1, None, None),
    TASK_STATUS_RUNNING: (0, None, True),
    TASK_STATUS_SUCCEEDED: (0, 0, True),
    TASK_STATUS_FAILED: (0, 1, True),
}


def _status_to_state(
    status: str
) -> Tuple[Optional[int], Optional[int], Optional[bool]]:
    """Derive job state attributes from job status.

    The time_run cannot be derived from the status so is returned as a boolean.

    Args:
        status: The job status, e.g. "submitted" or "running".

    Returns:
        (submit_status, run_status, time_run)

        submit_status:
            * 0 = successful submission
            * int = failed submission
            * None = no submission attempt
        run_status:
            * 0 = successful execution
            * int = failed execution
            * None = no execution attempt
        time_run:
            * True if the job would have started running

    Examples:
        >>> _status_to_state('running')
        (0, None, True)
        >>> _status_to_state('waiting')
        (None, None, None)

        >>> _state_to_status(*_status_to_state('succeeded'))
        'succeeded'

    """
    return _JOB_STATUS_TO_STATE.get(status, (None, None, None))


def _state_to_status(
    submit_status: Optional[int],
    run_status: Optional[int],
    time_run: Optional[str],
) -> str:
    """Derive job status from state attributes.

    Args:
        submit_status: Exit code from job submission.
        run_status: Exit code from job execution.
        time_run: The time the job reported that it started running.
            (note this is interpreted as a bool, the exact value is ignored).

    Returns:
        status: The job status, e.g "submitted" or "running".

    Examples:
        >>> _state_to_status(0, None, True)
        'running'
        >>> _state_to_status(None, None, None)
        'waiting'

        >>> _status_to_state(_state_to_status(0, 1, True))
        (0, 1, True)

    """
    if run_status is not None:
        if run_status == 0:
            status = TASK_STATUS_SUCCEEDED
        else:
            status = TASK_STATUS_FAILED
    elif time_run is not None:
        status = TASK_STATUS_RUNNING
    elif submit_status is not None:
        if submit_status == 0:
            status = TASK_STATUS_SUBMITTED
        else:
            status = TASK_STATUS_SUBMIT_FAILED
    else:
        status = TASK_STATUS_WAITING

    return status


def run_jobs_query(
    conn,
    workflow,
    ids=None,
    exids=None,
    states=None,
    exstates=None,
    tasks=None,
):
    """Query jobs from the database.

    Args:
        conn: Database connection.
        workflow: Workflow ID.
        kwargs: GraphQL sort/filter args as per cylc-flow interfaces.

    """
    # TODO: support all arguments:
    # * [x] ids
    # * [ ] sort
    # * [x] exids
    # * [x] states
    # * [x] exstates
    # See https://github.com/cylc/cylc-uiserver/issues/440
    jobs = []
    where_stmts = []
    where_args = []

    # filter by cycle/task/job ID
    if ids:
        items = []
        for id_ in ids:
            item = []
            for token, column in (
                ('cycle', 'cycle'),
                ('task', 'name'),
                ('job', 'submit_num'),
            ):
                value = id_[token]
                if value:
                    if token == 'job':
                        value = int(value)
                    item.append(rf'{column} GLOB ?')
                    where_args.append(value)
            items.append(rf'({" AND ".join(item)})')

        if items:
            where_stmts.append(
                r'(' + ' OR '.join(items) + ')'
            )

    # filter out cycle/task/job IDs
    if exids:
        for id_ in exids:
            items = []
            for token, column in (
                ('cycle', 'cycle'),
                ('task', 'name'),
                ('job', 'submit_num'),
            ):
                value = id_[token]
                if value:
                    if token == 'job':
                        value = int(value)
                    items.append(rf'{column} GLOB ?')
                    where_args.append(value)
            if items:
                where_stmts.append(r'NOT (' + ' AND '.join(items) + r')')

    # filter by job state
    if states:
        items = []
        for status in states:
            submit_status, run_status, time_run = _status_to_state(status)
            if submit_status is None:
                # hasn't yet submitted (i.e. there is no job)
                continue
            item = [r'IFNULL(submit_status,999) = ?']
            where_args.append(submit_status)

            if run_status is None:
                item.append('run_status IS NULL')
            else:
                item.append(r'IFNULL(run_status,999) = ?')
                where_args.append(run_status)

            if time_run is None:
                item.append(r'time_run IS NULL')
            else:
                item.append(r'time_run NOT NULL')

            items.append(r'(' + ' AND '.join(item) + r')')

        if items:
            where_stmts.append(r'(' + r' OR '.join(items) + r')')

    # filter out job states
    if exstates:
        for status in exstates:
            submit_status, run_status, time_run = _status_to_state(status)
            if submit_status is None:
                # hasn't yet submitted (i.e. there is no job)
                continue
            item = [r'IFNULL(submit_status,999) = ?']
            where_args.append(submit_status)

            if run_status is None:
                item.append(r'run_status IS NULL')
            else:
                item.append(r'IFNULL(run_status,999) = ?')
                where_args.append(run_status)

            if time_run is None:
                item.append(r'time_run IS NULL')
            else:
                item.append(r'time_run NOT NULL')

            where_stmts.append(r'NOT (' + ' AND '.join(item) + r')')

    # filter by task name (special UIS argument for namespace queries)
    if tasks:
        where_stmts.append(
            r'(data.name = '
            + r" OR data.name = ".join('?' for task in tasks)
            + r')'
        )
        where_args.extend(tasks)

    # build the SQL query
    query = r'''
        WITH data AS (
        SELECT *,
            CAST(REPLACE(te.message, 'max_rss ', '') AS INT) AS max_rss
        FROM
            task_jobs tj
        LEFT JOIN
            task_events te ON tj.name = te.name AND tj.cycle = te.cycle AND
            tj.submit_num = te.submit_num AND te.message LIKE 'max_rss%'
        WHERE
            tj.run_status = 0)
            
        SELECT
            data.name,
            data.cycle,
            data.submit_num,
            data.submit_status,
            data.time_run,
            data.time_run_exit,
            data.job_id,
            data.platform_name,
            data.time_submit,
            STRFTIME('%s', data.time_run_exit) - STRFTIME('%s', data.time_submit)
                AS total_time,
            STRFTIME('%s', data.time_run_exit) - STRFTIME('%s', data.time_run)
                AS run_time,
            STRFTIME('%s', data.time_run) - STRFTIME('%s', data.time_submit)
                AS queue_time,
            data.max_rss,
            CAST(REPLACE(te.message, 'cpu_time ', '') AS INT) AS cpu_time
            
        FROM data
        LEFT JOIN task_events te ON data.name = te.name AND
        data.cycle = te.cycle AND data.submit_num = te.submit_num
        WHERE te.message LIKE 'cpu_time%'
        '''
    if where_stmts:
        query += 'AND\n            ' + '\n            AND '.join(where_stmts)
    for row in conn.execute(query, where_args):
        # determine job status
        submit_status, run_status, time_run = row[3], row[12], row[4]
        status = _state_to_status(submit_status, run_status, time_run)

        # skip jobs that have not yet submitted
        if status == TASK_STATUS_WAITING:
            continue

        jobs.append({
            'id': workflow.duplicate(
                cycle=row[1],
                task=row[0],
                job=row[2]
            ),
            'name': row[0],
            'cycle_point': row[1],
            'submit_num': row[2],
            'state': status,
            'started_time': row[4],
            'finished_time': row[5],
            'job_ID': row[6],
            'platform': row[7],
            'submitted_time': row[8],
            'total_time': row[9],
            'run_time': row[10],
            'queue_time': row[11],
            'max_rss': row[12],
            'cpu_time': row[13]
        })

    return jobs


class UISTask(Task):

    platform = graphene.String()

    min_total_time = graphene.Int()
    mean_total_time = graphene.Int()
    max_total_time = graphene.Int()
    std_dev_total_time = graphene.Int()
    total_quartiles = graphene.List(
        graphene.Int,
        description=sstrip('''
                List containing the first, second,
                third and forth quartile total times.'''))
    min_queue_time = graphene.Int()
    mean_queue_time = graphene.Int()
    max_queue_time = graphene.Int()
    std_dev_queue_time = graphene.Int()
    queue_quartiles = graphene.List(
        graphene.Int,
        description=sstrip('''
            List containing the first, second,
            third and forth quartile queue times.'''))
    min_run_time = graphene.Int()
    mean_run_time = graphene.Int()
    max_run_time = graphene.Int()
    std_dev_run_time = graphene.Int()
    run_quartiles = graphene.List(
        graphene.Int,
        description=sstrip('''
                List containing the first, second,
                third and forth quartile run times.'''))
    max_rss = graphene.String()
    min_max_rss = graphene.Int()
    mean_max_rss = graphene.Int()
    max_max_rss = graphene.Int()
    std_dev_max_rss = graphene.Int()
    max_rss_quartiles = graphene.List(
        graphene.Int,
        description=sstrip('''
                List containing the first, second,
                third and forth quartile for Max RSS.'''))
    min_cpu_time = graphene.Int()
    mean_cpu_time = graphene.Int()
    max_cpu_time = graphene.Int()
    total_cpu_time = graphene.Int()
    std_dev_cpu_time = graphene.Int()
    cpu_time_quartiles = graphene.List(
        graphene.Int,
        description=sstrip('''
                List containing the first, second,
                third and forth quartile for CPU time.'''))
    total_of_totals = graphene.Int()
    count = graphene.Int()


class UISJob(Job):

    total_time = graphene.Int()
    queue_time = graphene.Int()
    run_time = graphene.Int()
    max_rss = graphene.Int()
    cpu_time = graphene.Int()


class UISQueries(Queries):

    class LogFiles(graphene.ObjectType):
        # Example GraphiQL query:
        # {
        #    logFiles(workflowID: "<workflow_id>", task: "<task_id>") {
        #      files
        #    }
        # }
        files = graphene.List(graphene.String)

    log_files = graphene.Field(
        LogFiles,
        description='List available job logs',
        id=graphene.Argument(
            graphene.ID,
            description='workflow//[cycle/task]',
            required=True,
        ),
        resolver=list_log_files
    )

    tasks = graphene.List(
        UISTask,
        description=Task._meta.description,
        live=graphene.Boolean(default_value=True),
        strip_null=STRIP_NULL_DEFAULT,
        resolver=partial(get_elements, 'tasks'),
        workflows=graphene.List(graphene.ID, default_value=[]),
        exworkflows=graphene.List(graphene.ID, default_value=[]),
        ids=graphene.List(graphene.ID, default_value=[]),
        exids=graphene.List(graphene.ID, default_value=[]),
        mindepth=graphene.Int(default_value=-1),
        maxdepth=graphene.Int(default_value=-1),
        sort=SortArgs(default_value=None),

    )

    jobs = graphene.List(
        UISJob,
        description=Job._meta.description,
        live=graphene.Boolean(default_value=True),
        strip_null=STRIP_NULL_DEFAULT,
        resolver=partial(get_elements, 'jobs'),
        workflows=graphene.List(graphene.ID, default_value=[]),
        exworkflows=graphene.List(graphene.ID, default_value=[]),
        ids=graphene.List(graphene.ID, default_value=[]),
        exids=graphene.List(graphene.ID, default_value=[]),
        mindepth=graphene.Int(default_value=-1),
        maxdepth=graphene.Int(default_value=-1),
        sort=SortArgs(default_value=None),
        tasks=graphene.List(
            graphene.ID,
            default_value=[],
            description='Deprecated, use ids: ["*/<task>"].',
        ),
        states=graphene.List(graphene.ID, default_value=[]),
        exstates=graphene.List(graphene.ID, default_value=[]),
    )


class UISSubscriptions(Subscriptions):
    # Example graphiql workflow log subscription:
    # subscription {
    #   logs(workflow: "foo") {
    #     lines
    #   }
    # }

    class Logs(graphene.ObjectType):
        lines = graphene.List(graphene.String)
        connected = graphene.Boolean()
        path = graphene.String()
        error = graphene.String()

    logs = graphene.Field(
        Logs,
        description='Workflow & job logs',
        id=graphene.Argument(
            graphene.ID,
            description='workflow//[cycle/task[/job]]',
            required=True,
        ),
        file=graphene.Argument(
            graphene.String,
            required=False,
            description='File name of job log to fetch, e.g. job.out'
        ),
        resolver=stream_log
    )


class UISMutations(Mutations):
    play = _mut_field(Play)
    clean = _mut_field(Clean)
    scan = _mut_field(Scan)


# Add UIS types to the cylc-flow backend:
NODE_MAP.update(
    UISTask=TASKS,
    UISJob=JOBS,
)

schema = graphene.Schema(
    query=UISQueries,
    subscription=UISSubscriptions,
    mutation=UISMutations
)
