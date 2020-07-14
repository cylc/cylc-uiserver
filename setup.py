# -*- coding: utf-8 -*-
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

import codecs
import re
import sys
from os.path import join, abspath, dirname

from setuptools import setup, find_namespace_packages

here = abspath(dirname(__file__))


def read(*parts):
    with codecs.open(join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# NB: We have cylc-flow at the top to force it to install its transitive
#     dependencies first. This way, if other dependencies (e.g. jupyterhub)
#     don't pin versions, we will get whatever cylc-flow needs, and not
#     the bleeding-edge version.
install_requires = [
    'cylc-flow==8.0a2',
    'jupyterhub==1.1.*',
    'tornado==6.0.*',
    'graphene-tornado==2.6.*',
    'graphql-core<3,>=2.1',  # TODO: graphql-python/graphql-ws#39
    'graphql-ws==0.3.*'
]

# Only include pytest-runner in setup_requires if we're invoking tests
if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_requires = ['pytest-runner']
else:
    setup_requires = []

tests_require = [
    'pytest',
    'coverage',
    'pytest-cov',
    'pytest-asyncio',
    'pytest-mock'
]

extras_require = {
    'tests': tests_require,
    'all': install_requires + tests_require
}

setup(
    version=find_version("cylc", "uiserver", "__init__.py"),
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    packages=find_namespace_packages(include=["cylc.*"]),
    package_data={
        'cylc.uiserver': [
            'logging_config.json'
        ]
    },
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'cylc-uiserver=cylc.uiserver.main:main'
        ]
    }
)
