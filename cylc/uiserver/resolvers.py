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
import errno
import os
import signal
from contextlib import suppress
from copy import deepcopy
from getpass import getuser
from subprocess import (
    DEVNULL,
    PIPE,
    Popen,
)
from time import time
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

import psutil
from cylc.flow.data_store_mgr import WORKFLOW
from cylc.flow.exceptions import ServiceFileError, WorkflowFilesError
from cylc.flow.id import Tokens
from cylc.flow.network.resolvers import BaseResolvers
from cylc.flow.scripts.clean import CleanOptions, run
from graphql.language.base import print_ast

if TYPE_CHECKING:
    from concurrent.futures import Executor
    from logging import Logger
    from optparse import Values

    from cylc.flow.data_store_mgr import DataStoreMgr
    from cylc.flow.option_parsers import Options
    from graphql import ResolveInfo

    from cylc.uiserver.app import CylcUIServer
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

    # log file stream lag
    CAT_LOG_SLEEP = 1

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
    async def scan(
        cls,
        args: dict,
        workflows_mgr: 'WorkflowsManager',
    ):
        await workflows_mgr.scan()
        return cls._return("Scan requested")

    @classmethod
    async def play(
        cls,
        workflows: Iterable[Tokens],
        args: Dict[str, Any],
        workflows_mgr: 'WorkflowsManager',
        log: 'Logger',
    ) -> List[Union[bool, str]]:
        """Calls `cylc play`."""
        cylc_version = args.pop('cylc_version', None)
        results: Dict[str, str] = {}
        failed = False
        for tokens in workflows:
            try:
                cmd = _build_cmd(['cylc', 'play', '--color=never'], args)

                if tokens['user'] and tokens['user'] != getuser():
                    return cls._error(
                        'Cannot start workflows for other users.'
                    )
                # Note: authorisation has already taken place.
                # add the workflow to the command
                wflow: str = tokens['workflow']
                cmd = [*cmd, wflow]

                # get a representation of the command being run
                cmd_repr = ' '.join(cmd)
                if cylc_version:
                    cmd_repr = f'CYLC_VERSION={cylc_version} {cmd_repr}'
                log.info(f'$ {cmd_repr}')

                env = os.environ.copy()
                if cylc_version:
                    env.pop('CYLC_ENV_NAME', None)
                    env['CYLC_VERSION'] = cylc_version

                # run cylc play
                proc = Popen(
                    cmd,
                    env=env,
                    stdin=DEVNULL,
                    stdout=PIPE,
                    stderr=PIPE,
                    text=True
                )
                ret_code = proc.wait(timeout=120)

                if ret_code:
                    # command failed
                    out, err = proc.communicate()
                    results[wflow] = err.strip() or out.strip() or (
                        f'Command failed ({ret_code}): {cmd_repr}'
                    )
                    failed = True
                else:
                    results[wflow] = 'started'

            except Exception as exc:
                # oh noes, something went wrong, send back confirmation
                return cls._error(exc)

        if failed:
            if len(results) == 1:
                return cls._error(results.popitem()[1])
            # else log each workflow result on separate lines
            return cls._error(
                "\n\n" + "\n\n".join(
                    f"{wflow}: {msg}" for wflow, msg in results.items()
                )
            )

        # trigger a re-scan
        await workflows_mgr.scan()
        # send a success message
        return cls._return('Workflow(s) started')

    @staticmethod
    async def enqueue(stream, queue):
        async for line in stream:
            await queue.put(line.decode())

    @classmethod
    async def cat_log(cls, id_: Tokens, app: 'CylcUIServer', info, file=None):
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
        app.log.info(f'$ {" ".join(cmd)}')

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

        # GraphQL operation ID
        op_id = info.root_value

        # track the number of lines received so far
        line_count = 0

        # the time we started the cylc cat-log process
        start_time = time()

        # configured cat-log process timeout
        timeout = float(app.log_timeout)

        try:
            while info.context['sub_statuses'].get(op_id) != 'stop':
                if time() - start_time > timeout:
                    # timeout exceeded -> kill the cat-log process
                    break

                if queue.empty():
                    # there are *no* lines to read from the cat-log process
                    if buffer:
                        # yield everything in the buffer
                        yield {'lines': list(buffer)}
                        buffer.clear()

                    if proc.returncode is not None:
                        # process exited
                        # -> pass any stderr text to the client
                        (_, stderr) = await proc.communicate()
                        msg = process_cat_log_stderr(stderr) or (
                            f"cylc cat-log exited {proc.returncode}"
                        )
                        yield {'error': msg}

                        # stop reading log lines
                        break

                    # sleep set at 1, which matches the `tail` default interval
                    await asyncio.sleep(cls.CAT_LOG_SLEEP)

                else:
                    # there *are* lines to read from the cat-log process
                    if line_count > MAX_LINES:
                        # we have read beyond the line count
                        yield {'lines': buffer}
                        yield {
                            'error': (
                                'This file has been truncated because'
                                f' it is over {MAX_LINES} lines long.'
                            )
                        }
                        break

                    elif line_count == 0:
                        # this is the first line
                        # (this is a special line contains the file path)
                        line_count += 1
                        yield {
                            'connected': True,
                            'path': (await queue.get())[2:].strip(),
                        }
                        continue

                    # read in the log lines and add them to the buffer
                    line = await queue.get()
                    line_count += 1
                    buffer.append(line)
                    if len(buffer) >= 75:
                        yield {'lines': list(buffer)}
                        buffer.clear()
                        # there is more text to read so don't sleep (but
                        # still "sleep(0)" to yield control to other
                        # coroutines)
                        await asyncio.sleep(0)

        finally:
            # kill the cat-log process
            kill_process_tree(proc.pid)

            # terminate the queue
            enqueue_task.cancel()
            with suppress(asyncio.CancelledError):
                await enqueue_task

            # tell the client we have disconnected
            yield {'connected': False}

    @classmethod
    async def cat_log_files(cls, id_: Tokens, log: 'Logger') -> List[str]:
        """Calls cat log to get list of available log files.

        Note kept separate from the cat_log method above as this is a one off
        query rather than a process held open for subscription.
        This uses the Cylc cat-log interface, list dir mode, forcing remote
        file checking.
        """
        cmd: List[str] = ['cylc', 'cat-log', '-m', 'l', '-o', id_.id]
        log.debug(f"$ {' '.join(cmd)}")
        proc_job = await asyncio.subprocess.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        ret_code = await proc_job.wait()
        out, err = await proc_job.communicate()
        if ret_code:
            log.error(
                f"Command failed ({ret_code}): {' '.join(cmd)}\n{err.decode()}"
            )
        if out:
            return sorted(
                # return the log files in reverse sort order
                # this means that the most recent log file rotations
                # will be at the top of the list
                out.decode().splitlines(),
                reverse=True,
            )
        return []


class Resolvers(BaseResolvers):
    """UI Server context GraphQL query and mutation resolvers."""

    def __init__(
        self,
        app: 'CylcUIServer',
        data: 'DataStoreMgr',
        log: 'Logger',
        workflows_mgr: 'WorkflowsManager',
        executor,
        **kwargs
    ):
        super().__init__(data)
        self.app = app
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
        kwargs: Dict[str, Any],
    ) -> List[Union[bool, str]]:

        if command == 'clean':  # noqa: SIM116
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
        elif command == 'scan':
            return await Services.scan(
                kwargs,
                self.workflows_mgr
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
            self.app,
            info,
            file
        ):
            yield ret

    async def query_service(
        self,
        id_: Tokens,
    ):
        return await Services.cat_log_files(id_, self.log)


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
