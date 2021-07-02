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
from dataclasses import dataclass
from functools import lru_cache
import grp
from typing import List, Dict, Union, Any, Sequence
from graphql.execution.base import ResolveInfo
from inspect import iscoroutinefunction
import logging
import os
from tornado import web
from traitlets.config.loader import LazyConfigValue
from traitlets.traitlets import Bool

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Authorization:
    """Authorization Information Class
    One instance per uiserver (frozen)
        
    """
    owner:str 
    owner_auth_conf: Dict
    site_auth_config: Dict
    owner_user_info = {}
    
     
    # config literals
    DEFAULT = 'default'
    LIMIT = 'limit'
    GROUP_IDENTIFIER = 'group:'

    # Operations

    READ_OP = 'read'

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

    def __post_init__(self) -> None:
        import mdb
        mdb.debug()
        object.__setattr__(self,'owner_user_info',{
            'user': self.owner,
            'user_groups': get_groups(self.owner)})
        object.__setattr__(self,'owner_dict', self.set_owner_site_auth_conf())
        

    def get_owner_site_limits_for_access_user(
            self, access_user: Dict[str, Union[str, Sequence[Any]]]) -> set:
        """Returns limits owner can give to given access_user
            Args:
            access_user: Dictionary containing info about access user and their
            membership of system groups.
            Returns:
            Set of limits that the uiserver owner is allowed to give away
            for given access user.
        """
        items_to_check = ['*', access_user['access_username']]
        for access_group in access_user['access_user_groups']:
            if access_group:
                items_to_check.append(
                    f'{Authorization.GROUP_IDENTIFIER}{access_group}'
                )
        limits = set()
        for item in items_to_check:
            permission = ''
            default = ''
            with suppress(KeyError):
                default = self.owner_dict[item].get(Authorization.DEFAULT, '')
            with suppress(KeyError):
                permission = self.owner_dict[item].get(
                    Authorization.LIMIT,
                    default)
            if isinstance(permission, str):
                limits.add(permission)
            else:
                limits.update(permission)
        limits.discard('')
        return limits

    def get_access_user_permissions_from_owner_conf(
            self, access_user: Dict[str, Union[str, Sequence[Any]]]):
        """
        Checks access user has permissions in the ui server owner user conf.
        Args:
            access_user: Dictionary containing info about access user and their
            membership of system groups. Defaults to None.
        """
        items_to_check = ['*', access_user['access_username']]
        for access_group in access_user['access_user_groups']:
            items_to_check.append(
                f'{Authorization.GROUP_IDENTIFIER}{access_group}'
            )
        allowed_operations = set()
        for item in items_to_check:
            permission = self.owner_auth_conf.get(item, '')
            if isinstance(permission, str):
                allowed_operations.add(permission)
            else:
                allowed_operations.update(permission)
        allowed_operations.discard('')
        return allowed_operations

    @lru_cache(128)
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
            Set of operations permitted by given access user for this UI Server
        """
        access_user_dict = {'access_username': access_user,
                            'access_user_groups': get_groups(access_user)
                            }
        limits_owner_can_give = self.get_owner_site_limits_for_access_user(
            access_user=access_user_dict)
        user_conf_permitted_ops = (
            self.get_access_user_permissions_from_owner_conf(
                access_user=access_user_dict)
            )
        # If not explicit permissions for access user in owner conf then revert
        # to site defaults
        if len(user_conf_permitted_ops) == 0:
            user_conf_permitted_ops = (
                self.return_site_auth_defaults_for_access_user(
                    access_user=access_user_dict))
        user_conf_permitted_ops = expand_and_process_access_groups(
            user_conf_permitted_ops)
        limits_owner_can_give = expand_and_process_access_groups(
            limits_owner_can_give)
        allowed_operations = limits_owner_can_give.intersection(
            user_conf_permitted_ops)
        return allowed_operations

    def is_permitted(
            self, access_user: Union[str, Dict], operation: str) -> Bool:
        """Checks if user is permitted to action operation.

        Args:
            access_user: User attempting to action given operation.
            operation: operation name

        Returns:
            True if access_user permitted to action operation, otherwise,
            False.
        """
        breakpoint()
        if isinstance(access_user, Dict):
            access_user = access_user['name']
        # if access_user == self.owner_user_info['user']:
        #     return True
        logger.info(f'{access_user}: requested {operation}')
        if str(operation) in self.get_permitted_operations(access_user):
            logger.info(f'{access_user}: authorised to {operation}')
            return True
        logger.info(f'{access_user}: not authorised to {operation}')

        return False

    def set_owner_site_auth_conf(self):
        """Get UI Server owner permissions dictionary.
        """
        owner_dict = {}
        if (isinstance(self.site_auth_config, LazyConfigValue) and
                not self.site_auth_config.to_dict()):
            # no site auth - return empty dict
            self.owner_dict = owner_dict
            return
        # concerned with process site config
        self.owner_user_info['user_groups'] = ([
            f'{Authorization.GROUP_IDENTIFIER}{group}'
            for group in self.owner_user_info[
                'user_groups']
        ])
        items_to_check = [
            '*', self.owner_user_info['user']]
        items_to_check.extend(self.owner_user_info['user_groups'])
        if not self.site_auth_config:
            return owner_dict
        # dict containing user info applying to the current ui_server owner
        for uis_owner_conf, access_user_dict in self.site_auth_config.items():
            if uis_owner_conf in items_to_check:
                # acc_user = access_user
                for acc_user_conf, acc_user_perms in access_user_dict.items():
                    with suppress(KeyError):
                        existing_user_conf = owner_dict.get(acc_user_conf)
                    if existing_user_conf:
                        # process limits and defaults and update dictionary
                        existing_default = existing_user_conf.get(
                            Authorization.DEFAULT, '')
                        existing_limit = existing_user_conf.get(
                            Authorization.LIMIT, existing_default)
                        new_default = acc_user_perms.get(
                            Authorization.DEFAULT, '')
                        new_limit = acc_user_perms.get(
                            Authorization.LIMIT, new_default)
                        set_defs = set()
                        for conf in [existing_default, new_default]:
                            if isinstance(conf, list):
                                set_defs.update(conf)
                            else:
                                set_defs.add(conf)
                        set_lims = set()
                        for conf in [existing_limit, new_limit]:
                            if isinstance(conf, list):
                                set_lims.update(conf)
                            else:
                                set_lims.add(conf)
                        # update and continue
                        owner_dict[
                            acc_user_conf][Authorization.LIMIT] = list(
                            set_lims)
                        owner_dict[
                            acc_user_conf][Authorization.DEFAULT] = list(
                            set_defs)
                        continue
                    owner_dict.update(access_user_dict)
        # Now we have a reduced site auth dictionary for the current owner
        return owner_dict

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
        for access_group in access_user['access_user_groups']:
            items_to_check.append(
                f'{Authorization.GROUP_IDENTIFIER}{access_group}'
            )
        defaults = set()
        for item in items_to_check:
            permission = ''
            with suppress(KeyError):
                permission = self.owner_dict[item].get(
                    Authorization.DEFAULT, ''
                )
            if isinstance(permission, str):
                defaults.add(permission)
            else:
                defaults.update(permission)
        defaults.discard('')
        return defaults


# GraphQL middleware
class AuthorizationMiddleware:

    auth = None
    current_user = None

    ASYNC_OPS = {'query', 'mutation'}
    READ_AUTH_OPS = {'query', 'subscription'}

    def resolve(self, next_, root, info, **args):
        # # We won't be re-checking auth for return variables
        # # TODO confirm GraphQL mutations won't be nested
        if len(info.path) > 1:
            return next_(root, info, **args)
        # Check user is allowed to READ
        authorised, op_name = self.process_auth(info)
        if not authorised:
            logger.warn(
                f"Authorisation failed for {self.current_user}"
                f":requested to {op_name}"
            )
            raise web.HTTPError(403)

        if (
            info.operation.operation in self.ASYNC_OPS
            or iscoroutinefunction(next_)
        ):
            return self.async_resolve(next_, root, info, **args)
        return next_(root, info, **args)

    def process_auth(self, info):
        authorised = False
        if (info.operation.operation in self.READ_AUTH_OPS and
                self.auth.is_permitted(
                    self.current_user, Authorization.READ_OP)):
            op_name = Authorization.READ_OP
            authorised = True
        else:
            # Check it is a mutation in our schema
            if (isinstance(info, ResolveInfo) and info.field_name and
                    info.field_name in Authorization.ALL):
                op_name = info.field_name
            elif info.operation.operation in Authorization.ALL:
                op_name = info.operation.operation

            if (info.parent_type.name.lower() in
                    'uismutations' and op_name and
                    self.auth.is_permitted(
                        self.current_user, op_name)):
                authorised = True
        return authorised, op_name

    async def async_resolve(self, next_, root, info, **args):
        """Return awaited coroutine"""
        return await next_(root, info, **args)


def get_groups(username: str) -> List[str]:
    """Return list of system groups for given user

    Args:
        username: username used to check system groups.

    Returns:
        list: system groups for username given
    """

    group_ids = os.getgrouplist(username, 99999)
    group_ids.remove(99999)
    return list(map(lambda x: grp.getgrgid(x).gr_name, group_ids))


def expand_and_process_access_groups(permission_set: set) -> set:
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
    permission_set.discard('')
    return permission_set
