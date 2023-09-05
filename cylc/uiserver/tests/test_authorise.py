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

from jupyter_server.extension.application import ExtensionApp
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from cylc.uiserver.authorise import (
    Authorization,
    AuthorizationMiddleware,
    get_list_of_mutations,
    parse_group_ids
)

log = ExtensionApp().log

CONTROL_OPS = [
    "clean",
    "ext_trigger",
    "hold",
    "kill",
    "message",
    "pause",
    "play",
    "poll",
    "release",
    "release_hold_point",
    "reload",
    "remove",
    "resume",
    "scan",
    "set_graph_window_extent",
    "set_hold_point",
    "set_outputs",
    "set_verbosity",
    "stop",
    "trigger",
]

ALL_OPS = [
    "clean",
    "read",
    "broadcast",
    "ext_trigger",
    "hold",
    "kill",
    "message",
    "pause",
    "play",
    "poll",
    "release",
    "release_hold_point",
    "reload",
    "remove",
    "resume",
    "scan",
    "set_graph_window_extent",
    "set_hold_point",
    "set_outputs",
    "set_verbosity",
    "stop",
    "trigger",
]

FAKE_SITE_CONF = {
    "*": {
        "*": {
            "default": "READ",
        },
        "user1": {
            "limit": ["!ALL"],
        },
    },
    "server_owner_1": {
        "*": {"default": ["READ", "message"],
              "limit": ["READ", "CONTROL"]},
        "user1": {"default": ["READ", "play", "pause"], "limit": ["ALL"]},
    },
    "server_owner_2": {
        "user2": {"limit": "ALL"},
        "group:groupA": {"default": ["READ", "CONTROL"]},
    },
    "group:grp_of_svr_owners": {
        "group:group2": {
            "default": "READ",
            "limit": ["READ", "CONTROL", "!stop", "!kill"],
        },
    },
}

FAKE_USER_CONF = {
    # Specified interactions granted to user1
    "user1": ["READ", "pause", "trigger", "message"],
    # Access to all operations workflows
    "group:group1": ["ALL"],
    # granted to users in group1
    # All READ and CONTROL, except trigger and edit
    "user2": ["READ", "CONTROL", "!trigger", "!edit"],
    # granted to user2
    "user3": ["READ"],
    "user4": ["!ALL"],
    "user5": ["play", "pause"],
    "group:group2": ["READ", "CONTROL", "!reload"],
}


@pytest.mark.parametrize(
    "expected_operations, owner_name, owner_groups, user_name, user_groups",
    [
        pytest.param(
            {
                "clean",
                "message",
                "play",
                "trigger",
                "resume",
                "scan",
                "set_verbosity",
                "set_graph_window_extent",
                "read",
                "poll",
                "hold",
                "remove",
                "set_hold_point",
                "release_hold_point",
                "ext_trigger",
                "pause",
                "pause",
                "set_outputs",
                "release",
            },
            "server_owner_2",
            ["group:grp_of_svr_owners"],
            "user7",
            ["group:group2"],
            id="user in * and groups, owner in * and groups",
        ),
        pytest.param(
            {"read"},
            "server_owner_3",
            [""],
            "user6",
            [""],
            id="user only in *, owner only in *",
        ),
        pytest.param(
            {"read"},
            "server_owner_2",
            ["group:grp_of_svr_owners"],
            "user-not-in-user-conf",
            ["group:non-existent-group"],
            id="user only in group and *",
        ),
        pytest.param(
            set(),
            "server_owner_1",
            [""],
            "user1",
            [""],
            id="user1 forbidden in site conf",
        ),
        pytest.param(
            set(),
            "server_owner_2",
            ["group:grp_of_svr_owners"],
            "user4",
            ["group:group2"],
            id="owner only in group and *",
        )
    ],
)
@patch("cylc.uiserver.authorise.get_groups")
def test_get_permitted_operations(
    mocked_get_groups,
    expected_operations,
    owner_name,
    owner_groups,
    user_name,
    user_groups,
):
    mocked_get_groups.side_effect = [(owner_groups, []), (user_groups, [])]
    auth_obj = Authorization(
        owner_name, FAKE_USER_CONF, FAKE_SITE_CONF, log
    )
    actual_operations = auth_obj.get_permitted_operations(
        access_user=user_name
    )
    assert actual_operations == expected_operations


@pytest.mark.parametrize(
    "expected_operations, access_user_dict, owner_auth_conf,",
    [
        pytest.param(
            {"!kill", "READ", "kill", "!stop", "pause", "play"},
            {
                "access_username": "access_user_1",
                "access_user_groups": ["group:group1", "group:group2"],
            },
            {
                "*": ["READ", "!kill"],
                "access_user_1": ["READ", "pause", "kill", "play", "!stop"],
            },
            id="Check username in user conf and in *",
        ),
        pytest.param(
            {"READ"},
            {
                "access_username": "access_user_2",
                "access_user_groups": ["group:group1", "group:group2"],
            },
            {
                "*": ["READ"],
                "access_user_1": ["READ", "pause", "kill", "play", "!stop"],
            },
            id="Check user just in *",
        ),
        pytest.param(
            {"pause", "kill", "!stop", "READ", "CONTROL"},
            {
                "access_username": "access_user_1",
                "access_user_groups": ["group:group1", "group:group2"],
            },
            {
                "*": ["READ"],
                "access_user_1": ["READ", "pause", "kill", "!stop"],
                "group:group1": ["CONTROL"],
            },
            id="Check group access permissions are added",
        ),
    ],
)
@patch("cylc.uiserver.authorise.get_groups")
def test_get_access_user_permissions_from_owner_conf(
    mocked_get_groups, expected_operations, access_user_dict, owner_auth_conf
):
    """Test the un-processed permissions of owner conf."""
    mocked_get_groups.return_value = (["group:blah"], [])
    authobj = Authorization(
        "some_user", owner_auth_conf, {"fake": "config"}, log
    )
    permitted_operations = authobj.get_access_user_permissions_from_owner_conf(
        access_user_dict
    )
    assert permitted_operations == expected_operations


@pytest.mark.parametrize(
    "permission_set, expected",
    [
        pytest.param(
            {"!kill", "READ", "kill", "!stop", "play"},
            {"play", "read"},
            id="Expansion with additions and negations",
        ),
        pytest.param(
            {"!CONTROL", "ALL"},
            {"broadcast", "read"},
            id="Check expansion and negation",
        ),
        pytest.param(
            {"READ", "!ALL", "broadcast", "CONTROL"},
            set(),
            id="Check expansion for !ALL with additions",
        ),
    ],
)
def test_expand_and_process_access_groups(permission_set, expected):
    authobj = Authorization(
        "some_user",
        {"fake": "config"},
        {"fake": "config"},
        log
    )
    actual = authobj.expand_and_process_access_groups(permission_set)
    assert actual == expected


@pytest.mark.parametrize(
    "mut_field_name, operation, expected_op_name",
    [
        pytest.param(
            "play",
            "mutation",
            "play",
            id="Mutation operation, play field, returns play",
        ),
        pytest.param(
            "_schema",
            "subscription",
            "read",
            id="Subscription operation, _schema field, returns read",
        ),
        pytest.param(
            "blah",
            "mutation",
            None,
            id="Mutation operation, invalid field, returns None",
        ),
        pytest.param(
            "workflows",
            "query",
            "read",
            id="Query operation, workflows field, returns read",
        ),
    ],
)
def test_get_op_name(mut_field_name, operation, expected_op_name):
    mock_authobj = Authorization(
        "some_user", {"fake": "config"},
        {"fake": "config"}, log
    )
    auth_middleware = AuthorizationMiddleware
    auth_middleware.auth = mock_authobj
    actual_op_name = auth_middleware.get_op_name(
        auth_middleware, mut_field_name, operation
    )
    assert actual_op_name == expected_op_name


@pytest.mark.parametrize(
    "owner_name,  user_name, get_permitted_operations_is_called, expected",
    [
        pytest.param(
            "mel",
            "mel",
            False,
            True,
            id="Owner user always permitted"
        ),
        pytest.param(
            "mel",
            "tim",
            True,
            True,
            id="User is not owner calls get_permitted_operations",
        ),
    ],
)
@patch("cylc.uiserver.authorise.get_groups")
def test_is_permitted(
    mocked_get_groups,
    owner_name,
    user_name,
    get_permitted_operations_is_called,
    expected,
):
    mocked_get_groups.side_effect = [([""], []), ([""], [])]
    auth_obj = Authorization(owner_name, FAKE_USER_CONF, FAKE_SITE_CONF, log)
    auth_obj.get_permitted_operations = Mock(return_value=["fake_operation"])
    actual = auth_obj.is_permitted(
        access_user=user_name, operation="fake_operation"
    )
    if get_permitted_operations_is_called:
        auth_obj.get_permitted_operations.assert_called_with(user_name)
    assert actual == expected


@pytest.mark.parametrize(
    "control, expected",
    [
        pytest.param(False, ALL_OPS, id="All ops returned"),
        pytest.param(True, CONTROL_OPS, id="Control ops returned"),
    ],
)
def test_get_list_of_mutations(control, expected):
    """Test ALL_OPS are returned"""
    actual = get_list_of_mutations(control=control)
    assert set(actual) == set(expected)


@pytest.mark.parametrize(
    'input_',
    (
        [123],
        [123, 456],
        [100, 123]
    )
)
def test_parse_group_ids(monkeypatch, input_):
    """Returns a list of group ids or groups where ID's haven't worked
    """
    mock_grid_db = {
        123: 'foo',
        456: 'bar',
    }
    monkeypatch.setattr(
        'grp.getgrgid', lambda x: SimpleNamespace(gr_name=mock_grid_db[x])
    )
    result = parse_group_ids(input_)
    assert result == (
        [
            f'group:{mock_grid_db[i]}'
            for i in input_ if i in mock_grid_db
        ],
        [
            i for i in input_ if i not in mock_grid_db
        ],
        )
