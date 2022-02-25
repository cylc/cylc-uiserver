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

"""GraphQL resolvers for use in data accessing and mutation of workflows."""

from getpass import getuser
import os
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_EXCEPTION
from copy import deepcopy
from functools import partial
from typing import Callable, Dict, List, Union
from subprocess import Popen, PIPE, DEVNULL
from types import SimpleNamespace

from graphql.language.base import print_ast

from cylc.flow.network.resolvers import BaseResolvers
from cylc.flow.data_store_mgr import WORKFLOW
from cylc.flow.exceptions import CylcError
from cylc.flow.workflow_files import init_clean


class InvalidSchemaOptionError(CylcError):
    ...


# show traceback from cylc commands
DEBUG = True


def snake_to_kebab(snake):
    """Convert snake_case text to --kebab-case text.

    Examples:
        >>> snake_to_kebab('foo_bar_baz')
        '--foo-bar-baz'
        >>> snake_to_kebab('')
        ''
        >>> snake_to_kebab(None)
        Traceback (most recent call last):
        TypeError: <class 'NoneType'>

    """
    if isinstance(snake, str):
        if not snake:
            return ''
        return f'--{snake.replace("_", "-")}'
    raise TypeError(type(snake))


def check_cylc_version(version):
    """Check the provided Cylc version is available on the CLI.

    Sets CYLC_VERSION=version and tests the result of cylc --version
    to make sure the requested version is installed and selectable via
    the CYLC_VERSION environment variable.
    """
    proc = Popen(
        ['cylc', '--version'],
        env={**os.environ, 'CYLC_VERSION': version},
        stdin=DEVNULL,
        stdout=PIPE,
        stderr=PIPE,
        text=True
    )
    ret = proc.wait(timeout=5)
    out, err = proc.communicate()
    return ret or out.strip() == version


def _build_cmd(cmd: List, args: Dict) -> List:
    """Add args to command.

    Args:
        cmd: A base command.
        args: Args to append to base command.

    Returns: An elaborated command.

    Examples:
        It adds one arg to a command:
            >>> _build_cmd(['foo', 'bar'], {'set_baz': 'qux'})
            ['foo', 'bar', '--set-baz', 'qux']

        It adds one integer arg to a command:
            >>> _build_cmd(['foo', 'bar'], {'set_baz': 42})
            ['foo', 'bar', '--set-baz', '42']

        It adds a list of the same arg to a command:
            >>> _build_cmd(['foo', 'bar'], {'set_baz': ['qux', 'quiz']})
            ['foo', 'bar', '--set-baz', 'qux', '--set-baz', 'quiz']

        It doesn't append args == False:
            >>> _build_cmd(['foo', 'bar'], {'set_baz': False})
            ['foo', 'bar']
    """
    for key, value in args.items():
        if value is False:
            # don't add binary flags
            continue
        key = snake_to_kebab(key)
        if not isinstance(value, list):
            if isinstance(value, int):
                # Any iteger items need converting to strings:
                value = str(value)
            value = [value]
        for item in value:
            cmd.append(key)
            if item is not True:
                # don't provide values for binary flags
                cmd.append(item)
    return cmd


def _schema_opts_to_api_opts(schema_opts: Dict) -> SimpleNamespace:
    """Convert Schema opts to api Opts

    Contains data SCHEMA_TO_API:
        A mapping of schema options to functions in the form:
        def func(schema_key, schema_value):
            return (option_key, option _value)

    Args:
        schema_opts: Opts as described by the schema.

    Returns:
        Namespace for use as options.

    TODO:
        So far only `cyle clean` has been added. It may become necessary
        to separate the SCHEMA_TO_API dict into GENERIC_SCHEMA_TO_API and
        <COMMAND>_SCHEMA_TO_API, and add a kwarg indicating which
        additional schema to use.

    question:
        convert to class?
    """
    SCHEMA_TO_API: Dict[str, Union[Callable, None]] = {
        'rm': lambda opt, value: ('rm_dirs', value),
        'local_only': None,
        'remote_only': None,
        'debug':
            lambda opt, value:
                ('verbosity', 2) if value is True else ('verbosity', 0),
        'no_timestamp': lambda opt, value: ('log_timestamp', not value),
    }
    api_opts = {}
    for opt, value in schema_opts.items():
        # All valid options should be in SCHEMA_TO_API:
        if opt not in SCHEMA_TO_API:
            raise InvalidSchemaOptionError(
                f'{opt} is not a valid option for Cylc Clean'
            )

        # If converter is callable, call it on opt, value,
        # else just copy them verbatim to api_opts
        converter = SCHEMA_TO_API[opt]
        if callable(converter):
            api_opt_name, api_opt_value = converter(opt, value)
            api_opts[api_opt_name] = api_opt_value
        else:
            api_opts[opt] = value

    return SimpleNamespace(**api_opts)


def clean(tokens, opts):
    """Run Cylc Clean using `cylc.flow.workflow_files` api.
    """
    # set remote timeout to 10 minutes.
    opts.timeout = 600
    init_clean(tokens.pop('workflow'), opts)
    return 'Workflow cleaned'


class Services:
    """Cylc services provided by the UI Server."""

    @staticmethod
    def _error(message):
        """Format error case response."""
        return [
            False,
            str(message)
        ]

    @staticmethod
    def _return(message):
        """Format success case response."""
        return [
            True,
            message
        ]

    @classmethod
    async def _run_cmd_in_procpoolexecutor(cls, func_, timeout=600):
        """Run a function in procpool executor.

        Deliberately agnostic of the function to be run.

        Args:
            func_: Callable to be run
            timeout: Number of seconds to wait.

        TODO:
            Consider extending this to work with a list of functions.
        """
        with ProcessPoolExecutor(max_workers=None) as executor:
            future = executor.submit(func_)
            # If no exception is raised this is the same as
            # `return_when=ALL_COMPLETED`:
            done, _ = wait(
                [future], timeout=timeout, return_when=FIRST_EXCEPTION
            )
        failed = [d for d in done if d.exception() is not None]
        done = list(done)
        if failed:
            return cls._error(failed[0].exception())
        return cls._return(done[0].result())

    @classmethod
    async def clean(cls, workflows, args, workflows_mgr, log):
        """Calls `cylc clean`."""
        response = []
        # get ready to run the command
        try:
            # build the command
            opts = _schema_opts_to_api_opts(args)

        except Exception as exc:
            # oh noes, something went wrong, send back confirmation
            return cls._error(exc)

        # clean each requested flow
        for tokens in workflows:
            clean_func = partial(clean, tokens, opts)
            await cls._run_cmd_in_procpoolexecutor([clean_func])

        # trigger a re-scan
        await workflows_mgr.update()
        return response

    @classmethod
    async def play(cls, workflows, args, workflows_mgr, log):
        """Calls `cylc play`."""
        response = []
        # get ready to run the command
        try:
            # check that the request cylc version is available
            cylc_version = None
            if 'cylc_version' in args:
                cylc_version = args['cylc_version']
                if not check_cylc_version(cylc_version):
                    return cls._error(
                        f'cylc version not available: {cylc_version}'
                    )
                args = dict(args)
                args.pop('cylc_version')

            # build the command
            cmd = ['cylc', 'play', '--color=never']
            cmd = cls._build_cmd(cmd, args)

        except Exception as exc:
            # oh noes, something went wrong, send back confirmation
            return cls._error(exc)
        # start each requested flow
        for tokens in workflows:
            try:
                if tokens['user'] and tokens['user'] != getuser():
                    return cls._error(
                        'Cannot start workflows for other users.'
                    )
                # Note: authorisation has already taken place.
                # add the workflow to the command
                cmd = [*cmd, tokens['workflow']]

                # get a representation of the command being run
                cmd_repr = ' '.join(cmd)
                if cylc_version:
                    cmd_repr = f'CYLC_VERSION={cylc_version} {cmd_repr}'
                log.info(f'$ {cmd_repr}')

                # run cylc run
                proc = Popen(
                    cmd,
                    stdin=DEVNULL,
                    stdout=PIPE,
                    stderr=PIPE,
                    text=True
                )
                ret = proc.wait(timeout=20)

                if ret:
                    # command failed
                    _, err = proc.communicate()
                    raise Exception(
                        f'Could not start {tokens["workflow"]} - {cmd_repr}'
                        # suppress traceback unless in debug mode
                        + (f' - {err}' if DEBUG else '')
                    )

            except Exception as exc:
                # oh noes, something went wrong, send back confirmation
                return cls._error(exc)

            else:
                # send a success message
                return cls._return(
                    'Workflow started'
                )
        # trigger a re-scan
        await workflows_mgr.update()
        return response


class Resolvers(BaseResolvers):
    """UI Server context GraphQL query and mutation resolvers."""

    workflows_mgr = None

    def __init__(self, data, log, **kwargs):
        super().__init__(data)
        self.log = log

        # Set extra attributes
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    # Mutations
    async def mutator(self, info, *m_args):
        """Mutate workflow."""
        req_meta = {}
        _, w_args, _, _ = m_args
        req_meta['auth_user'] = info.context.get(
            'current_user', 'unknown user')
        w_ids = [
            flow[WORKFLOW].id
            for flow in await self.get_workflows_data(w_args)]
        if not w_ids:
            return [{
                'response': (False, 'No matching workflows')}]
        # Pass the request to the workflow GraphQL endpoints
        _, variables, _, _ = info.context.get('graphql_params')

        # Create a modified request string,
        # containing only the current mutation/field.
        operation_ast = deepcopy(info.operation)
        operation_ast.selection_set.selections = info.field_asts

        graphql_args = {
            'request_string': print_ast(operation_ast),
            'variables': variables,
        }
        return await self.workflows_mgr.multi_request(
            'graphql', w_ids, graphql_args, req_meta=req_meta
        )

    async def service(self, info, *m_args):
        if m_args[0] == 'clean':
            return await Services.clean(
                m_args[1]['workflows'],
                m_args[2],
                self.workflows_mgr,
                log=self.log
            )
        else:
            return await Services.play(
                m_args[1]['workflows'],
                m_args[2],
                self.workflows_mgr,
                log=self.log
            )
