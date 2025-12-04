# THIS FILE IS PART OF THE CYLC WORKFLOW ENGINE.
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

"""Unit testing for web service functionality
"""
from contextlib import contextmanager
import pytest
from types import SimpleNamespace

from cylc.uiserver.ws import get_review_service_config


def _mock_bind(input_):
    """Mock the socket.bind interface with simulating having a range
    of bad ports.
    """
    _, port = input_
    if port in list(range(8000, 8002)):
        raise Exception(f'Port is {port}')
    return True


@contextmanager
def _mock_socket(*args):
    """Mock socket.socket context object
    """
    yield SimpleNamespace(bind=_mock_bind)


@pytest.mark.parametrize(
    'inputs, port',
    (
        (((8000, 8003), None), 8002),
        (((8000, 8003), 'gerbil/wheel'), 8002),
    )
)
def test_get_review_service_config(monkeypatch, inputs, port):
    monkeypatch.setattr('socket.socket', _mock_socket)
    result = get_review_service_config(*inputs)
    assert result['command'][3] == f'--port={port}'
    assert result['command'][4] == f'--service-root={inputs[1]}'
    assert result['url'] == f"http://127.0.0.1:{port}/"


def test_get_review_service_config_no_port(monkeypatch):
    inputs = ((8000, 8001), None)
    monkeypatch.setattr('socket.socket', _mock_socket)
    with pytest.raises(Exception, match='bleugh'):
        get_review_service_config(*inputs)
