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


import json
import os
from shutil import which
import socket
import sys
from typing import Any, Optional, Union, Dict
from tornado.httpclient import (
    AsyncHTTPClient,
    HTTPRequest,
    HTTPClientError
)

from cylc.flow import LOG
from cylc.flow.exceptions import ClientError
from cylc.flow.network import encode_
from cylc.flow.network.client import WorkflowRuntimeClientBase
from cylc.flow.network.client_factory import CommsMeth

from cylc.uiserver.app import API_INFO_FILE


class WorkflowRuntimeClient(WorkflowRuntimeClientBase):
    """Client to UI server communication using HTTP."""

    DEFAULT_TIMEOUT = 10  # seconds

    def __init__(
        self,
        workflow: str,
        host: Optional[str] = None,
        port: Union[int, str, None] = None,
        timeout: Union[float, str, None] = None,
    ):
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        # gather header info post start
        self.header = self.get_header()

    async def async_request(
        self,
        command: str,
        args: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        req_meta: Optional[Dict[str, Any]] = None
    ) -> object:
        """Send an asynchronous request using asyncio.

        Has the same arguments and return values as ``serial_request``.

        """
        if not args:
            args = {}

        try:
            with open(API_INFO_FILE, "r") as api_file:
                api_info = json.loads(api_file.read())
        except FileNotFoundError:
            raise ClientError(
                'API info not found, is the UI-Server running?\n'
                f'({API_INFO_FILE})'
            )

        # send message
        msg: Dict[str, Any] = {'command': command, 'args': args}
        msg.update(self.header)
        # add the request metadata
        if req_meta:
            msg['meta'].update(req_meta)

        LOG.debug('https:send %s', msg)

        try:
            request = HTTPRequest(
                url=api_info["url"] + 'cylc/graphql',
                method='POST',
                headers={
                    'Authorization': f'token {api_info["token"]}',
                    'Content-Type': 'application/json',
                    'meta': encode_(msg.get('meta', {})),
                },
                body=json.dumps(
                    {
                        'query': args['request_string'],
                        'variables': args.get('variables', {}),
                    }
                ),
                request_timeout=float(self.timeout)
            )
            res = await AsyncHTTPClient().fetch(request)
        except ConnectionRefusedError:
            raise ClientError(
                'Connection refused, is the UI-Server running?\n'
                f'({api_info["url"]}cylc/graphql)'
            )
        except HTTPClientError as exc:
            raise ClientError(
                'Client error with Hub/UI-Server request.',
                f'{exc}'
            )

        response = json.loads(res.body)
        LOG.debug('https:recv %s', response)

        try:
            return response['data']
        except KeyError:
            error = response.get(
                'error',
                {'message': f'Received invalid response: {response}'},
            )
            raise ClientError(
                error.get('message'),
                error.get('traceback'),
            )

    def get_header(self) -> dict:
        """Return "header" data to attach to each request for traceability.

        Returns:
            dict: dictionary with the header information, such as
                program and hostname.
        """
        host = socket.gethostname()
        if len(sys.argv) > 1:
            cmd = sys.argv[1]
        else:
            cmd = sys.argv[0]

        cylc_executable_location = which("cylc")
        if cylc_executable_location:
            cylc_bin_dir = os.path.abspath(
                os.path.join(cylc_executable_location, os.pardir)
            )
            if not cylc_bin_dir.endswith("/"):
                cylc_bin_dir = f"{cylc_bin_dir}/"

            if cmd.startswith(cylc_bin_dir):
                cmd = cmd.replace(cylc_bin_dir, '')
        return {
            'meta': {
                'prog': cmd,
                'host': host,
                'comms_method':
                    os.getenv(
                        "CLIENT_COMMS_METH",
                        default=CommsMeth.HTTPS.value
                    )
            }
        }
