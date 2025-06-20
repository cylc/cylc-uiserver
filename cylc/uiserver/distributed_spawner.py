#!/usr/bin/env python3
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

from contextlib import suppress
import logging
from subprocess import Popen, PIPE, DEVNULL
import sys
from textwrap import dedent
from typing import List, Tuple

from jupyterhub.spawner import Spawner
from psutil import Process, NoSuchProcess
from traitlets import (
    DottedObjectName,
    List as TList,
    Unicode,
    default,
)

from cylc.flow import __version__ as CYLC_VERSION
from cylc.flow.host_select import select_host


logger = logging.getLogger(__name__)


class DottedObject(DottedObjectName):
    """Like DottedObjectName, only it actually imports the thing."""

    def validate(self, obj, value):
        """Import and return bar given the string foo.bar."""
        package = '.'.join(value.split('.')[0:-1])
        obj = value.split('.')[-1]
        try:
            if package:
                module = __import__(package, fromlist=[obj])
                return module.__dict__[obj]
            else:
                return __import__(obj)
        except ImportError:
            self.error(obj, value)


class DistributedSpawner(Spawner):
    """A simple SSH Spawner with load balancing capability.

    Runs as the user, no elevated privileges required.

    Requires both passphraseless SSH and a shared filesystem between the
    hub server and all configured hosts.
    """

    hosts = TList(
        trait=Unicode(),
        config=True,
        help='''
            List of host names to choose from.
        '''
    )

    ranking = Unicode(
        config=True,
        help='''
            Ranking to use for load balancing purposes.

            If unspecified a host is chosen at random.

            These rankings can be used to pick the host with the most available
            memory or filter out hosts with high server load.

            These rankings are provided in the same format as
            :cylc:conf`global.cylc[scheduler][run hosts]ranking`.
        '''
    )

    ssh_cmd = TList(
        trait=Unicode(),
        config=True,
        help='''
            The SSH command to use for connecting to the remote hosts.

            E.G: ``['ssh']`` (default)
        '''
    )

    get_ip_from_hostname = DottedObject(
        config=True,
        help='''
            Function for obtaining the IP address from a hostname.

            E.G: ``socket.gethostbyname`` (default)
        '''
    )

    @default('get_ip_from_hostname')
    def default_ip_from_hostname_command(self):
        return 'socket.gethostbyname'

    @default('ssh_cmd')
    def default_ssh_command(self):
        return ['ssh']

    def __init__(self, *args, **kwargs):
        print('# INIT')
        Spawner.__init__(self, *args, **kwargs)
        self.pid = None
        print('# /INIT')

    def choose_host(self):
        print('# SELECT')
        return select_host(self.hosts, self.ranking)[1]

    def get_env(self):
        return {
            **Spawner.get_env(self),
            'CYLC_VERSION': CYLC_VERSION,
            'JUPYTERHUB_SERVICE_PREFIX': '/user/osanders/'
        }

    def get_env_cmd(self) -> List[str]:
        """Return the spawner environment as an ``env`` command.

        Example output: ``['env', 'FOO=bar']``
        """
        env = self.get_env()
        if not env:
            return []
        return [
            'env'
        ] + [
            f'{key}={value}'
            for key, value in self.get_env().items()
        ]

    def get_remote_port(self) -> int:
        """Find an open port to spawn the app onto.

        Invokes Python over SSH to call a JupyterHub utility function on the
        remote host.
        """
        print('# GET_REMOTE_PORT')
        cmd = [
            *self.ssh_cmd,
            self._host,
            sys.executable,
        ]
        logger.debug('$ ' + ' '.join(cmd))
        proc = Popen(
            cmd,
            stdout=PIPE,
            stdin=PIPE,
            text=True
        )
        proc.communicate(dedent('''
            from jupyterhub.utils import random_port
            print(random_port())
        '''))
        if proc.returncode:
            raise Exception('remote proc failed')
        stdout, _ = proc.communicate()
        try:
            port = int(stdout)
        except Exception:
            raise Exception(f'invalid stdout: {stdout}')
        print('# /GET_REMOTE_PORT', port)
        return port

    async def start(self) -> Tuple[str, str]:
        print('# START')
        self._host = self.choose_host()
        port = self.get_remote_port()
        cmd = [
            *self.ssh_cmd,
            self._host,
            *self.get_env_cmd(),
            *self.cmd,
            *self.get_args(),
            # NOTE: selg.get_args may set --port, however, we override it
            f'--port={port}',
        ]
        logger.info('$ ' + ' '.join(cmd))
        print('$ ' + ' '.join(cmd))
        self.pid = Popen(
            cmd,
            stderr=PIPE,
            stdin=DEVNULL,
            text=True
        ).pid

        # TODO
        # The server launches on the host
        # The URL is accessible from the host
        # The server appears to be hub-aware in that it adds a hub redirect thinggy
        # But not from elsewhere on the network

        # Need to pass through the Hub URL somehow???

        ip = self.get_ip_from_hostname(self._host)
        print('# /START', ip, port)
        return (ip, port)

    async def stop(self, now=False):
        if self.pid:
            with suppress(NoSuchProcess):
                Process(self.pid).kill()

    async def poll(self):
        print('# POLL')
        if self.pid:
            try:
                Process(self.pid)
                print('# /POLL', None)
                return None  # running
            except NoSuchProcess:
                print('# /POLL', 1)
                return 1  # stopped
        print('# /POLL', 0)
        return 0  # not yet started
