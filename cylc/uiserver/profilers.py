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

"""Profilers for the ServerApp instance.

This is effectively a cut-down version of the cylc.flow.main_loop plugin
system. It's only intended for developer use.

NOTE: All profiler specific imports are handled in their `__init__` methods
to avoid importing profiler code when not requested.
"""

from time import time
from types import SimpleNamespace

from cylc.uiserver.config_util import USER_CONF_ROOT


class Profiler:
    def __init__(self, app):
        self.app = app
        self.app.log.warning(f'Starting profiler: {self.__class__.__name__}')

    def periodic(self):
        pass

    def shutdown(self):
        pass


class CProfiler(Profiler):
    """Invoke cprofile via the cylc.flow.profiler interface."""

    def __init__(self, app):
        Profiler.__init__(self, app)

        from cylc.flow.profiler import Profiler as CylcCProfiler

        self.cprofiler = CylcCProfiler(
            # the profiler is designed to attach to a Cylc scheduler
            schd=SimpleNamespace(workflow_log_dir=USER_CONF_ROOT),
            enabled=True,
        )

        self.cprofiler.start()

    def periodic(self):
        pass

    def shutdown(self):
        self.cprofiler.stop()


class TrackObjects(Profiler):
    """Invoke pympler.asized via the cylc.main_loop.log_memory interface."""

    def __init__(self, app):
        Profiler.__init__(self, app)

        from cylc.flow.main_loop.log_memory import (
            _compute_sizes,
            _plot,
            _transpose,
        )

        self._compute_sizes = _compute_sizes
        self._transpose = _transpose
        self._plot = _plot
        self.data = []
        self.min_size = 100
        self.obj = app

    def periodic(self):
        self.data.append(
            (
                time(),
                self._compute_sizes(self.obj, min_size=self.min_size),
            )
        )

    def shutdown(self):
        self.periodic()
        fields, times = self._transpose(self.data)
        self._plot(
            fields,
            times,
            USER_CONF_ROOT,
            f'{self.obj} attrs > {self.min_size / 1000}kb',
        )


class TrackDataStore(TrackObjects):
    """Like TrackObjects but for the Data Store."""

    def __init__(self, app):
        TrackObjects.__init__(self, app)
        self.obj = self.app.data_store_mgr


PROFILERS = {
    'cprofile': CProfiler,
    'track_objects': TrackObjects,
    'track_data_store': TrackDataStore,
}


def get_profiler(profiler: str):
    if not profiler:
        return None
    try:
        return PROFILERS[profiler]
    except KeyError:
        raise Exception(
            f'Unknown profiler: {profiler}'
            f'\nValid options: {", ".join(PROFILERS)}'
        )
