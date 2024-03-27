#!/usr/bin/env python3
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

"""
Cylc UI Server can be configured using a ``jupyter_config.py`` file, loaded
from a hierarchy of locations. This hierarchy includes the prepackaged
configuration, the site directory (which defaults to ``/etc/cylc/uiserver`` but
can be set with the environment variable ``$CYLC_SITE_CONF_PATH``) and
the user directory (``~/.cylc/uiserver``).
For example, at Cylc UI Server version 0.6.0, the hierarchy (highest priority
at the bottom) would be:

* ``cylc/uiserver/jupyter_config.py`` (pre-packaged default)
* ``/etc/cylc/uiserver/jupyter_config.py``
* ``/etc/cylc/uiserver/0/jupyter_config.py``
* ``/etc/cylc/uiserver/0.6/jupyter_config.py``
* ``/etc/cylc/uiserver/0.6.0/jupyter_config.py``
* ``~/.cylc/uiserver/jupyter_config.py``
* ``~/.cylc/uiserver/0/jupyter_config.py``
* ``~/.cylc/uiserver/0.6/jupyter_config.py``
* ``~/.cylc/uiserver/0.6.0/jupyter_config.py``


An example configuration might look like this:

.. code-block:: python

   # scan for workflows every 10 seconds
   c.CylcUIServer.scan_interval = 10

The Cylc UI Server is a `Jupyter Server`_ extension. For generic configuration
options see the Jupyter Servers documentation:
:external+jupyter_server:ref:`other-full-config`.
Cylc specific configurations are documented here.

.. note::

   ``c.CylcUIServer.site_authorization`` should be defined in
   ``/etc/cylc/uiserver/jupyter_config.py``, or, alternatively, via
   the environment variable ``CYLC_SITE_CONF_PATH``.
"""

from concurrent.futures import ProcessPoolExecutor
import getpass
import os
from pathlib import Path, PurePath
import sys
from textwrap import dedent
from typing import List

from pkg_resources import parse_version
from tornado import ioloop
from tornado.web import RedirectHandler
from traitlets import (
    Dict,
    Float,
    Int,
    TraitError,
    TraitType,
    Undefined,
    Unicode,
    default,
    validate,
)

from jupyter_server.extension.application import ExtensionApp

from cylc.flow.network.graphql import (
    CylcGraphQLBackend, IgnoreFieldMiddleware
)
from cylc.uiserver import (
    __file__ as uis_pkg,
)
from cylc.uiserver.authorise import (
    Authorization,
    AuthorizationMiddleware
)
from cylc.uiserver.data_store_mgr import DataStoreMgr
from cylc.uiserver.handlers import (
    CylcStaticHandler,
    CylcVersionHandler,
    SubscriptionHandler,
    UIServerGraphQLHandler,
    UserProfileHandler,
)
from cylc.uiserver.config_util import (
    get_conf_dir_hierarchy,
    SITE_CONF_ROOT,
    USER_CONF_ROOT
)
from cylc.uiserver.resolvers import Resolvers
from cylc.uiserver.schema import schema
from cylc.uiserver.websockets.tornado import TornadoSubscriptionServer
from cylc.uiserver.workflows_mgr import WorkflowsManager

INFO_FILES_DIR = Path(USER_CONF_ROOT / "info_files")


class PathType(TraitType):
    """A pathlib traitlet type which allows string and undefined values."""

    @property
    def info_text(self):
        return 'a pathlib.PurePath object'

    def validate(self, obj, value):
        if isinstance(value, str):
            return Path(value).expanduser()
        if isinstance(value, PurePath):
            return value
        if value == Undefined:
            return value
        self.error(obj, value)


class CylcUIServer(ExtensionApp):

    name = 'cylc'
    app_name = 'cylc-gui'
    load_other_extensions = True
    description = '''
    Cylc gui - A user interface for monitoring and controlling Cylc workflows.
    '''  # type: ignore[assignment]
    examples = dedent('''
    cylc gui                  # Start the Cylc GUI (at the dashboard page)
    cylc gui [workflow]       # Start the Cylc GUI (at the workflow page)
    cylc gui --new [workflow] # Start a new Cylc server instance if an old one
                              # has become unresponsive.
    cylc gui --no-browser     # Start the server but don't open the browser

    ''')  # type: ignore[assignment]
    config_file_paths = get_conf_dir_hierarchy(
        [
            SITE_CONF_ROOT,  # site configuration
            USER_CONF_ROOT,  # user configuration
        ], filename=False
    )
    # Next include currently needed for directory making
    config_file_paths.insert(0, str(Path(uis_pkg).parent))  # packaged config
    config_file_paths.reverse()
    # TODO: Add a link to the access group table mappings in cylc documentation
    # https://github.com/cylc/cylc-uiserver/issues/466
    AUTH_DESCRIPTION = '''
            Authorization can be granted at operation (mutation) level, i.e.
            specifically grant user access to execute Cylc commands, e.g.
            ``play``, ``pause``, ``edit``, ``trigger`` etc. For your
            convenience, these operations have been mapped to access groups
            ``READ``, ``CONTROL`` and ``ALL``.

            To remove permissions, prepend the access group or operation with
            ``!``.

            Permissions are additive but negated permissions take precedence
            above additions e.g. ``CONTROL, !stop`` will permit all operations
            in the ``CONTROL`` group except for ``stop``.

            .. note::

               Any authorization permissions granted to a user will be
               applied to all workflows.

            For more information, including the access group mappings, see
            :ref:`cylc.uiserver.multi-user`.
    '''

    site_authorization = Dict(
        config=True,
        help='''
            Dictionary containing site limits and defaults for authorization.

            This configuration should be placed only in the site set
            configuration file and not the user configuration file (use
            ``c.CylcUIServer.user_authorization`` for user defined
            authorization).

            If this configuration is empty, site authorization defaults to no
            configurable authorization and users will be unable to set any
            authorization.

            ''' + AUTH_DESCRIPTION + '''

            .. rubric:: Example Configuration:

            .. code-block:: python

               c.CylcUIServer.site_authorization = {
                   "*": {  # For all ui-server owners,
                       "*": {  # Any authenticated user
                           "default": "READ",  # Has default read access
                       },
                       "user1": {  # user1
                           "default": ["!ALL"],  # No privileges for all
                           # ui-server owners.
                       },  # No limit set, so all ui-server owners
                   },  # limit is also "!ALL" for user1
                   "server_owner_1": {  # For specific UI Server owner,
                       "group:group_a": {  # Any member of group_a
                           "default": "READ",  # Will have default read access
                           "limit": ["ALL", "!play"],  # server_owner_1 can
                       },  # grant All privileges, except play.
                   },
                   "group:grp_of_svr_owners": {  # Group of UI Server owners
                       "group:group_b": {
                           "limit": [  # can grant groupB users up to READ and
                               "READ",  # CONTROL privileges, without stop and
                               "CONTROL",  # kill
                               "!stop",
                               "!kill",  # No default, so default is no access
                           ],
                       },
                   },
               }

        ''')

    user_authorization = Dict(
        config=True,
        help='''
            Dictionary containing authorized users and permission levels for
            authorization.

            Use this setting to share control of your workflows
            with other users.

            Note that you are only permitted to give away permissions up to
            your limit for each user, as defined in the site_authorization
            configuration.

            ''' + AUTH_DESCRIPTION + '''

            Example configuration, residing in
            ``~/.cylc/uiserver/jupyter_config.py``:

            .. code-block:: python

               c.CylcUIServer.user_authorization = {
                   "*": ["READ"],  # any authenticated user has READ access
                   "group:group2": ["ALL"],  # Any user in system group2 has
                                             # access to all operations
                   "userA": ["ALL", "!stop"],  # userA has ALL operations, not
                                               # stop
               }

        '''
    )

    ui_path = PathType(
        config=False,
        help='''
            Path to the UI build to serve.

            Internal config derived from ui_build_dir and ui_version.
        '''
    )
    ui_build_dir = PathType(
        config=True,
        help='''
            The directory containing the UI build.

            This can be a directory containing a single UI build e.g::

               dir/
                   index.html

            Or a tree of builds where each build has a version number e.g::

               dir/
                   1.0/
                       index.html
                   2.0/
                       index.html

            By default this points at the UI build tree which was bundled with
            the UI Server. Change this if you want to pick up a different
            build e.g. for development or evaluation purposes.

            Takes effect on (re)start.
        '''
    )
    ui_version = Unicode(
        config=True,
        help='''
            Hardcodes the UI version to serve.

            If the ``ui_build_dir`` is a tree of builds, this config can be
            used to determine which UI build is used.

            By default the highest version is chosen according to PEP440
            version sorting rules.

            Takes effect on (re)start.
        '''
    )
    scan_interval = Float(
        config=True,
        help='''
            Set the interval between workflow scans in seconds.

            Workflow scans allow a UI server to detect workflows which have
            been started from the CLI since the last update.

            This involves a number of filesystem operations, to reduce
            system load set a higher value.
        ''',
        default_value=5.0  # default values as kwargs correctly display in docs
    )
    max_workers = Int(
        config=True,
        help='''
            Set the maximum number of workers for process pools.
        ''',
        default_value=1
    )
    max_threads = Int(
        config=True,
        help='''
            Set the maximum number of threads the Cylc UI Server can use.

            This determines the maximum number of active workflows that the
            server can track.
        ''',
        default_value=100,
    )

    @validate('ui_build_dir')
    def _check_ui_build_dir_exists(self, proposed):
        if proposed['value'].exists():
            return proposed['value']
        raise TraitError(f'ui_build_dir does not exist: {proposed["value"]}')

    @validate('site_authorization')
    def _check_site_auth_dict_correct_format(self, proposed):
        # TODO: More advanced auth dict validating
        if isinstance(proposed['value'], dict):
            return proposed['value']
        raise TraitError(
            f'Error in site authorization config: {proposed["value"]}')

    @staticmethod
    def _list_ui_versions(path: Path) -> List[str]:
        """Return a list of UI build versions detected in self.ui_path."""
        return sorted(
            (
                version.name
                for version in path.glob('[0-9][0-9.]*')
                if version
            ),
            key=parse_version
        )

    @default('ui_path')
    def _get_ui_path(self):
        build_dir = self.ui_build_dir
        version = self.ui_version

        if build_dir and build_dir != Undefined:
            # ui path has been configured, check if the path is a build
            # (rather than a dir of builds e.g. development build)
            if (build_dir / 'index.html').exists():
                return build_dir
        else:
            # default UI build base directory
            build_dir = Path(uis_pkg).parent / 'ui'

        if not version:
            # pick the highest installed version by default
            try:
                version = self._list_ui_versions(build_dir)[-1]
            except IndexError:
                raise Exception(
                    f'Could not find any UI builds in {build_dir}.'
                )

        ui_path = build_dir / version
        if (ui_path / 'index.html').exists():
            return ui_path

        raise Exception(f'Could not find UI build in {ui_path}')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = ProcessPoolExecutor(max_workers=self.max_workers)
        self.workflows_mgr = WorkflowsManager(self, log=self.log)
        self.data_store_mgr = DataStoreMgr(
            self.workflows_mgr,
            self.log,
            self.max_threads,
        )
        # sub_status dictionary storing status of subscriptions
        self.sub_statuses = {}
        self.resolvers = Resolvers(
            self.data_store_mgr,
            log=self.log,
            executor=self.executor,
            workflows_mgr=self.workflows_mgr,
        )

    def initialize_settings(self):
        """Update extension settings.

        Update the self.settings trait to pass extra settings to the underlying
        Tornado Web Application.

        self.settings.update({'<trait>':...})
        """
        super().initialize_settings()
        self.log.info("Starting Cylc UI Server")
        self.log.info(f'Serving UI from: {self.ui_path}')
        self.log.debug(
            'CylcUIServer config:\n' + '\n'.join(
                f'  * {key} = {repr(value)}'
                for key, value in self.config['CylcUIServer'].items()
            )
        )
        # start the async scan task running (do this on server start not init)
        ioloop.IOLoop.current().add_callback(
            self.workflows_mgr.run
        )
        # configure the scan interval
        ioloop.PeriodicCallback(
            self.workflows_mgr.scan,
            self.scan_interval * 1000
        ).start()

    def initialize_handlers(self):
        self.authobj = self.set_auth()
        self.set_sub_server()

        self.handlers.extend([
            (
                'cylc/version',
                CylcVersionHandler,
                {'auth': self.authobj}
            ),
            (
                'cylc/graphql',
                UIServerGraphQLHandler,
                {
                    'schema': schema,
                    'resolvers': self.resolvers,
                    'backend': CylcGraphQLBackend(),
                    'middleware': [
                        AuthorizationMiddleware,
                        IgnoreFieldMiddleware
                    ],
                    'auth': self.authobj,
                }
            ),
            (
                'cylc/graphql/batch',
                UIServerGraphQLHandler,
                {
                    'schema': schema,
                    'resolvers': self.resolvers,
                    'backend': CylcGraphQLBackend(),
                    'middleware': [
                        AuthorizationMiddleware,
                        IgnoreFieldMiddleware
                    ],
                    'batch': True,
                    'auth': self.authobj,
                }
            ),
            (
                'cylc/subscriptions',
                SubscriptionHandler,
                {
                    'sub_server': self.subscription_server,
                    'resolvers': self.resolvers,
                    'sub_statuses': self.sub_statuses
                }
            ),
            (
                'cylc/userprofile',
                UserProfileHandler,
                {'auth': self.authobj}
            ),
            (
                'cylc/(.*)?',
                CylcStaticHandler,
                {
                    'path': str(self.ui_path),
                    'default_filename': 'index.html'
                }
            ),
            (
                # redirect '/cylc' to '/cylc/'
                'cylc',
                RedirectHandler,
                {
                    'url': 'cylc/'
                }
            )
        ])

    def set_sub_server(self):
        self.subscription_server = TornadoSubscriptionServer(
            schema,
            backend=CylcGraphQLBackend(),
            middleware=[
                IgnoreFieldMiddleware,
                AuthorizationMiddleware,
            ],
            auth=self.authobj,
        )

    def set_auth(self):
        """Create authorization object.
        One for the lifetime of the UIServer.
        """
        return Authorization(
            getpass.getuser(),
            self.config.CylcUIServer.user_authorization,
            self.config.CylcUIServer.site_authorization,
            self.log
        )

    def initialize_templates(self):
        """Change the jinja templating environment."""

    @classmethod
    def launch_instance(cls, argv=None, workflow_id=None, **kwargs):
        if workflow_id:
            cls.default_url = f"/cylc/#/workspace/{workflow_id}"
        else:
            cls.default_url = "/cylc"
        if argv is None:
            # jupyter server isn't expecting to be launched by a Cylc command
            # this patches some internal logic
            argv = sys.argv[2:]
        os.environ["JUPYTER_RUNTIME_DIR"] = str(INFO_FILES_DIR)
        super().launch_instance(argv=argv, **kwargs)
        del os.environ["JUPYTER_RUNTIME_DIR"]

    async def stop_extension(self):
        # stop the async scan task
        await self.workflows_mgr.stop()
        for sub in self.data_store_mgr.w_subs.values():
            sub.stop()
        # Shutdown the thread pool executor
        self.data_store_mgr.executor.shutdown(wait=False)
        # Destroy ZeroMQ context of all sockets
        self.workflows_mgr.context.destroy()
