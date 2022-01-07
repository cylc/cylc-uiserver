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
from textwrap import dedent

import pytest

from cylc.flow.id import Tokens


@pytest.fixture
def gql_query(jp_fetch):
    """Perform a GraphQL request.

    E.G:

    response = await gql_query(
        *('cylc', 'graphql'),
        query='''
            query {
                workflows {
                    id
                    status
                }
            }
        ''',
    )

    """

    async def _fetch(*endpoint, query=None, headers=None):
        headers = headers or {}
        headers = {
            **headers,
            'Content-Type': 'application/json'
        }
        return await jp_fetch(
            *endpoint,
            method='POST',
            headers=headers,
            body=json.dumps({'query': query}, indent=4),
        )

    return _fetch


async def test_query(gql_query, dummy_workflow):
    """Test sending the most basic GraphQL query."""
    # configure two dummy workflows so we have something to look at
    await dummy_workflow('foo')
    await dummy_workflow('bar')

    # perform the request
    response = await gql_query(
        *('cylc', 'graphql'),
        query='''
            query {
                workflows {
                    id
                    status
                }
            }
        ''',
    )
    assert response.code == 200

    # we should find the two dummy workflows in the response
    body = json.loads(response.body)
    assert body['data'] == {
        'workflows': [
            {
                'id': Tokens(user='me', workflow='foo').id,
                'status': 'stopped',
            },
            {
                'id': Tokens(user='me', workflow='bar').id,
                'status': 'stopped',
            },
        ]
    }


async def test_multi(gql_query, monkeypatch, cylc_uis, dummy_workflow):
    """Ensure multi-mutation requests are properly forwarded.

    * Multiple mutations can be specified in one request.
    * These pass through the GraphQL routing where they are authorised
      one by one.
    * They should be issued to the scheduler one by one, the GraphQL
      query must be altered so it only contains the single mutation.

    """
    # need at leat one workflow for the request to be forwarded
    await dummy_workflow('foo')
    await dummy_workflow('bar')

    # log all calls that go via the multi_request interface
    # (and prevent these calls from actually being made)
    calls = []

    async def _log(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr(cylc_uis.workflows_mgr, 'multi_request', _log)

    # issue three mutations
    response = await gql_query(
        *('cylc', 'graphql'),
        query='''
            mutation {
                hold(workflows: ["*"], tasks: []) {
                    result
                }
                pause(workflows: ["*"]) {
                    result
                }
                stop(workflows: ["*"]) {
                    result
                }
            }
        ''',
    )
    assert response.code == 200

    # there should have been three calls for the two mutations
    assert len(calls) == 3
    # the first for the hold mutation
    assert calls[0][0][2]['request_string'] == dedent('''
        mutation {
          hold(workflows: ["*"], tasks: []) {
            result
          }
        }
    ''').strip()
    # the second for the pause mutation
    assert calls[1][0][2]['request_string'] == dedent('''
        mutation {
          pause(workflows: ["*"]) {
            result
          }
        }
    ''').strip()
    # the third for the stop mutation
    assert calls[2][0][2]['request_string'] == dedent('''
        mutation {
          stop(workflows: ["*"]) {
            result
          }
        }
    ''').strip()
