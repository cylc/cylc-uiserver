import json
import re
from subprocess import Popen, PIPE

from jupyterhub.services.auth import HubOAuthenticated
from tornado import web
from typing import List, Union


class CylcScanHandler(HubOAuthenticated, web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Content-Type", 'application/json')

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


__all__ = ["CylcScanHandler"]
