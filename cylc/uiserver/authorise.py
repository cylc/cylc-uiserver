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
from getpass import getuser
import grp
from inspect import iscoroutinefunction
import os
from typing import List, Optional, Union, Set, Tuple

import graphene
from jupyter_server.auth import Authorizer
from tornado import web

from cylc.uiserver.schema import UISMutations
from cylc.uiserver.utils import is_bearer_token_authenticated

from graphene.utils.str_converters import to_snake_case


class CylcAuthorizer(Authorizer):
    """Defines a safe default authorization policy for Jupyter Server.

    `Jupyter Server`_ provides an authorisation layer which gives full
    permissions to any user who has been granted permission to the Jupyter Hub
    ``access:servers`` scope
    (see :ref:`JupyterHub scopes reference <jupyterhub-scopes>`). This allows
    the execution of arbitrary code under another user account.

    To prevent this you must define an authorisation policy using
    :py:attr:`c.ServerApp.authorizer_class
    <jupyter_server.serverapp.ServerApp.authorizer_class>`.

    This class defines a policy which blocks all API calls to another user's
    server, apart from calls to Cylc interfaces explicitly defined in the
    :ref:`Cylc authorisation configuration <cylc.uiserver.user_authorization>`.

    This class is configured as the default authoriser for all Jupyter Server
    instances spawned via the ``cylc hubapp`` command. This is the default if
    you started `Jupyter Hub`_ using the ``cylc hub`` command. To see where
    this default is set, see this file for the appropriate release of
    cylc-uiserver:
    https://github.com/cylc/cylc-uiserver/blob/master/cylc/uiserver/jupyter_config.py

    If you are launching Jupyter Hub via another command (e.g. ``jupyterhub``)
    or are overriding :py:attr:`jupyterhub.app.JupyterHub.spawner_class`, then
    you will need to configure a safe authorisation policy e.g:

    .. code-block:: python

       from cylc.uiserver.authorise import CylcAuthorizer
       c.ServerApp.authorizer_class = CylcAuthorizer

    .. note::

       It is possible to provide read-only access to Jupyter Server extensions
       such as Jupyter Lab, however, this isn't advisable as Jupyter Lab does
       not apply file-system permissions to what another user is allowed to
       see.

       If you wish to grant users access to other user's Jupyter Lab servers,
       override this configuration with due care over what you choose to
       expose.

    """

    # This is here just to fix sphinx autodoc warning from traitlets' __init__
    # see https://github.com/cylc/cylc-uiserver/pull/560
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_authorized(self, handler, user, action, resource) -> bool:
        """Allow a user to access their own server.

        Note that Cylc uses its own authorization system (which is locked-down
        by default) and is not affected by this policy.
        """
        if is_bearer_token_authenticated(handler):
            # this session is authenticated by a token or password NOT by
            # Jupyter Hub -> the bearer of the token has full permissions
            return True

        # the username of the user running this server
        # (used for authorzation purposes)
        me = getuser()

        if user.username == me:
            # give the user full permissions to their own server
            return True

        # block access to everyone else
        return False


class Authorization:
    """Authorization configuration object.

    One instance of this class lives for the life of the UI Server.

    If authorization settings change the UI Server will need to be re-started
    to pick them up.

    Authorization has access groups: `READ`, `CONTROL`, `ALL` - along with
    their negations, `!READ`, `!CONTROL` and `!ALL` which indicate removal of
    the permission groups.

    Args:
        owner: The server owner's user name.
        owner_auth_conf: The server owner's authorization configuration.
        site_auth_conf: The site's authorization configuration.
        log: The application logger.

    """

    # config literals
    DEFAULT = "default"
    LIMIT = "limit"
    GRP_IDENTIFIER = "group:"

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
    READ_OPS = {READ_OPERATION}
    ASYNC_OPS = {"query", "mutation"}
    READ_AUTH_OPS = {"query", "subscription"}

    def __init__(
        self,
        owner_user_name: str,
        owner_auth_conf: dict,
        site_auth_conf: dict,
        log,
    ):
        self.owner_user_name: str = owner_user_name
        self.owner_user_groups: List[str] = self._get_groups(
            self.owner_user_name
        )
        self.log = log
        self.owner_auth_conf: dict = owner_auth_conf
        self.site_auth_config: dict = site_auth_conf
        self.owner_dict = self.build_owner_site_auth_conf()

        # lru_cache this method - see flake8-bugbear B019
        self.get_permitted_operations = lru_cache(maxsize=128)(
            self._get_permitted_operations
        )

    @property
    def ALL_OPS(self) -> List[str]:
        """ALL OPS constant, returns list of all mutations."""
        return get_list_of_mutations()

    @property
    def CONTROL_OPS(self) -> List[str]:
        """CONTROL OPS constant, returns list of all control mutations."""
        return get_list_of_mutations(control=True)

    def expand_and_process_access_groups(self, permission_set: set) -> set:
        """Process a permission set.

        Takes a permission set, e.g. limits, defaults.
        Expands the access groups and removes negated operations.

        Args:
            permission_set: set of permissions

        Returns:
            processed permission set.

        """
        # Expand permission groups
        # E.G. ALL -> ["read", "trigger", "broadcast", ...]
        for action_group, expansion in {
            Authorization.READ: Authorization.READ_OPS,
            Authorization.CONTROL: self.CONTROL_OPS,
            Authorization.ALL: self.ALL_OPS,
        }.items():
            if action_group in permission_set:
                permission_set.remove(action_group)
                permission_set.update(expansion)

        # Expand negated permission groups
        # E.G. !CONTROL -> ["!trigger", "!stop", "!pause", ...]
        for action_group, expansion in {
            Authorization.NOT_READ: [f"!{x}" for x in Authorization.READ_OPS],
            Authorization.NOT_CONTROL: [
                f"!{x}" for x in self.CONTROL_OPS
            ],
            Authorization.NOT_ALL: [
                f"!{x}" for x in self.ALL_OPS
            ],
        }.items():
            if action_group in permission_set:
                permission_set.remove(action_group)
                permission_set.update(expansion)

        # Remove negated permissions
        remove = set()
        for perm in permission_set:
            if perm.startswith("!"):
                remove.add(perm.lstrip("!"))
                remove.add(perm)
        permission_set.difference_update(remove)
        permission_set.discard("")

        return permission_set

    def get_owner_site_limits_for_access_user(
        self, access_user_name: str, access_user_groups: List[str]
    ) -> Set[str]:
        """Returns limits owner can give to given access_user

        Args:
            access_user_name: The username of the authenticated user.
            access_user_groups: All groups the authenticated user belongs to.

        Returns:
            Set of limits that the uiserver owner is allowed to give away
            for given access user.

        """
        limits: Set[str] = set()
        if not self.owner_dict:
            return limits
        items_to_check = ["*", access_user_name]
        items_to_check.extend(access_user_groups)
        for item in items_to_check:
            permission: Union[str, List] = ""
            default = ""
            with suppress(KeyError):
                default = self.owner_dict[item].get(Authorization.DEFAULT, "")
            with suppress(KeyError):
                permission = self.owner_dict[item].get(
                    Authorization.LIMIT, default
                )
            if permission == []:
                raise_auth_config_exception("site")
            if isinstance(permission, str):
                limits.add(permission)
            else:
                limits.update(permission)
        limits.discard("")
        return limits

    def get_access_user_permissions_from_owner_conf(
        self, access_user_name: str, access_user_groups: List[str]
    ) -> set:
        """
        Returns set of operations specific to access user from owner user conf.

        Args:
            access_user_name: The username of the authenticated user.
            access_user_groups: All groups the authenticated user belongs to.

        """
        items_to_check = ["*", access_user_name]
        items_to_check.extend(access_user_groups)
        allowed_operations = set()
        for item in items_to_check:
            permission = self.owner_auth_conf.get(item, "")
            # Specifiying empty list equates to removing of all permissions.
            if permission == []:
                raise_auth_config_exception("user")
            if isinstance(permission, str):
                allowed_operations.add(permission)
            else:
                allowed_operations.update(permission)
        allowed_operations.discard("")
        return allowed_operations

    # lru_cached - see __init__()
    def _get_permitted_operations(self, access_user: str):
        """Return permitted operations for given access_user.

        This method is cached for efficiency.

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
        # users have full access to their own server (ALL)
        if access_user == self.owner_user_name:
            return set(self.ALL_OPS)

        # all groups the authenticated user belongs to
        access_user_groups = self._get_groups(access_user)

        # the maximum permissions the site permits the user to grant
        limits_owner_can_give = self.get_owner_site_limits_for_access_user(
            access_user, access_user_groups
        )

        # the permissions the user wishes to grant
        user_conf_permitted_ops = (
            self.get_access_user_permissions_from_owner_conf(
                access_user, access_user_groups
            )
        )

        if len(user_conf_permitted_ops) == 0:
            # the user has not specified the permissions they wish to grant
            # -> fallback to the site defaults
            user_conf_permitted_ops = (
                self.return_site_auth_defaults_for_access_user(
                    access_user, access_user_groups
                )
            )

        # expand permission groups and remove negated permissions
        user_conf_permitted_ops = self.expand_and_process_access_groups(
            user_conf_permitted_ops
        )
        limits_owner_can_give = self.expand_and_process_access_groups(
            limits_owner_can_give
        )

        # subtract permissions that the site does not permit to be granted
        allowed_operations = limits_owner_can_give.intersection(
            user_conf_permitted_ops
        )

        self.log.info(
            f"User {access_user} authorized permissions: "
            f"{sorted(allowed_operations)}"
        )
        return allowed_operations

    def is_permitted(self, access_user: str, operation: str) -> bool:
        """Checks if user is permitted to action operation.

        Args:
            access_user: User attempting to action given operation.
            operation: operation name

        Returns:
            True if access_user permitted to action operation, otherwise,
            False.

        """
        if access_user == self.owner_user_name:
            return True

        # convert from GraphQL camel case to Python snake case
        operation = to_snake_case(operation)

        if operation in self.get_permitted_operations(access_user):
            self.log.info(f"{access_user}: authorized to {operation}")
            return True

        self.log.info(f"{access_user}: not authorized to {operation}")
        return False

    def build_owner_site_auth_conf(self):
        """Build UI Server owner permissions dictionary.

        Creates a reduced site auth dictionary for the ui-server owner.
        """
        owner_dict = {}
        items_to_check = ["*", self.owner_user_name]
        items_to_check.extend(self.owner_user_groups)

        # dict containing user info applying to the current ui_server owner
        for uis_owner_conf, access_user_dict in self.site_auth_config.items():
            if uis_owner_conf in items_to_check:
                # acc_user = access_user
                for acc_user_conf, acc_user_perms in access_user_dict.items():
                    existing_user_conf = owner_dict.get(acc_user_conf)
                    if existing_user_conf:
                        # process limits and defaults and update dictionary
                        existing_default = existing_user_conf.get(
                            Authorization.DEFAULT, ''
                        )
                        existing_limit = existing_user_conf.get(
                            Authorization.LIMIT, existing_default
                        )
                        new_default = acc_user_perms.get(
                            Authorization.DEFAULT, ''
                        )
                        new_limit = acc_user_perms.get(
                            Authorization.LIMIT, new_default
                        )
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
                        owner_dict[acc_user_conf][Authorization.LIMIT] = list(
                            set_lims
                        )
                        owner_dict[acc_user_conf][Authorization.DEFAULT] = (
                            list(set_defs)
                        )
                        continue
                    owner_dict.update(access_user_dict)
        # Now we have a reduced site auth dictionary for the current owner
        return owner_dict

    def return_site_auth_defaults_for_access_user(
        self, access_user_name: str, access_user_groups: List[str]
    ) -> Set:
        """Return site authorization defaults for given access user.

        Args:
            access_user_name: The username of the authenticated user.
            access_user_groups: All groups the authenticated user belongs to.

        Returns:
            The set of default operations permitted.

        """
        defaults: Set[str] = set()
        if not self.owner_dict:
            return defaults
        items_to_check = ["*", access_user_name]
        items_to_check.extend(access_user_groups)
        for item in items_to_check:
            permission: Union[str, List] = ""
            with suppress(KeyError):
                permission = self.owner_dict[item].get(
                    Authorization.DEFAULT, ""
                )
            if permission == []:
                raise_auth_config_exception("site")
            if isinstance(permission, str):
                defaults.add(permission)
            else:
                defaults.update(permission)
        defaults.discard("")
        return defaults

    def _get_groups(self, user: str) -> List[str]:
        """Allows get groups to use self.logger if something goes wrong.

        Added to provide a single interface for get_groups to this class, to
        avoid having to pass the logger to get_groups (and methods it calls).
        """
        good_groups, bad_groups = get_groups(user)
        if bad_groups:
            self.log.warning(
                f'{user} has the following invalid groups in their profile '
                f'{bad_groups} - these groups will be ignored.'
            )
        return good_groups


# GraphQL middleware
class AuthorizationMiddleware:
    """Authorization Middleware for authorization checking GraphQL.

    Mutations are checked against permissions from config files.

    Raises:
        web.HTTPError: Unauthorized requests.

    """

    auth = None

    def resolve(self, next_, root, info, **args):
        current_user = info.context["current_user"]
        # We won't be re-checking auth for return variables
        if len(info.path) > 1:
            return next_(root, info, **args)
        op_name = self.get_op_name(info.field_name, info.operation.operation)
        # It shouldn't get here but worth checking for zero trust
        if not op_name:
            self.auth_failed(
                current_user,
                op_name,
                http_code=400,
                msg="Operation not in schema.",
            )
        try:
            authorised = self.auth.is_permitted(current_user, op_name)
        except Exception:
            # Fail secure
            authorised = False
        if not authorised:
            self.auth_failed(current_user, op_name, http_code=403)
        if (
            info.operation.operation in Authorization.ASYNC_OPS
            or iscoroutinefunction(next_)
        ):
            return self.async_resolve(next_, root, info, **args)
        return next_(root, info, **args)

    def auth_failed(
        self,
        current_user: str,
        op_name: str,
        http_code: int,
        message: Optional[str] = None,
    ):
        """Raise an authorization error.

        Args:
            current_user: username accessing operation
            op_name: operation name
            http_code: http error code to raise
            message: Message to log Defaults to None.

        Raises:
            web.HTTPError

        """
        log_message = (
            f"Authorization failed for {current_user}"
            f":requested to {op_name}."
        )
        if message:
            log_message = log_message + " " + message
        raise web.HTTPError(http_code, reason=message)

    def get_op_name(self, field_name: str, operation: str) -> Optional[str]:
        """Returns the operation name required for authorization.

        Converts queries and subscriptions to read operations.

        Args:
            field_name: Field name e.g. play
            operation: operation type

        Returns:
            The operation name.

        """
        if operation in Authorization.READ_AUTH_OPS:
            return Authorization.READ_OPERATION

        # convert from GraphQL camel case to Python snake case
        field_name = to_snake_case(field_name)

        # Check it is a mutation in our schema
        if self.auth and field_name in self.auth.ALL_OPS:
            return field_name

        return None

    async def async_resolve(self, next_, root, info, **args):
        """Return awaited coroutine"""
        return await next_(root, info, **args)


def get_groups(username: str) -> Tuple[List[str], List[str]]:
    """Return a list of system groups for given user.

    Uses ``os.getgrouplist`` and ``os.NGROUPS_MAX`` to get system groups for a
    given user. ``grp.getgrgid`` then parses these to return a list of group
    names.

    Args:
        username: username used to check system groups.

    Returns:
        System groups for username given

    """
    groupmax = os.NGROUPS_MAX  # type: ignore
    group_ids = os.getgrouplist(username, groupmax)
    group_ids.remove(groupmax)
    # turn list of group_ids into group names with group identifier prepended
    return parse_group_ids(group_ids)


def parse_group_ids(group_ids: List) -> Tuple[List[str], List[str]]:
    """Returns list of groups in the correct format for authorisation.

    Args:
        group_ids: List of users groups, in number format

    Returns:
        List of users groups, in id format with group identifier prepended.

    """
    group_list = []
    bad_group_list = []
    for x in group_ids:
        try:
            group_list.append(
                f"{Authorization.GRP_IDENTIFIER}{grp.getgrgid(x).gr_name}"
            )
        except OverflowError:
            continue
        except KeyError:
            bad_group_list.append(x)
    return group_list, bad_group_list


def get_list_of_mutations(control: bool = False) -> List[str]:
    """Gets list of mutations"""
    list_of_mutations = [
        attr
        for attr in dir(UISMutations)
        if isinstance(getattr(UISMutations, attr), graphene.Field)
    ]
    if control:
        # Broadcast is an ALL mutation
        list_of_mutations.remove("broadcast")
    else:
        # 'read' is used soley for authorization and is not a UISMutation
        list_of_mutations.append(Authorization.READ_OPERATION)
    return list_of_mutations


def raise_auth_config_exception(config_type: str):
    """Error raise for empty list in auth config.

    Args:
        config_type: Either site or user.

    """
    raise Exception(
        f'Error in {config_type} config: '
        f'`c.CylcUIServer.{config_type}_authorization`. '
        f'"[]" is not supported. Use "{Authorization.NOT_ALL}" to remove all'
        ' permissions.'
    )
