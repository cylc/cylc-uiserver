[![Build Status](https://travis-ci.org/cylc/cylc-uiserver.svg?branch=master)](https://travis-ci.org/cylc/cylc-uiserver)
[![codecov](https://codecov.io/gh/cylc/cylc-uiserver/branch/master/graph/badge.svg)](https://codecov.io/gh/cylc/cylc-uiserver)

# Cylc UI Server

This project contains the Cylc UI Server. A JupyterHub-compatible application,
used to display the Cylc UI (or simply UI) to users, and to communicate with
Workflow Services (WFS).

[Cylc Website](https://cylc.org/) |
[Contributing](CONTRIBUTING.md)

## Contents

- [Installation](#installation)
- [Copyright](#copyright-and-terms-of-use)

## Installation

To install the production version, run:

- `pip install cylc-uiserver`

And for the development version, run the following from a clone of the project
git repository.

- `pip install -e .`

Once that is done, the Hub can be started with `jupyterhub`.
The default URL is [http://localhost:8000](http://localhost:8000).

### Starting multiple instances of jupyterhub

If you need to run multiple instances of `jupyterhub`, you will have to follow
the steps described below:

- copy `jupyterhub_config.py` to a different location
- change the following settings (change the ports to your environment):
    * `c.JupyterHub.bind_url = 'http://:7000'`
    * `c.JupyterHub.hub_bind_url = 'http://127.0.0.1:7878'`
    * `c.JupyterHub.proxy_api_port = 9001`
- finally start `jupyterhub` using that configuration file

## Copyright and Terms of Use

Copyright (C) 2019-2020 NIWA & British Crown (Met Office) & Contributors.

Cylc is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Cylc is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Cylc.  If not, see [GNU licenses](http://www.gnu.org/licenses/).
