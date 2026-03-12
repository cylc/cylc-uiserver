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

from logging import getLogger
from logging.config import dictConfig
import os
from pathlib import Path
from secrets import token_hex

import pytest

from cylc.uiserver.logging_util import RotatingUISFileHandler


@pytest.fixture
def rotating_log_setup():
    """Fixture to reset RotatingUISFileHandler state after each test."""
    try:
        yield
    finally:
        RotatingUISFileHandler.started = False


def test_rollover(tmp_path: Path, rotating_log_setup):
    """Check log file rotates on restart."""
    log_dir = tmp_path / 'log_dir'
    log_dir.mkdir(parents=True)
    log_file = log_dir / 'log'
    logger_name = f'test_{token_hex(3)}'
    logging_config = {
        'version': 1,
        'handlers': {
            'test_handler': {
                'class': 'cylc.uiserver.logging_util.RotatingUISFileHandler',
                'filename': str(log_file),
                'backupCount': 1,
            }
        },
        'loggers': {
            logger_name: {
                'handlers': ['test_handler'],
                'level': 'INFO',
            }
        }
    }
    dictConfig(logging_config)
    logger = getLogger(logger_name)

    logger.info('A')
    logger.info('B')
    # Traitlets may reconfigure logging several times; it should not rollover
    dictConfig(logging_config)
    logger.info('C')
    assert set(os.listdir(log_dir)) == {'log'}

    # Simulate starting the application again, which should cause a rollover
    RotatingUISFileHandler.started = False
    dictConfig(logging_config)
    logger.info('Z')
    assert set(os.listdir(log_dir)) == {'log', 'log.1'}

    assert log_file.read_text().splitlines() == ['Z']
    assert (log_dir / 'log.1').read_text().splitlines() == ['A', 'B', 'C']
