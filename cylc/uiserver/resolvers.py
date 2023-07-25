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

import asyncio
from contextlib import suppress
import errno
from getpass import getuser
import os
from copy import deepcopy
import signal
from subprocess import Popen, PIPE, DEVNULL
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    TYPE_CHECKING,
    Tuple,
    Union,
)

from graphql.language.base import print_ast
import psutil

from cylc.flow.data_store_mgr import WORKFLOW
from cylc.flow.exceptions import (
    ServiceFileError,
    WorkflowFilesError,
)
from cylc.flow.id import Tokens
from cylc.flow.network.resolvers import BaseResolvers
from cylc.flow.scripts.clean import CleanOptions
from cylc.flow.scripts.clean import run

if TYPE_CHECKING:
    from concurrent.futures import Executor
    from logging import Logger
    from optparse import Values
    from graphql import ResolveInfo
    from cylc.flow.data_store_mgr import DataStoreMgr
    from cylc.flow.option_parsers import Options
    from cylc.uiserver.workflows_mgr import WorkflowsManager


# show traceback from cylc commands
DEBUG = True
OPT_CONVERTERS: Dict['Options', Dict[
    str, Callable[[object], Tuple[str, object]]
]] = {
    CleanOptions: {
        'rm': lambda value: ('rm_dirs', [value] if value else None),
    }
}

# the maximum number of log lines to yield before truncating the file
MAX_LINES = 5000

ENOENT_MSG = os.strerror(errno.ENOENT)


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

        It doesn't add boolean values, just the switch
            >>> _build_cmd(['foo', 'bar'], {'set_baz': True})
            ['foo', 'bar', '--set-baz']
    """
    for key, value in args.items():
        if value is False:
            # don't add binary flags
            continue
        key = snake_to_kebab(key)
        if not isinstance(value, list):
            if isinstance(value, int) and not isinstance(value, bool):
                # Any integer items need converting to strings:
                value = str(value)
            value = [value]
        for item in value:
            cmd.append(key)
            if item is not True:
                # don't provide values for binary flags
                cmd.append(item)
    return cmd


def process_cat_log_stderr(text: bytes) -> str:
    """Tidy up cylc cat-log stderr.

    If ENOENT message is present in stderr, just return that, because
    stderr may be full of other crud.
    """
    msg = text.decode()
    return (
        ENOENT_MSG if ENOENT_MSG in msg
        else msg.strip()
    )


def _schema_opts_to_api_opts(
    schema_opts: Dict, schema: 'Options'
) -> 'Values':
    """Convert Schema opts to api Opts

    Contains data SCHEMA_TO_API:
        A mapping of schema options to functions in the form:
        def func(schema_key, schema_value):
            return (option_key, option _value)

    Args:
        schema_opts: Opts as described by the schema.
        schema: Schema for conversion - used to select
            converter functions from SCHEMA_TO_API.

    Returns:
        Namespace for use as options.
    """
    converters = OPT_CONVERTERS[schema]
    api_opts = {}
    for opt, value in schema_opts.items():
        # If option has a converter, call it with the value,
        # else just copy verbatim to api_opts
        converter = converters.get(opt)
        if converter is not None:
            api_opt_name, api_opt_value = converter(value)
            api_opts[api_opt_name] = api_opt_value
        else:
            api_opts[opt] = value
    return schema(**api_opts)


def _clean(workflow_ids, opts):
    """Helper function to call `cylc clean`.

    Execute this function inside of an "executor" (note this is why we have
    to set up asyncio here).
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(
        run(*workflow_ids, opts=opts)
    )


class Services:
    """Cylc services provided by the UI Server."""

    @staticmethod
    def _error(message: Union[Exception, str]):
        """Format error case response."""
        return [
            False,
            str(message)
        ]

    @staticmethod
    def _return(message: str):
        """Format success case response."""
        return [
            True,
            message
        ]

    @classmethod
    async def clean(
        cls,
        workflows: Iterable['Tokens'],
        args: dict,
        workflows_mgr: 'WorkflowsManager',
        executor: 'Executor',
        log: 'Logger'
    ):
        """Calls `cylc clean`"""
        # Convert Schema options → cylc.flow.workflow_files.init_clean opts:
        opts = _schema_opts_to_api_opts(args, schema=CleanOptions)
        opts.remote_timeout = "600"  # Hard set remote timeout.
        opts.skip_interactive = True  # disable interactive prompts

        # Convert tokens into string IDs
        workflow_ids = [tokens.workflow_id for tokens in workflows]

        # run cylc clean
        log.info(f'Cleaning {" ".join(workflow_ids)}')
        try:
            await asyncio.get_event_loop().run_in_executor(
                executor, _clean, workflow_ids, opts
            )
        except Exception as exc:
            if isinstance(exc, ServiceFileError):  # Expected error
                # The "workflow still running" msg is very long
                msg = str(exc).split('\n')[0]
            elif isinstance(exc, WorkflowFilesError):  # Expected error
                msg = str(exc)
            else:  # Unexpected error
                msg = f"{type(exc).__name__}: {exc}"
                log.exception(msg)
            return cls._error(msg)

        # trigger a re-scan
        await workflows_mgr.scan()
        return cls._return("Workflow(s) cleaned")

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
            cmd = _build_cmd(cmd, args)

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
        await workflows_mgr.scan()
        return response

    @staticmethod
    async def enqueue(stream, queue):
        async for line in stream:
            await queue.put(line.decode())

    @classmethod
    async def cat_log(cls, id_: Tokens, log, info, file=None):
        """Calls `cat log`.

        Used for log subscriptions.
        """
        cmd: List[str] = [
            'cylc',
            'cat-log',
            '--mode=tail',
            '--force-remote',
            '--prepend-path',
            id_.id,
        ]
        if file:
            cmd += ['-f', file]
        log.info(f'$ {" ".join(cmd)}')

        # For info, below subprocess is safe (uses shell=false by default)
        proc = await asyncio.subprocess.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        buffer: List[str] = []
        queue: asyncio.Queue = asyncio.Queue()
        # Farm out reading from stdout stream to a background task
        # This is to get around problem where stream is not EOF until
        # subprocess ends
        enqueue_task = asyncio.create_task(cls.enqueue(proc.stdout, queue))
        op_id = info.root_value
        line_count = 0
        try:
            while info.context['sub_statuses'].get(op_id) != 'stop':
                if queue.empty():
                    if buffer:
                        yield {'lines': list(buffer)}
                        buffer.clear()
                    if proc.returncode is not None:
                        (_, stderr) = await proc.communicate()
                        # pass any error onto ui
                        msg = process_cat_log_stderr(stderr) or (
                            f"cylc cat-log exited {proc.returncode}"
                        )
                        yield {'error': msg}
                        break
                    # sleep set at 1, which matches the `tail` default interval
                    await asyncio.sleep(1)
                else:
                    if line_count > MAX_LINES:
                        yield {'lines': buffer}
                        yield {
                            'error': (
                                'This file has been truncated because'
                                f' it is over {MAX_LINES} lines long.'
                            )
                        }
                        break
                    elif line_count == 0:
                        line_count += 1
                        yield {
                            'connected': True,
                            'path': (await queue.get())[2:].strip(),
                        }
                        continue
                    line = await queue.get()
                    line_count += 1
                    buffer.append(line)
                    if len(buffer) >= 75:
                        yield {'lines': list(buffer)}
                        buffer.clear()
                        await asyncio.sleep(0)
        finally:
            kill_process_tree(proc.pid)
            enqueue_task.cancel()
            with suppress(asyncio.CancelledError):
                await enqueue_task
            yield {'connected': False}

    @classmethod
    async def cat_log_files(cls, id_: Tokens):
        """Calls cat log to get list of available log files.

        Note kept separate from the cat_log method above as this is a one off
        query rather than a process held open for subscription.
        This uses the Cylc cat-log interface, list dir mode, forcing remote
        file checking.
        """
        cmd: List[str] = ['cylc', 'cat-log', '-m', 'l', '-o', id_.id]
        proc_job = await asyncio.subprocess.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # wait for proc to finish
        await proc_job.wait()

        # MOTD returned in stderr, no use in returning
        out_job, _ = await proc_job.communicate()
        if out_job:
            return sorted(
                # return the log files in reverse sort order
                # this means that the most recent log file rotations
                # will be at the top of the list
                out_job.decode().splitlines(),
                reverse=True,
            )
        else:
            return []


class Resolvers(BaseResolvers):
    """UI Server context GraphQL query and mutation resolvers."""

    def __init__(
        self,
        data: 'DataStoreMgr',
        log: 'Logger',
        workflows_mgr: 'WorkflowsManager',
        executor,
        **kwargs
    ):
        super().__init__(data)
        self.log = log
        self.workflows_mgr = workflows_mgr
        self.executor = executor

        # Set extra attributes
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    # Mutations
    async def mutator(
        self,
        info: 'ResolveInfo',
        command: str,
        w_args: Dict[str, Any],
        _kwargs: Dict[str, Any],
        _meta: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Mutate workflow."""
        req_meta = {
            'auth_user': info.context.get(  # type: ignore[union-attr]
                'current_user', 'unknown user'
            )
        }
        w_ids = [
            flow[WORKFLOW].id
            for flow in await self.get_workflows_data(w_args)]
        if not w_ids:
            return [{
                'response': (False, 'No matching workflows')}]
        # Pass the request to the workflow GraphQL endpoints
        _, variables, _, _ = info.context.get(  # type: ignore[union-attr]
            'graphql_params'
        )
        # Create a modified request string,
        # containing only the current mutation/field.
        operation_ast = deepcopy(info.operation)
        operation_ast.selection_set.selections = info.field_asts

        graphql_args = {
            'request_string': print_ast(operation_ast),
            'variables': variables,
        }
        return await self.workflows_mgr.multi_request(  # type: ignore # TODO
            'graphql', w_ids, graphql_args, req_meta=req_meta
        )

    async def service(
        self,
        info: 'ResolveInfo',
        command: str,
        workflows: Iterable['Tokens'],
        kwargs: Dict[str, Any]
    ) -> List[Union[bool, str]]:
        if command == 'clean':
            return await Services.clean(
                workflows,
                kwargs,
                self.workflows_mgr,
                log=self.log,
                executor=self.executor
            )

        elif command == 'play':
            return await Services.play(
                workflows,
                kwargs,
                self.workflows_mgr,
                log=self.log
            )

        raise NotImplementedError()

    async def subscription_service(
        self,
        info: 'ResolveInfo',
        _command: str,
        ids: List[Tokens],
        file=None
    ):
        async for ret in Services.cat_log(
            ids[0],
            self.log,
            info,
            file
        ):
            yield ret

    async def query_service(
        self,
        id_: Tokens,
    ):
        return await Services.cat_log_files(id_)


def kill_process_tree(
    pid,
    sig=signal.SIGTERM,
    include_parent=True,
):
    """Kill an entire process tree.

    Args:
        pid: The parent process ID to kill.
        sig: The signal to send to the processes in this tree.
        include_parent: Also kill the parent process (pid).

    """
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        with suppress(psutil.NoSuchProcess):
            p.send_signal(sig)


async def list_log_files(
    root: Optional[Any],
    info: 'ResolveInfo',
    id: str,  # noqa: required to match schema arg name
):
    tokens = Tokens(id)
    resolvers: 'Resolvers' = (
        info.context.get('resolvers')  # type: ignore[union-attr]
    )
    files = await resolvers.query_service(tokens)
    return {'files': files}


async def stream_log(
    root: Optional[Any],
    info: 'ResolveInfo',
    *,
    command='cat_log',
    id: str,  # noqa: required to match schema arg name
    file=None,
    **kwargs: Any,
) -> AsyncGenerator[Any, None]:
    """Cat Log Resolver
    Expands workflow provided subscription query.
    """
    tokens = Tokens(id)
    if kwargs.get('args', False):
        kwargs.update(kwargs.get('args', {}))
        kwargs.pop('args')
    resolvers: 'Resolvers' = (
        info.context.get('resolvers')  # type: ignore[union-attr]
    )
    async for item in resolvers.subscription_service(
        info,
        command,
        [tokens],
        file
    ):
        yield item
