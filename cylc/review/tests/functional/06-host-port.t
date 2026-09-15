#!/bin/bash
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
#-------------------------------------------------------------------------------
# Test for "cylc review", cycles/taskjobs list, workflow server host:port.
# Require a version of cylc with cylc/cylc-flow#1705 merged in.
#-------------------------------------------------------------------------------
. "$(dirname "$0")/test_header"
requires_cherrypy
requires_jq

set_test_number 6
#-------------------------------------------------------------------------------
# Initialise, validate and run a workflow for testing with
init_workflow "${TEST_NAME_BASE}" <<'__FLOW_CONFIG__'
[scheduler]
    allow implicit tasks = True
[scheduling]
    [[graph]]
        R1 = foo
__FLOW_CONFIG__

TEST_NAME=$TEST_NAME_BASE-validate
run_ok "${TEST_NAME}" cylc validate "${WORKFLOW_NAME}"

# Run workflow in background to leave sitting in paused state
cylc play --debug --pause "${WORKFLOW_NAME}" 2>'/dev/null'
#-------------------------------------------------------------------------------
# Initialise WSGI application for the cylc review web service
TEST_NAME="${TEST_NAME_BASE}-ws-init"
cylc_ws_init 'cylc' 'review'
if [[ -z "${TEST_CYLC_WS_PORT}" ]]; then
    exit 1
fi

# Set up standardURL escaping of forward slashes in 'cylctb-' workflow names.
# shellcheck disable=SC2001
ESC_WORKFLOW_NAME="$(echo "${WORKFLOW_NAME}" | sed 's|/|%2F|g')"
#-------------------------------------------------------------------------------
# Data transfer output check for a specific workflow's host and port

SRV_D="${HOME}/cylc-run/${WORKFLOW_NAME}/.service"
CONTACT="${SRV_D}/contact"
poll test -s "${CONTACT}"
sleep 1
PORT="$(awk -F= '$1 ~ /CYLC_WORKFLOW_PORT/ {print $2}' "${CONTACT}")"
HOST="$(awk -F= '$1 ~ /CYLC_WORKFLOW_HOST/ {print $2}' "${CONTACT}")"
HOST=${HOST%%.*} # strip domain

if [[ -n "${HOST}" && -n "${PORT}" ]]; then
    for METHOD in 'cycles' 'taskjobs'; do
        TEST_NAME="${TEST_NAME_BASE}-ws-run-${METHOD}"
        URL_NAME="${TEST_CYLC_WS_URL}/${METHOD}/${USER}?suite=${ESC_WORKFLOW_NAME}&form=json"
        run_ok "${TEST_NAME}" curl "${URL_NAME}"
        cmp_ok <(jq -r '.states.server' "${TEST_NAME}.stdout") <<< "${HOST}:${PORT}"
    done
else
    skip 4 'Cannot determine workflow host or port'
fi
#-------------------------------------------------------------------------------
# Tidy up - requires the stop because we deliberately left it running.
cylc stop "${WORKFLOW_NAME}" --now --now
poll_workflow_stopped
purge "${WORKFLOW_NAME}"
cylc_ws_kill

exit
