[![Anaconda-Server Badge](https://anaconda.org/conda-forge/cylc-uiserver/badges/version.svg)](https://anaconda.org/conda-forge/cylc-uiserver)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/cylc-uiserver/badges/downloads.svg)](https://anaconda.org/conda-forge/cylc-uiserver)
[![Test](https://github.com/cylc/cylc-uiserver/actions/workflows/test.yml/badge.svg?branch=master&event=push)](https://github.com/cylc/cylc-uiserver/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/cylc/cylc-uiserver/branch/master/graph/badge.svg)](https://codecov.io/gh/cylc/cylc-uiserver)

# Cylc UI Server

This project contains the Cylc UI Server. A JupyterHub-compatible application,
used to serve the Cylc UI, and to communicate with running Cylc Schedulers.

[Cylc Website](https://cylc.org/) |
[Contributing](CONTRIBUTING.md) |
[Developing](DEVELOPING.md)

## Contents

- [Installation](#installation)
- [Introduction](#introduction)
- [Copyright](#copyright-and-terms-of-use)

## Introduction

The functionality in this repository is required to run the Cylc web user
interface.

This repository provides the following components of the Cylc system.

* The UI

  This is the Cylc web app that provides control and monitoring functionalities
  for Cylc workflows.

* The UI Server

  This is a web server which serves the Cylc web UI. It connects to running
  workflows and workflow databases to provide the information the UI displays.

* The Hub

  This launches UI Servers, provides a proxy for running server and handles
  authentication. It is a JupyterHub server.

## Installation

For production:

```console
# via conda (preferred)
$ conda install cylc-uiserver

# via pip
$ pip install cylc-uiserver
```

## Running

```console
$ cylc hub
```

The default URL is [http://localhost:8000](http://localhost:8000).

## Configuring

### Hub

The Cylc Hub will load the following files in order:

1) System Config

   These are the Cylc defaults which are hardcoded within the repository.

   (`<python-installation>/cylc/uiserver/config_defaults.py`)

2) Site Config

   This file configures the Hub/UIS for all users. The default path can be
   changed by the ``CYLC_SITE_CONF_PATH`` environment variable.

   (`/etc/cylc/hub/config.py`)

3) User Config

   This file

   (`~/.cylc/hub/config.py`)

Alternatively a single config file can be provided on the command line.

```console
$ cylc hub --config
```

> **Warning:**
>
> If specifying a config file on the command line the system config containing
> the hardcoded Cylc default will **not** be loaded.

See the Jupyterhub documentation for details on configuration options.

### UI Server

The UI Server is (currently) also configured from the same configuration file(s)
as the hub using the
`UIServer` namespace.

Currently the UI Server accepts these configurations:

* `c.UIServer.ui_build_dir`
* `c.UIServer.ui_version`
* `c.UIServer.logging_config`
* `c.UIServer.scan_iterval`

See the `cylc.uiserver.main.UIServer` file for details.

## Developing

1) Read the [Contributing](CONTRIBUTING.md) page.

2) Fork and clone this repo.

3) Install from source into your Python environment:

   ```console
   $ pip install -e .[all]
   ```

   > **Note:**
   >
   > If you want to run with a development copy of Cylc Flow you must install
   > it first else `pip` will download the latest version from PyPi.

4) For UI development set the following configuration to use your UI build
   (rather than the default bundled UI build):

   ```python
   # ~/.cylc/hub/config.py
   c.UIServer.ui_build_dir = '~/cylc-ui/dist'  # path to build
   ```

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
