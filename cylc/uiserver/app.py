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

from pathlib import Path, PurePath
import sys
from typing import List

from pkg_resources import parse_version
from tornado import web, ioloop
from tornado.web import RedirectHandler
from traitlets import (
    Float,
    TraitError,
    TraitType,
    Undefined,
    Unicode,
    default,
    validate,
)

from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.application import ExtensionApp
# from jupyterhub.utils import url_path_join
import tornado

from cylc.flow.network.graphql import (
    CylcGraphQLBackend, IgnoreFieldMiddleware
)

from cylc.uiserver import (
    __file__ as uis_pkg
)
from cylc.uiserver.data_store_mgr import DataStoreMgr
from cylc.uiserver.handlers import (
    SubscriptionHandler,
    UIServerGraphQLHandler,
    UserProfileHandler,
    CylcStaticHandler
)
from cylc.uiserver.resolvers import Resolvers
from cylc.uiserver.schema import schema
from cylc.uiserver.websockets.tornado import TornadoSubscriptionServer
from cylc.uiserver.workflows_mgr import WorkflowsManager


class MyExtensionHandler(JupyterHandler):

    @tornado.web.authenticated
    def get(self):
        self.write('hello cylc')

    @tornado.web.authenticated
    def post(self):
        ...


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
    default_url = "/cylc"
    load_other_extensions = True
    # file_url_prefix = "/render"
    description = '''
    Cylc - A user interface for monitoring and controlling Cylc workflows.
    '''
    examples = '''
        cylc gui    # start the cylc GUI
    '''
    config_file_paths = list(
        map(
            str,
            [
                # base configuration - always used
                Path(uis_pkg).parent,
                # site configuration
                Path('/etc/cylc/hub'),
                # user configuration
                Path('~/.cylc/hub').expanduser()
            ]
        )
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
    logging_config = PathType(
        config=True,
        help='''
            Set the path to a logging config JSON file.

            This configures what gets logged where.

            For more information on logging configuration see:
            https://docs.python.org/3/library/logging.config.html

            Currently only JSON format is supported.

            If unspecified the default config located in
            ``cylc/uiserver/logging_config.json`` will apply.
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
        '''
    )

    @default('scan_interval')
    def _default_scan_interval(self):
        return 5

    @validate('ui_build_dir')
    def _check_ui_build_dir_exists(self, proposed):
        if proposed['value'].exists():
            return proposed['value']
        raise TraitError(f'ui_build_dir does not exist: {proposed["value"]}')

    @staticmethod
    def _list_ui_versions(path: Path) -> List[str]:
        """Return a list of UI build versions detected in self.ui_path."""
        return list(
            sorted(
                (
                    version.name
                    for version in path.glob('[0-9][0-9.]*')
                    if version
                ),
                key=parse_version
            )
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

    @default('logging_config')
    def _default_logging_config(self):
        return Path(Path(uis_pkg).parent / 'logging_config.json')

    @default('static_dir')
    def _get_static_dir(self):
        return str(self.ui_path)

    @default('static_paths')
    def _get_static_paths(self):
        return [str(self.ui_path)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workflows_mgr = WorkflowsManager(self, log=self.log)
        self.data_store_mgr = DataStoreMgr(self.workflows_mgr, self.log)
        self.resolvers = Resolvers(
            self.data_store_mgr,
            log=self.log,
            workflows_mgr=self.workflows_mgr,
        )
        self.subscription_server = TornadoSubscriptionServer(
            schema,
            backend=CylcGraphQLBackend(),
            middleware=[IgnoreFieldMiddleware],
        )

        ioloop.IOLoop.current().add_callback(
            self.workflows_mgr.update
        )
        ioloop.PeriodicCallback(
            self.workflows_mgr.update,
            self.scan_interval * 1000
        ).start()

    def initialize_settings(self):
        """Update extension settings.

        Update the self.settings trait to pass extra settings to the underlying
        Tornado Web Application.

        self.settings.update({'<trait>':...})
        """
        super().initialize_settings()
        self.log.info("Starting Cylc UI Server")
        self.log.info(f'Serving UI from: {self.ui_path}')

    def initialize_handlers(self):
        self.handlers.extend([
            ('cylc/hello', MyExtensionHandler),
            (
                'cylc/graphql',
                UIServerGraphQLHandler,
                {
                    'schema': schema,
                    'resolvers': self.resolvers,
                    'backend': CylcGraphQLBackend(),
                    'middleware': [IgnoreFieldMiddleware],
                }
            ),
            (
                'cylc/graphql/batch',
                UIServerGraphQLHandler,
                {
                    'schema': schema,
                    'resolvers': self.resolvers,
                    'backend': CylcGraphQLBackend(),
                    'middleware': [IgnoreFieldMiddleware],
                    'batch': True,
                }
            ),
            (
                'cylc/subscriptions',
                SubscriptionHandler,
                {
                    'sub_server': self.subscription_server,
                    'resolvers': self.resolvers,
                }
            ),
            (
                'cylc/userprofile',
                UserProfileHandler,
            ),
            (
                'cylc/(.*)?',
                # web.StaticFileHandler,
                CylcStaticHandler,
                {
                    'path': str(self.ui_path),
                    'default_filename': 'index.html'
                    # 'url': url_path_join(
                    #     self.static_url_prefix, 'index.html'
                    # )
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

    def initialize_templates(self):
        """Change the jinja templating environment."""

    @classmethod
    def launch_instance(cls, argv=None, **kwargs):
        if argv is None:
            # jupyter server isn't expecting to be launched by a Cylc command
            # this patches some internal logic
            argv = sys.argv[2:]
        super().launch_instance(argv=argv, **kwargs)

    def stop_extension(self):
        for sub in self.data_store_mgr.w_subs.values():
            sub.stop()
        # Shutdown the thread pool executor
        for executor in self.data_store_mgr.executors.values():
            executor.shutdown(wait=False)
        # Destroy ZeroMQ context of all sockets
        self.workflows_mgr.context.destroy()
        ioloop.IOLoop.instance().stop()
        self.log.info('exit success')
