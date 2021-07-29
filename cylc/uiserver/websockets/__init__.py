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

"""Websockets and subscriptions related code."""

from typing import (
    Awaitable,
    Callable,
    Optional,
    TYPE_CHECKING,
)
import functools
from tornado.web import HTTPError

if TYPE_CHECKING:
    from cylc.uiserver.handlers import CylcAppHandler


def authenticated(
    method: Callable[..., Optional[Awaitable[None]]]
) -> Callable[..., Optional[Awaitable[None]]]:
    """
    A decorator based on the original by tornado.web.authenticated.

    This decorator, different than the original, does not forward
    the user to the log-in form. If the user is not present, it
    fails immediately.

    This is necessary, as when establishing a WebSockets connection,
    the client may not be able to handle HTTP redirects.

    Args:
        method (Callable): The method to be decorated
    Returns:
        Callable: decorated method
    """
    @functools.wraps(method)
    def wrapper(  # type: ignore
            self: 'CylcAppHandler', *args, **kwargs
    ) -> Optional[Awaitable[None]]:
        if not self.current_user:
            self.log.debug('Unauthenticated WebSocket request!')
            raise HTTPError(403)

        return method(self, *args, **kwargs)

    return wrapper
