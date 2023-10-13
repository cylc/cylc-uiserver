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

"""Utilities relating to the listing and management of source workflows."""

from contextlib import suppress
from pathlib import Path
from typing import Optional, List, Dict

from cylc.flow.cfgspec.glbl_cfg import glbl_cfg
from cylc.flow.id import Tokens
from cylc.flow.network.scan import scan_multi
from cylc.flow.pathutil import get_workflow_run_dir
from cylc.flow.workflow_files import get_workflow_source_dir


# the user's configured workflow source directories
SOURCE_DIRS: List[Path] = [
    Path(source_dir).expanduser()
    for source_dir in glbl_cfg().get(['install', 'source dirs'])
]


SourceWorkflow = Dict


def _source_workflow(source_path: Path) -> SourceWorkflow:
    """Return the fields required to resolve a SourceWorkflow.

    Args:
        source_path:
            Path to the source workflow directory.

    """
    return {
        'name': _get_source_workflow_name(source_path),
        'path': source_path,
    }


def _blank_source_workflow() -> SourceWorkflow:
    """Return a blank source workflow.

    This will be used for workflows which were not installed by "cylc install".
    """

    return {'name': None, 'path': None}


def _get_source_workflow_name(source_path: Path) -> Optional[str]:
    """Return the "name" of the source workflow.

    This is the "name" that can be provided to the "cylc install" command.

    Args:
        source_path:
            Path to the source workflow directory.

    Returns:
        The source workflow name if the source workflow is located within
        a configured source directory, else None.

    """
    for source_dir in SOURCE_DIRS:
        with suppress(ValueError):
            return str(source_path.relative_to(source_dir))
    return None


def _get_workflow_source(workflow_id):
    """Return the source workflow for the given workflow ID."""
    run_dir = get_workflow_run_dir(workflow_id)
    source_dir, _symlink = get_workflow_source_dir(run_dir)
    if source_dir:
        return _source_workflow(Path(source_dir))
    return _blank_source_workflow()


async def list_source_workflows(*_) -> List[SourceWorkflow]:
    """List source workflows located in the configured source directories."""
    ret = []
    async for flow in scan_multi(SOURCE_DIRS):
        ret.append(_source_workflow(flow['path']))
    return ret


def get_workflow_source(data, _, **kwargs) -> Optional[SourceWorkflow]:
    """Resolve the source for an installed workflow.

    If the source cannot be resolved, e.g. if the workflow was not installed by
    "cylc install", then this will return None.
    """
    workflow_id = Tokens(data.id)['workflow']
    return _get_workflow_source(workflow_id)
