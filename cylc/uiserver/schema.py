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

from graphene import (
    Boolean,
    Enum,
    List,
    Mutation,
    Schema,
    String,
)
from graphene.types.generic import GenericScalar

from cylc.flow.id import Tokens
from cylc.flow.network.schema import (
    CyclePoint,
    GenericResponse,
    Mutations,
    Queries,
    Subscriptions,
    WorkflowID,
    _mut_field,
    sstrip,
)


async def mutator(root, info, command=None, workflows=None,
                  exworkflows=None, **args):
    """Call the resolver method that act on the workflow service
    via the internal command queue."""
    if workflows is None:
        workflows = []
    if exworkflows is None:
        exworkflows = []
    w_args = {
        'workflows': [Tokens(w_id) for w_id in workflows],
        'exworkflows': [Tokens(w_id) for w_id in exworkflows],
    }
    if args.get('args', False):
        args.update(args.get('args', {}))
        args.pop('args')

    resolvers = info.context.get('resolvers')
    res = await resolvers.service(info, command, w_args, args)
    return GenericResponse(result=res)


class RunMode(Enum):
    """The mode to run a workflow in."""

    Live = 'live'
    Dummy = 'dummy'
    DummyLocal = 'dummy-local'
    Simulation = 'simulation'

    @property
    def description(self):
        if self == RunMode.Live:
            return 'The normal default run mode'
        if self == RunMode.Dummy:
            return 'Replaces all *-script items with nothing'
        if self == RunMode.DummyLocal:
            return (
                'Replaces all *-script items with nothing and sets'
                ' platform = localhost for all tasks.'
            )
        if self == RunMode.Simulation:
            return 'Simulates job submission, does not run anything at all.'


class CylcVersion(String):
    """A Cylc version identifier e.g. 8.0.0"""


class Play(Mutation):
    class Meta:
        description = sstrip('''
            Start, resume or un-pause a workflow run.
        ''')
        resolver = partial(mutator, command='play')

    class Arguments:
        workflows = List(WorkflowID, required=True)
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
                Set the start cycle point, which may be after the initial cycle
                point.

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
        pause = Boolean(
            description=sstrip('''
                Pause workflow immediately on starting.
            ''')
        )
        hold_cycle_point = CyclePoint(
            description=sstrip('''
                Hold all tasks after this cycle point.
            ''')
        )
        mode = RunMode()
        host = String(
            description=sstrip('''
                Specify the host on which to start-up the workflow. If not
                specified, a host will be selected using the
                `[scheduler]run hosts` global config.
            ''')
        )
        main_loop = List(
            String,
            description=sstrip('''
                Specify an additional plugin to run in the main loop. These
                are used in combination with those specified in
                `[scheduler][main loop]plugins`. Can be used multiple times.
            ''')
        )
        abort_if_any_task_fails = Boolean(
            default_value=False,
            description=sstrip('''
                If set workflow will abort with status 1 if any task fails.
            ''')
        )
        debug = Boolean(
            default_value=False,
            description=sstrip('''
                Output developer information and show exception tracebacks.
            ''')
        )
        no_timestamp = Boolean(
            default_value=False,
            description=sstrip('''
                Don't timestamp logged messages.
            ''')
        )
        set = List(  # noqa: A003 (graphql field name)
            String,
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
        set_file = String(
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


class UISMutations(Mutations):

    play = _mut_field(Play)


schema = Schema(
    query=Queries,
    subscription=Subscriptions,
    mutation=UISMutations
)
