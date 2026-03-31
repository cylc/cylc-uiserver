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
from time import time
from urllib.parse import urlencode

import pytest
from tornado.httpclient import HTTPClientError

from cylc.flow.id import Tokens
from cylc.uiserver.data_store_mgr import DataStoreMgr, ALL_DELTAS


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

    async def _fetch(*endpoint, query=None, headers=None, **kwargs):
        headers = headers or {}
        headers = {
            'Content-Type': 'application/json',
            **headers,
        }
        if not kwargs.get('method'):
            kwargs['method'] = 'POST'
        params = {}
        if 'body' not in kwargs:
            if kwargs['method'] in ("POST", "PATCH", "PUT"):
                kwargs['body'] = json.dumps({'query': query}, indent=4)
            else:
                params = {'query': query}
        return await jp_fetch(
            *endpoint,
            headers=headers,
            params=params,
            **kwargs
        )

    return _fetch


@pytest.fixture
def gql_subscription(jp_ws_fetch):
    """Open a GraphQL subscription.

    E.G:

    ws = await gql_subscription(
        *('cylc', 'subscriptions'),
        sub={
            'id': '1',
            'type': 'start',
            'payload': {
                'query': '''
                    subscription {
                      workflows {
                        id
                        status
                      }
                    }
                '''
            }
        }
    )
    # Can loop on this
    response = json.loads(await ws.read_message())
    assert response == . . .

    ws.close()
    """

    async def _fetch(*endpoint, sub=None, headers=None, **kwargs):
        headers = headers or {}
        headers = {
            'Content-Type': 'application/json',
            'Sec-Websocket-Protocol': 'graphql-ws',
            **headers,
        }
        ws = await jp_ws_fetch(
            *endpoint,
            headers=headers,
            **kwargs
        )

        # Using graphql-ws protocol, so send connection_init
        await ws.write_message(
            json.dumps({"type": "connection_init", "payload": {}})
        )
        ack = json.loads(await ws.read_message())
        assert ack["type"] == "connection_ack"

        # Start subscription
        sub = sub or {}
        await ws.write_message(json.dumps(sub))

        return ws

    return _fetch


async def test_query(gql_query, dummy_workflow):
    """Test sending the most basic GraphQL query in all it's forms."""
    # configure two dummy workflows so we have something to look at
    await dummy_workflow('foo')
    await dummy_workflow('bar')

    query = '''query {workflows {id status}}'''

    # perform the request
    get_response = await gql_query(
        *('cylc', 'graphql'),
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        query=query,
        method='GET'
    )
    assert get_response.code == 200

    # test against same query different method
    post_response = await gql_query(*('cylc', 'graphql'), query=query)
    assert get_response.body == post_response.body

    # we should find the two dummy workflows in the response
    body = json.loads(get_response.body)
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

    # Test a bad query
    with pytest.raises(HTTPClientError) as exc:
        await gql_query(*('cylc', 'graphql'), query='this is not a query')
    assert r"Syntax Error: Unexpected Name 'this" in str(exc)

    # Test bad graphql query
    bad_query = '''
        query {
            workflows {
                notAField
            }
        }
    '''
    result = await gql_query(
        *('cylc', 'graphql'), query=bad_query, raise_error=False)
    assert r"Cannot query field 'not" in result.reason

    # Test 'application/graphql'
    response_gql = await gql_query(
        *('cylc', 'graphql'),
        headers={'Content-Type': 'application/graphql'},
        body=query
    )
    assert response_gql.code == 200
    assert json.loads(response_gql.body) == body

    # Test 'application/x-www-form-urlencoded'
    response_form = await gql_query(
        *('cylc', f'graphql'),
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        body=urlencode({'query': query, 'pretty': True}),
    )
    assert response_form.code == 200
    assert json.loads(response_form.body) == body
    # should be pretty
    assert response_form.body != get_response.body


async def test_batch_query(gql_query, dummy_workflow):
    """Test sending a GraphQL batch query."""
    # configure two dummy workflows so we have something to look at
    await dummy_workflow('foo')
    await dummy_workflow('bar')

    query = '''
        query fooFlow {workflows (ids: ["~me/foo"]) {...shared}}
        query barFlow {workflows (ids: ["~me/bar"]) {...shared}}
        fragment shared on Workflow { id status }
    '''

    # perform the request
    response = await gql_query(
        *('cylc', 'graphql', 'batch'),
        body=json.dumps(
            [{'id': 1, 'query': query, 'operationName': 'fooFlow'}]
        )
    )
    assert response.code == 200

    # we should find the 'fooFlow' query result in the response
    body = json.loads(response.body)
    assert body == [
        {
            "id":1,
            "data": {
                "workflows": [
                    {
                        "id": "~me/foo",
                        "status": "stopped"
                    }
                ]
            },
            "status":200
        }
    ]

    # Test a empty batch
    with pytest.raises(HTTPClientError) as exc:
        await gql_query(
            *('cylc', 'graphql', 'batch'), body=json.dumps([]))
    assert 'Bad Request' in str(exc)

    # Test a non-list "batch"
    response = await gql_query(
        *('cylc', 'graphql', 'batch'), body=json.dumps({}), raise_error=False)
    assert response.reason == 'Bad Request'


async def test_mutation(gql_query, dummy_workflow):
    """Test simple mutation scenarios."""

    # start a workflow
    await dummy_workflow('foo')

    # make a simple mutation
    response = await gql_query(
        *('cylc', 'graphql'),
        query='''
            mutation {
                pause(workflows: ["*"]) {
                    result
                }
            }
        ''',
    )
    assert response.code == 200

    # try a mutation with GET method
    response = await gql_query(
        *('cylc', 'graphql'),
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        query='''
            mutation {
                stop(workflows: ["*"]) {
                    result
                }
            }
        ''',
        method='GET',
        raise_error=False
    )
    # Should be rejected for incorrect method.
    assert response.code == 405
    assert response.reason == 'Method Not Allowed'


async def test_multi(gql_query, monkeypatch, cylc_uis, dummy_workflow):
    """Ensure multi-mutation requests are properly forwarded.

    * Multiple mutations can be specified in one request.
    * These pass through the GraphQL routing where they are authorised
      one by one.
    * They should be issued to the scheduler one by one, the GraphQL
      query must be altered so it only contains the single mutation.

    """
    # need at least one workflow for the request to be forwarded
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

    # issue clean mutation
    response = await gql_query(
        *('cylc', 'graphql'),
        query='''
            mutation {
                clean(workflows: ["%s"]){
                    result
                }
            }
        ''' % (
            Tokens(user='me', workflow='foo').id,
        ),
    )
    assert response.code == 200


async def test_subscription(gql_subscription, dummy_workflow):
    """Test opening a GraphQL subscription and receive a message."""

    # Start a workflow for subscription content.
    await dummy_workflow('foo')

    # Start subscription
    sub_id = "1"
    ws = await gql_subscription(
        *('cylc', 'subscriptions'),
        sub={
            "id": sub_id,
            "type": "start",
            "payload": {
                "query": """
                    subscription {
                      workflows {
                        id
                        status
                      }
                    }
                """
            }
        }
    )

    # Receive the next message
    response = json.loads(await ws.read_message())

    assert response == {
        'id': sub_id,
        'type': 'data',
        'payload': {
            'data': {
                'workflows': [
                    {
                        'id': '~me/foo',
                        'status': 'stopped'
                    }
                ]
            }
        }
    }

    # Run the stop/cleanup code
    await ws.write_message(json.dumps({"id": sub_id, "type": "stop"}))

    ws.close()


async def test_subscription_deltas(
    cylc_uis, gql_subscription, make_all_delta):
    """Test deltas being processesed and recieved by a GraphQL subscription."""

    data_store_mgr = cylc_uis.data_store_mgr

    # Start subscription
    sub_id = "1"
    ws = await gql_subscription(
        *('cylc', 'subscriptions'),
        sub={
            "id": sub_id,
            "type": "start",
            "payload": {
                "query": """
                    subscription {
                      deltas (stripNull: true){
                        id
                        shutdown
                        added {
                          workflow {
                            status
                          }
                          taskProxies {
                            id
                            state
                          }
                        }
                        updated {
                          workflow {
                            status
                          }
                          taskProxies {
                            id
                            state
                          }
                        }
                      }
                    }
                """
            }
        }
    )

    w_tokens = Tokens(user='user', workflow='this')
    w_id = w_tokens.id

    # Stop scanning messages
    cylc_uis.workflows_mgr._stopping = True
    # Register for data-store entry
    await data_store_mgr.register_workflow(w_id=w_id, is_active=False)

    # Receive first message
    response = json.loads(await ws.read_message())
    assert response == {
        'id': sub_id,
        'type': 'data',
        'payload': {
            'data': {
                'deltas': {
                    'id': w_id,
                    'shutdown': False,
                    'added': {
                        'workflow': {'status': 'stopped'}
                    },
                    'updated': {}
                }
            }
        }
    }

    # Create added delta
    tp_id = w_tokens.duplicate(cycle='1', task='foo').id
    all_added_delta = make_all_delta(w_id, 'added', tp_id, 'waiting', time())
    all_added_delta.workflow.added.status = 'running'
    all_added_delta.workflow.reloaded = True

    # Process added delta, creating gql subscription delta as a result
    data_store_mgr._update_workflow_data(ALL_DELTAS, all_added_delta, w_id)

    # Receive next message
    response = json.loads(await ws.read_message())
    assert response == {
        'id': sub_id,
        'type': 'data',
        'payload': {
            'data': {
                'deltas': {
                    'id': w_id,
                    'shutdown': False,
                    'added': {
                        'workflow': {'status': 'running'},
                        'taskProxies': [
                            {
                                'id': tp_id,
                                'state': 'waiting'
                            }
                        ]
                    },
                    'updated': {}
                }
            }
        }
    }

    # Create update delta
    all_updated_delta = make_all_delta(
        w_id, 'updated', tp_id, 'running', time())
    all_updated_delta.workflow.updated.status = 'stopping'
    all_updated_delta.workflow.reloaded = False

    # Process updated delta
    data_store_mgr._update_workflow_data(ALL_DELTAS, all_updated_delta, w_id)

    # Receive next message
    response = json.loads(await ws.read_message())
    assert response['payload']['data']['deltas']['updated'][
        'workflow'
    ]['status'] == 'stopping'
    assert response['payload']['data']['deltas']['updated'][
        'taskProxies'
    ][0]['state'] == 'running'

    # Shutdown delta
    data_store_mgr._update_workflow_data(
        'shutdown', 'this is the end'.encode('utf-8'), w_id)

    # Receive shutdown message
    response = json.loads(await ws.read_message())
    assert response['payload']['data']['deltas']['shutdown']

    # Start scanning messages again
    cylc_uis.workflows_mgr._stopping = False
    # Receive scan message
    response = json.loads(await ws.read_message())
    assert response['payload']['data']['deltas']['updated'][
        'workflow'
    ]['status'] == 'stopped'

    # Run the stop/cleanup code
    await ws.write_message(json.dumps({"id": sub_id, "type": "stop"}))

    ws.close()
