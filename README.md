[![Anaconda-Server Badge](https://anaconda.org/conda-forge/cylc-uiserver/badges/version.svg)](https://anaconda.org/conda-forge/cylc-uiserver)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/cylc-uiserver/badges/downloads.svg)](https://anaconda.org/conda-forge/cylc-uiserver)
[![Test](https://github.com/cylc/cylc-uiserver/actions/workflows/test.yml/badge.svg?branch=master&event=push)](https://github.com/cylc/cylc-uiserver/actions/workflows/test.yml)
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

For production:

```console
$ pip install cylc-uiserver
```

For development run the following from a clone of the project git repository:

```console
$ pip install -e .[all]
```

## Running

```console
$ cylc hub
```

The default URL is [http://localhost:8000](http://localhost:8000).

# Configuring

The default "base" configuration is defined in
`cylc.uiserver.config_defaults.py`, these values can be overridden by the
user config in `~/.cylc/hub/config.py`.

See the Jupyterhub documentation for details on configuration options.

## Copyright and Terms of Use

Copyright (C) 2019-<span actions:bind='current-year'>2021</span> NIWA & British Crown (Met Office) & Contributors.

Cylc is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Cylc is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Cylc.  If not, see [GNU licenses](http://www.gnu.org/licenses/).
