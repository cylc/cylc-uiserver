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

from contextlib import suppress
from functools import lru_cache
import grp
from typing import List, Dict
from graphql.utils.ast_to_dict import ast_to_dict
from inspect import iscoroutinefunction
import logging
import os
from tornado import web

logger = logging.getLogger(__name__)


class Authorization:
    # config literals
    DEFAULT = 'default'
    LIMIT = 'limit'
    GROUP_IDENTIFIER = 'group:'

    # Operations

    READ = [
        "ping",
        "read",
    ]
    CONTROL = [
        "ext-trigger",
        "hold",
        "kill",
        "message",
        "pause",
        "play",
        "poll",
        "release",
        "releaseholdpoint",
        "reload",
        "remove",
        "resume",
        "setgraphwindowextent",
        "setholdpoint",
        "setoutputs",
        "setverbosity",
        "stop",
        "trigger",
    ]

    ALL = [
        "ping",
        "read",
        "broadcast",
        "ext-trigger",
        "hold",
        "kill",
        "message",
        "pause",
        "play",
        "poll",
        "release",
        "releaseholdpoint",
        "reload",
        "remove",
        "resume",
        "setgraphwindowextent",
        "setholdpoint",
        "setoutputs",
        "setverbosity",
        "stop",
        "trigger",
    ]

    NOT_READ = [
        "!ping",
        "!read",
    ]

    NOT_CONTROL = [
        "!broadcast",
        "!ext-trigger",
        "!hold",
        "!kill",
        "!message",
        "!pause",
        "!play",
        "!poll",
        "!release",
        "!releaseholdpoint",
        "!reload",
        "!remove",
        "!resume",
        "!setgraphwindowextent",
        "!setholdpoint",
        "!setoutputs",
        "!setverbosity",
        "!stop",
        "!trigger",
    ]

    NOT_ALL = [
        "!broadcast",
        "!ping",
        "!read",
        "!broadcast",
        "!ext-trigger",
        "!hold",
        "!kill",
        "!message",
        "!pause",
        "!play",
        "!poll",
        "!release",
        "!releaseholdpoint",
        "!reload",
        "!remove",
        "!resume",
        "!setgraphwindowextent",
        "!setholdpoint",
        "!setoutputs",
        "!setverbosity",
        "!stop",
        "!trigger"
    ]

    def __init__(self, owner, owner_conf, site_conf) -> None:
        self.owner_user_info = {'user': owner,
                                'user_groups': get_groups(owner)}
        # owner_user_info = {'user': # getpass.getuser(),
        #      'user_groups': ['vmuser', 'group2']
        #      }
        self.auth_users_perms = {}
        # stores {usernames: permitted_operations}
        self.site_auth_config = site_conf
        self.owner_auth_conf = owner_conf
        self.set_owner_site_auth_conf()

    def query_site_conf_for_permission_limits(self, access_user=None):
        """Query ui-servers site conf
            Args:

            Returns:
            Set of limits that the uiserver owner is allowed to give away
            for specified user.
        """
        try:
            items_to_check = ['*', access_user['access_username']]
            for access_group in access_user['access_user_groups']:
                items_to_check.append(
                    f'{Authorization.GROUP_IDENTIFIER}{access_group}'
                )
            limits = set()
            for item in items_to_check:
                with suppress(KeyError):
                    permission = self.owner_dict[item].get(
                        Authorization.LIMIT,
                        self.owner_dict[item].get(Authorization.DEFAULT, '')
                    )
                if isinstance(permission, str):
                    limits.add(permission)
                else:
                    limits.update(permission)
        except Exception as ex:
            print(f'dsd{ex}')
        return self.expand_and_process_access_groups(limits)

    def check_user_permitted_in_owner_conf(self, access_user=None):
        """[summary]

        Args:
            uiserver_owner_conf ([type], optional): [description].
            access_user ([type], optional): [description]. Defaults to None.
        """
        items_to_check = ['*', access_user['access_username']]
        for access_group in access_user['access_user_groups']:
            items_to_check.append(
                f'{Authorization.GROUP_IDENTIFIER}{access_group}'
            )
        allowed_operations = set()
        for item in items_to_check:
            with suppress(KeyError):
                permission = self.owner_auth_conf.get(item, "")
            if isinstance(permission, str):
                allowed_operations.add(permission)
            else:
                allowed_operations.update(permission)
        return self.expand_and_process_access_groups(
            allowed_operations
        )

    @lru_cache(maxsize=128)
    def get_permitted_operations(self, access_user: str):
        """Return permitted operations for given access_user.

        Cached for efficiency.
        Checks:
        - site config to ensure owner is permitted to give away permissions
        - user config for authorised operations related to access_user and
          their groups
        - if user not in user config, then returns defaults from site config.

        Args:
            access_user: username to check for permitted operations

        Returns:


        """

        access_user_dict = {'access_username': access_user,
                            'access_user_groups': get_groups(access_user)
                            }
        limits_owner_can_give = self.query_site_conf_for_permission_limits(
            access_user=access_user_dict)
        user_conf_permitted_ops = self.check_user_permitted_in_owner_conf(
            access_user=access_user_dict)
        allowed_operations = limits_owner_can_give.intersection(
            user_conf_permitted_ops)
        # If not explicit permissions for user, revert to site defaults
        if len(allowed_operations) == 0:
            allowed_operations = (
                self.return_site_auth_defaults_for_access_user(
                    access_user=access_user_dict))
        return allowed_operations

    def is_permitted(self, access_user, operation):
        if isinstance(access_user, Dict):
            access_user = access_user['name']
        if access_user == self.owner_user_info['user']:
            print("its meeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            return True
        logger.info(f'{access_user}: requested {operation}')
        print(
            f"allowed operations are these: {self.get_permitted_operations(access_user)} for user: {access_user}")
        if str(operation) in self.get_permitted_operations(access_user):
            logger.info(f'{access_user}: authorised to {operation}')
            return True
        logger.info(f'{access_user}: not authorised to {operation}')

        return False

    def set_owner_site_auth_conf(self):
        """Get UI Server owner permissions dictionary.

        Args:
            owner_user_info: Dictionary containing information about
                             the ui-server owner Defaults to None.
            site_config: Defaults to None....
            : Optional[
                Dict[str: Dict[
                    str: Dict[
                        str: Union[List[str], None]
                        ]]]]
        """
        # concerned with process site config
        self.owner_user_info['user_groups'] = ([
            f'{Authorization.GROUP_IDENTIFIER}{group}'
            for group in self.owner_user_info[
                'user_groups']
        ])
        owner_dict = {}
        items_to_check = [
            '*', self.owner_user_info['user']]
        items_to_check.extend(self.owner_user_info['user_groups'])

        # dict containing user info applying to the current ui_server owner
        for uis_owner_conf, access_user_dict in self.site_auth_config.items():
            if uis_owner_conf in items_to_check:
                owner_dict.update(access_user_dict)

        # Now we have a dictionary for the current owner which can be
        #  cached and
        # used for reference for anyone accessing this uiserver
        # format of dictionary created:
        # { users: {default:[],
        #           limit:[]
        # }
        # where user can be *, username or group:groupname
        # At this point missing defaults and limits have not been filled in

        self.owner_dict = owner_dict

    def expand_and_process_access_groups(self, permission_set: set) -> set:
        """Process a permission set.

        Takes a permission set, e.g. limits, defaults.
        Expands the access groups and removes negated operations.

        Args:
            permission_set: set of permissions

        Returns:
            permission_set: processed permission set.
        """
        for action_group, expansion in {
            "CONTROL": Authorization.CONTROL,
            "ALL": Authorization.ALL,
                "READ": Authorization.READ}.items():
            if action_group in permission_set:
                permission_set.remove(action_group)
                permission_set.update(expansion)
        # Expand negated permissions
        for action_group, expansion in {
            "!CONTROL": Authorization.NOT_CONTROL,
            "!ALL": Authorization.NOT_ALL,
            "!READ": Authorization.NOT_READ
        }.items():
            if action_group in permission_set:
                permission_set.remove(action_group)
                permission_set.update(expansion)
        # Remove negated permissions
        remove = set()
        for perm in permission_set:
            if perm.startswith("!"):
                with suppress(KeyError):
                    remove.add(perm.lstrip("!"))
                    remove.add(perm)
        permission_set.difference_update(remove)
        return permission_set

    def return_site_auth_defaults_for_access_user(
            self, access_user):
        """Return site authorisation defaults for given access user.
            Args:
                access_user: access_user dictionary, in the form
                            {'access_username': username
                             'access_user_group: [group1, group2,...]'
                            }
            Returns:
                Set of default operations permitted

        """
        items_to_check = ['*', access_user['access_username']]
        print(items_to_check)
        for access_group in access_user['access_user_groups']:
            items_to_check.append(
                f'{Authorization.GROUP_IDENTIFIER}{access_group}'
            )
        print(items_to_check)
        defaults = set()
        for item in items_to_check:
            with suppress(KeyError):  # item not in config
                permission = self.owner_dict[item].get(
                    Authorization.DEFAULT, ''
                )
            if isinstance(permission, str):
                defaults.add(permission)
            else:
                defaults.update(permission)
        print(defaults)
        # Deal with additions of permissions...
        defaults = self.expand_and_process_access_groups(defaults)
        print(defaults)
        return defaults

# GraphQL middleware


class AuthorizationMiddleware:

    auth = None
    current_user = None

    ASYNC_OPS = {'query', 'mutation'}
    READ_AUTH_OPS = {'query', 'subscription'}

    def resolve(self, next, root, info, **args):
        try:
            if info.operation.operation:
                print(
                    f"info.operation.operation is ths....{info.operation.operation}")
            else:
                print("no info.operation.operation")
            if info.parent_type.name:
                print(
                    f"info.parent_type.name is ths....{info.parent_type.name}")
            else:
                print("No info.parent_type.name")
            if info.field_name:
                print(f"info.field_name:{info.field_name}")
            else:
                print("no info.field_name")
            authorised = False
            # We won't be re-checking auth for return variables
            # TODO confirm GraphQL mutations won't be nested
            if len(info.path) > 1:
                return
            if (info.operation.operation in self.READ_AUTH_OPS and
                    self.auth.is_permitted(self.current_user, 'read')):
                # check user is allowed to READ
                authorised = True
            # Check it is a mutation in our schema

            elif (
                (info.parent_type.name.lower() in ['uismutations', Authorization.ALL]) and
                    self.auth.is_permitted(
                        self.current_user, info.operation.operation)):
                authorised = True

            if not authorised:
                logger.warn(
                    f"Authorisation failed for {self.current_user}")
                raise web.HTTPError(403)

            if (
                info.operation.operation in self.ASYNC_OPS
                or iscoroutinefunction(next)
            ):
                return self.async_resolve(next, root, info, **args)
            return next(root, info, **args)
        except Exception as exc:
            print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{exc}')

    async def async_resolve(self, next, root, info, **args):
        """Return awaited coroutine"""
        return await next(root, info, **args)

    @staticmethod
    def op_names(ast):
        node = ast_to_dict(ast)
        for leaf in node['selections']:
            if leaf['kind'] == 'Field':
                yield leaf['name']['value']


def get_groups(username: str) -> List:
    """Return list of system groups for given user

    Args:
        username: username used to check system groups.

    Returns:
        list: system groups for username given
    """

    group_ids = os.getgrouplist(username, 99999)
    group_ids.remove(99999)
    return list(map(lambda x: grp.getgrgid(x).gr_name, group_ids))
