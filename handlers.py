# -*- coding: utf-8 -*-
# Copyright (C) 2019 NIWA & British Crown (Met Office) & Contributors.
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
import re
from subprocess import Popen, PIPE
from typing import List, Union
from urllib.parse import urlparse
from urllib.parse import urlunparse

from jupyterhub import __version__ as jupyterhub_version
from jupyterhub.services.auth import HubOAuthenticated
from tornado import web


class BaseHandler(web.RequestHandler):

    def set_default_headers(self) -> None:
        self.set_header("X-JupyterHub-Version", jupyterhub_version)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


class APIHandler(BaseHandler):

    def set_default_headers(self) -> None:
        super().set_default_headers()
        self.set_header("Content-Type", 'application/json')


class MainHandler(HubOAuthenticated, BaseHandler):

    # hub_users = ["kinow"]
    # hub_groups = []
    # allow_admin = True

    def initialize(self, path):
        self._static = path

    @web.authenticated
    def get(self):
        """Render the UI prototype."""
        index = os.path.join(self._static, "index.html")
        self.write(open(index).read())


class UserProfileHandler(HubOAuthenticated, APIHandler):

    def set_default_headers(self) -> None:
        super().set_default_headers()
        self.set_header("Content-Type", 'application/json')

    @web.authenticated
    def get(self):
        self.write(json.dumps(self.get_current_user()))


class CylcScanHandler(HubOAuthenticated, APIHandler):

    def _parse_suite_line(self, suite_line: bytes) -> Union[dict, None]:
        if suite_line:
            parts = re.split(r"[ :@]", suite_line.decode())
            if len(parts) == 4:
                return {
                    "name": parts[0],
                    "user": parts[1],
                    "host": parts[2],
                    "port": int(parts[3])
                }
        return None

    def _get_suites(self, suite_lines: List[bytes]) -> List[dict]:
        suites = []
        for suite_line in suite_lines:
            suite = self._parse_suite_line(suite_line)
            if suite:
                suites.append(suite)
        return suites

    @web.authenticated
    def get(self):
        cylc_scan_proc = Popen("cylc scan", shell=True, stdout=PIPE)
        cylc_scan_out = cylc_scan_proc.communicate()[0]

        suite_lines = cylc_scan_out.splitlines()
        suites = self._get_suites(suite_lines)
        self.write(json.dumps(suites))


class AddSlashHandler(web.RequestHandler):

    def get(self, *args):
        src = urlparse(self.request.uri)
        dest = src._replace(path=src.path + '/')
        self.redirect(urlunparse(dest))


__all__ = [
    "MainHandler",
    "UserProfileHandler",
    "CylcScanHandler",
    "AddSlashHandler"
]
