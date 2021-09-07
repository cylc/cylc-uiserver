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
from typing import List, Dict, Optional, Union, Any, Sequence, Set
from inspect import iscoroutinefunction
import logging
import os
from tornado import web
from traitlets.config.loader import LazyConfigValue
from traitlets.traitlets import Bool

logger = logging.getLogger(__name__)


class Authorization:
    """Authorization Information Class
    One instance for the life of the UI Server. If authorization settings
    change they will need to re-start the UI Server.
    Authorization has access groups: `READ`, `CONTROL`, `ALL` - along with
    their negations, `!READ`, `!CONTROL` and `!ALL` which indicate removal of
    the permission groups.

    """

    # config literals
    DEFAULT = 'default'
    LIMIT = 'limit'
    GRP_IDENTIFIER = 'group:'

    # Operations

    ##########################################################################
    #                               !WARNING!                                #
    #                                                                        #
    #   Beware of changing these permission groups. Users may be relying on  #
    #   these settings. Changes should be widely publicised to users.        #
    #                                                                        #
    #   If adding/removing operations, ensure documentation is updated.      #
    #                                                                        #
    ##########################################################################

    READ_OPERATION = "read"

    # Access group identifiers (used in config)

    READ = "READ"
    CONTROL = "CONTROL"
    ALL = "ALL"
    NOT_READ = "!READ"
    NOT_CONTROL = "!CONTROL"
    NOT_ALL = "!ALL"

    # Access Groups

    READ_OPS = [
        "ping",
        "read",
    ]

    CONTROL_OPS = [
        "ext-trigger",
        "pause",
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

    ALL_OPS = [
        "ping",
        "read",
        "broadcast",
        "ext-trigger",
        "pause",
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

    ASYNC_OPS = {'query', 'mutation'}
    READ_AUTH_OPS = {'query', 'subscription'}

    def __init__(self, owner, owner_auth_conf, site_auth_conf) -> None:
        self.owner = owner
        self.owner_auth_conf = self.set_auth_conf(owner_auth_conf)
        self.site_auth_config = self.set_auth_conf(site_auth_conf)
        self.owner_user_info = {
            'user': self.owner,
            'user_groups': get_groups(self.owner)}
        self.owner_dict = self.build_owner_site_auth_conf()
        self.get_permitted_operations = (
            lru_cache(maxsize=128)(self._get_permitted_operations))

    @staticmethod
    def set_auth_conf(auth_conf: Union[LazyConfigValue, dict]) -> dict:
        """Resolve lazy config where empty

        Args:
            auth_conf: Authorization configuration from a config.py

        Returns:
            Valid configuration dictionary
        """
        if (isinstance(auth_conf, LazyConfigValue) and
                not auth_conf.to_dict()):
            # no owner user auth - return empty dict
            return {}
        return auth_conf

    def get_owner_site_limits_for_access_user(
            self, access_user: Dict[str, Union[str, Sequence[Any]]]) -> Set:
        """Returns limits owner can give to given access_user

        Args:
            access_user: Dictionary containing info about access user and their
            membership of system groups.

        Returns:
            Set of limits that the uiserver owner is allowed to give away
            for given access user.
        """
        limits: Set[str] = set()
        if not self.owner_dict:
            return limits
        items_to_check = ['*', access_user['access_username']]
        items_to_check.extend(access_user['access_user_groups'])
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
            self, access_user: Dict[str, Union[str, Sequence[Any]]]) -> set:
        """
        Returns set of operations specific to access user from owner user conf.

        Args:
            access_user: Dictionary containing info about access user and their
            membership of system groups. Defaults to None.
        """
        items_to_check = ['*', access_user['access_username']]
        items_to_check.extend(access_user['access_user_groups'])
        allowed_operations = set()
        for item in items_to_check:
            permission = self.owner_auth_conf.get(item, '')
            if isinstance(permission, str):
                allowed_operations.add(permission)
            else:
                allowed_operations.update(permission)
        allowed_operations.discard('')
        return allowed_operations

    def _get_permitted_operations(self, access_user: str):
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
        # For use in the ui, owner permissions (ALL operations) are set
        if access_user == self.owner:
            return expand_and_process_access_groups(set(self.ALL_OPS))
        # Otherwise process permissions for (non-uiserver owner) access_user

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
            self, access_user: str, operation: str) -> Bool:
        """Checks if user is permitted to action operation.

        Args:
            access_user: User attempting to action given operation.
            operation: operation name

        Returns:
            True if access_user permitted to action operation, otherwise,
            False.
        """
        if access_user == self.owner_user_info['user']:
            return True
        logger.info(f'{access_user}: requested {operation}')
        if str(operation) in self.get_permitted_operations(access_user):
            logger.info(f'{access_user}: authorised to {operation}')
            return True
        logger.info(f'{access_user}: not authorised to {operation}')

        return False

    def build_owner_site_auth_conf(self):
        """Build UI Server owner permissions dictionary.
        Creates a reduced site auth dictionary for the ui-server owner.

        """
        owner_dict = {}
        items_to_check = [
            '*', self.owner_user_info['user']]
        items_to_check.extend(self.owner_user_info['user_groups'])

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
            self, access_user: Dict[str, Union[str, Sequence[Any]]]) -> Set:
        """Return site authorization defaults for given access user.
            Args:
                access_user: access_user dictionary, in the form
                            {'access_username': username
                             'access_user_group: [group1, group2,...]'
                            }
            Returns:
                Set of default operations permitted

        """
        defaults: Set[str] = set()
        if not self.owner_dict:
            return defaults
        items_to_check = ['*', access_user['access_username']]
        items_to_check.extend(access_user['access_user_groups'])
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

    def resolve(self, next_, root, info, **args):
        # We won't be re-checking auth for return variables
        if len(info.path) > 1:
            return next_(root, info, **args)
        op_name = self.get_op_name(info.field_name, info.operation.operation)
        # It shouldn't get here but worth checking for zero trust
        if not op_name:
            self.auth_failed(self.current_user, op_name, 400,
                             "Operation not in schema.")
        try:
            authorised = self.auth.is_permitted(self.current_user, op_name)
        except Exception:
            # Fail secure
            authorised = False
        if not authorised:
            self.auth_failed(self.current_user, op_name, 403)
        if (info.operation.operation in Authorization.ASYNC_OPS
                or iscoroutinefunction(next_)):
            return self.async_resolve(next_, root, info, **args)
        return next_(root, info, **args)

    @staticmethod
    def auth_failed(current_user: str, op_name: str,
                    http_code: int, message: Optional[str] = None):
        """
        Raise authorization error
        Args:
            current_user: username accessing operation
            op_name: operation name
            http_code: http error code to raise
            message: Message to log Defaults to None.

        Raises:
            web.HTTPError
        """
        log_message = (f"Authorization failed for {current_user}"
                       f":requested to {op_name}.")
        if message:
            log_message = log_message + " " + message
        logger.warning(log_message)
        raise web.HTTPError(http_code, reason=message)

    @staticmethod
    def get_op_name(field_name: str, operation: str) -> Union[None, str]:
        """
        Returns operation name required for authorization.
        Converts queries and subscriptions to read operations.
        Args:
            field_name: Field name e.g. play
            operation: operation type

        Returns:
            operation name
        """
        if operation in Authorization.READ_AUTH_OPS:
            return Authorization.READ_OPERATION
        else:
            # Check it is a mutation in our schema
            if field_name in Authorization.ALL_OPS:
                return field_name
        return None

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
    groupmax = os.NGROUPS_MAX  # type: ignore
    group_ids = os.getgrouplist(username, groupmax)
    group_ids.remove(groupmax)
    # turn list of group_ids into group names with group identifier prepended
    return list(map(
        lambda x: f'{Authorization.GRP_IDENTIFIER}{grp.getgrgid(x).gr_name}',
        group_ids
        )
    )


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
        Authorization.CONTROL: Authorization.CONTROL_OPS,
        Authorization.ALL: Authorization.ALL_OPS,
            Authorization.READ: Authorization.READ_OPS}.items():
        if action_group in permission_set:
            permission_set.remove(action_group)
            permission_set.update(expansion)
    # Expand negated permissions
    for action_group, expansion in {
            Authorization.NOT_CONTROL: list(
                map((lambda x: '!' + x), Authorization.CONTROL_OPS)),
            Authorization.NOT_ALL: list(
                map((lambda x: '!' + x), Authorization.ALL_OPS)),
            Authorization.NOT_READ: list(
                map((lambda x: '!' + x), Authorization.READ_OPS))}.items():
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
