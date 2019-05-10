# -*- coding: utf-8 -*-
# Copyright (C) 2019 NIWA & British Crown (Met Office) & Contributors.
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

from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'jupyterhub==1.0.*',
    'tornado==6.0.*',
    'graphene-tornado==2.1.*'
]

setup_requires = [
    'pytest-runner==4.4.*'
]

tests_require = [
    'pytest==4.4.*',
    'coverage==4.5.*',
    'pytest-cov==2.6.*'
]

extras_require = {
    'tests': tests_require,
    'all': install_requires + tests_require
}

setup(
    name='cylc-uiserver',
    version='1.0',
    description='Cylc UI Server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cylc/cylc-uiserver/',
    py_modules=['handlers', 'cylc_singleuser'],
    python_requires='>=3.7',
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'cylc-singleuser=cylc_singleuser:main'
        ]
    }
)
