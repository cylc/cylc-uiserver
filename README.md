[![Anaconda-Server Badge](https://anaconda.org/conda-forge/cylc-uiserver/badges/version.svg)](https://anaconda.org/conda-forge/cylc-uiserver)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/cylc-uiserver/badges/downloads.svg)](https://anaconda.org/conda-forge/cylc-uiserver)
[![PyPI](https://img.shields.io/pypi/v/cylc-uiserver.svg?color=yellow)](https://pypi.org/project/cylc-uiserver/)
[![forum](https://img.shields.io/discourse/https/cylc.discourse.group/posts.svg)](https://cylc.discourse.group/)
[![Test](https://github.com/cylc/cylc-uiserver/actions/workflows/test.yml/badge.svg?branch=master&event=push)](https://github.com/cylc/cylc-uiserver/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/cylc/cylc-uiserver/branch/master/graph/badge.svg)](https://codecov.io/gh/cylc/cylc-uiserver)


# Cylc UI Server

This project contains the Cylc UI Server which serves the Cylc UI
and communicates with running Cylc Schedulers. It also bundles the GUI.

[Cylc Website](https://cylc.org/) |
[Contributing](CONTRIBUTING.md) |
[Developing](#Developing) |
[Forum](https://cylc.discourse.group/)


## Introduction

The functionality in this repository is required to run the Cylc web user
interface.

This repository provides the following components of the Cylc system.

* **The UI**

  This is the Cylc web app that provides control and monitoring functionalities
  for Cylc workflows.

  > **Note**
  > The UI is developed in a separate repository https://github.com/cylc/cylc-ui

* **The UI Server**

  This is a web server which serves the Cylc web UI. It connects to running
  workflows and workflow databases to provide the information the UI displays.
  It is a [Jupyter Server](https://github.com/jupyter-server/jupyter_server).

* **The Hub**

  In multi-user setups this launches UI Servers, provides a proxy for running
  server and handles authentication. It is a
  [JupyterHub](https://github.com/jupyterhub/jupyterhub) server.


## Installation

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/cylc-uiserver/badges/version.svg)](https://anaconda.org/conda-forge/cylc-uiserver)
[![PyPI](https://img.shields.io/pypi/v/cylc-uiserver.svg?color=yellow)](https://pypi.org/project/cylc-uiserver/)
![Conda-Platforms](https://img.shields.io/conda/pn/conda-forge/cylc-uiserver)

For more information on the Cylc components and full-stack Cylc installations
see the
[Cylc documentation](https://cylc.github.io/cylc-doc/latest/html/installation.html).

### For Single-User Setups

Install:

| Conda/Mamba (preferred) | Pip |
| --- | --- |
| `conda install cylc-uiserver-base` | `pip install cylc-uiserver` |

Then start your server:
```bash
cylc gui
```

### For Multi-User Setups

Install:

| Conda/Mamba (preferred) | Pip + Npm |
| --- | --- |
| `conda install cylc-uiserver` | `pip install cylc-uiserver[hub]` |
|   | `npm install configurable-http-proxy` |


Then start your hub:
```bash
cylc hub
```

### List Of Packages

There are a few different packages to suit different needs.

| Tool | Package | Description | Cylc UI Server | Jupyter Hub | Configurable HTTP Proxy |
| --- | --- | --- | --- | --- | --- |
| pip | cylc-uiserver | Single user | :heavy_check_mark: | :x: | :x: |
| conda | cylc-uiserver-base | Single user | :heavy_check_mark:  | :x: | :x: |
| conda | cylc-uiserver-hub-base | Multi user (without proxy) | :heavy_check_mark: | :heavy_check_mark: | :x: |
| pip | cylc-uiserver[hub] | Multi user (without proxy) | :heavy_check_mark: | :heavy_check_mark: | :x: |
| conda | cylc-uiserver | Multi user | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |

The Configurable HTTP Proxy package (Node JS) provides the reverse proxy
that Jupyter Hub requires to collate user's servers behind a single URL. It can
be installed via `conda install configurable-http-proxy` but is not available
via pip (because it requires Node JS)

Other proxies including the
[Traefik Proxy](https://github.com/jupyterhub/traefik-proxy) (Python) can also
fulfil this purpose, see
[list of Jupyter Hub proxies](https://jupyterhub.readthedocs.io/en/stable/howto/proxy.html#index-of-proxies).

### Installing Jupyter Hub Separately

The easiest way to get going with Cylc and Jupyter Hub is to install and deploy
them together and launch Jupyter Hub via the `cylc hub` command.

```bash
conda install cylc-uiserver
cylc hub
```

However, you can also deploy Jupyter Hub separately from the servers it
deploys (e.g. Jupyter Lab or Cylc UI Server) and launch it via the `jupyterhub`
command.

If you are deploying Jupyter Hub separately from Cylc UI Server, these
configurations may be relevant:

* The Jupyter Hub
  [`spawner.cmd`](https://jupyterhub.readthedocs.io/en/stable/reference/config-reference.html)
  determines the command that Jupyter Hub runs in order to start a user's
  server. You may wish to use a wrapper script to activate the required environment.
* The Jupyter Server
  [``ServerApp.jpserver_extensions``](https://jupyter-server.readthedocs.io/en/latest/other/full-config.html)
  configuration determines what Jupyter Server Extensions (e.g. Jupyter Lab or
  Cylc UI Server) are activated when Jupyter Server starts.
  The default behaviour is to activate any installed extensions, however, if
  overridden, you may need to explicitly list cylc-uiserver here.
* The Cylc
  [jupyter_config.py](https://github.com/cylc/cylc-uiserver/blob/master/cylc/uiserver/jupyter_config.py)
  file contains the default Cylc configuration. This applies to hubs started by
  `cylc hub` command but not by the `jupyterhub` command. You may want to
  include some of the configurations from this file in your Jupyter Hub
  configuration.


## Running

The Cylc UIServer is a
[Jupyter Server](https://github.com/jupyter-server/jupyter_server)
extension (like [JupyterLab](https://github.com/jupyterlab/jupyterlab)).

### For Single-User Setups

Run as a standalone server using a URL token for authentication:

```bash
# launch the Cylc GUI and open a browser tab
$ cylc gui

# alternatively the same app can be opened with the jupyter command
$ jupyter cylc
```

> **Note**
> By default, authentication is provided by the URL token. Alternatively, a
> password can be configured (see Jupyter Server docs).
>
> There is no per-user authorisation, so anyone who has the URL token has full
> access to the server.

### For Multi-User Setups

Run a central [JupyterHub](https://github.com/jupyterhub/jupyterhub) server
under a user account with the privileges required to spawn `cylc` processes as
other users.

```bash
# launch the Cylc Hub
# (the default URL is http://localhost:8000)
$ cylc hub
```

Users then authenticate with the hub which launches and manages their UI Server.


## Configuring

### Hub

The Cylc Hub will load the following files in order:

1) System Config

   These are the Cylc defaults which are hardcoded within the repository.

   (`<python-installation>/cylc/uiserver/jupyter_config.py`)

2) Site Config

   This file configures the Hub/UIS for all users. The default path can be
   changed by the ``CYLC_SITE_CONF_PATH`` environment variable.

   (`/etc/cylc/uiserver/jupyter_config.py`)

3) User Config

   This file

   (`~/.cylc/uiserver/jupyter_config.py`)

Alternatively a single config file can be provided on the command line.

```bash
cylc hub --config
```

> **Warning**
> If specifying a config file on the command line, the system config containing
> the hardcoded Cylc default will **not** be loaded.

> **Note**
> The hub can also be run using the ``jupyterhub`` command, however, you
> must source the configuration files manually on the command line.

See the JupyterHub documentation for details on configuration options.

### UI Server

See the [Cylc documentation](
https://cylc.github.io/cylc-doc/latest/html/reference/config/ui-server.html)
for all Cylc-specific configuration options.

The Cylc UI Server is a
[Jupyter Server](https://github.com/jupyter-server/jupyter_server) extension.
Jupyter Server can run multiple extensions. To control the extensions that
are run use the `ServerApp.jpserver_extensions` configuration, see the
[Jupyter Server configuration documentation](https://jupyter-server.readthedocs.io/en/latest/other/full-config.html#other-full-config).

By default the Cylc part of the UI Server log is written to
`~/.cylc/uiserver/uiserver.log`.

<!--
TODO: Link to Jupyter Server logging_config docs when published
-->

### UI

The UI can be configured via the "Settings" option in the Dashboard.

Currently these configurations are stored in the web browser so won't travel
around a network and might not persist.


## Developing

[![Contributors](https://img.shields.io/github/contributors/cylc/cylc-uiserver.svg?color=9cf)](https://github.com/cylc/cylc-uiserver/graphs/contributors)
[![Commit activity](https://img.shields.io/github/commit-activity/m/cylc/cylc-uiserver.svg?color=yellowgreen)](https://github.com/cylc/cylc-uiserver/commits/master)
[![Last commit](https://img.shields.io/github/last-commit/cylc/cylc-uiserver.svg?color=ff69b4)](https://github.com/cylc/cylc-uiserver/commits/master)

Contributions welcome:

* Read the [contributing](CONTRIBUTING.md) page.
* Development setup instructions are in the
  [developer docs](https://cylc.github.io/cylc-admin/#cylc-8-developer-docs).
* Involved change proposals can be found in the
  [admin pages](https://cylc.github.io/cylc-admin/#change-proposals).
* Touch base in the
  [developers chat](https://matrix.to/#/#cylc-general:matrix.org).

1) Install from source into your Python environment:

   ```bash
   pip install -e .[all]
   ```

   > **Note**
   > If you want to run with a development copy of Cylc Flow you must install
   > it first else `pip` will download the latest version from PyPi.

2) For UI development follow the developer instructions for the
   [cylc-ui](https://github.com/cylc/cylc-ui) project, then
   set the following configuration so Cylc uses your UI build
   (rather than the default bundled UI build):

   ```python
   # ~/.cylc/uiserver/jupyter_config.py
   import os
   c.CylcUIServer.ui_build_dir = os.path.expanduser('~/cylc-ui/dist')
   ```

Note about testing: unlike cylc-flow, cylc-uiserver uses the
[pytest-tornasync](https://github.com/eukaryote/pytest-tornasync/) plugin
instead of [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio).
This means you should not decorate async test functions with
`@pytest.mark.asyncio`.

## Copyright and Terms of Use

Copyright (C) 2019-<span actions:bind='current-year'>2025</span> NIWA & British Crown (Met Office) & Contributors.

Cylc is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Cylc is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Cylc. If not, see [GNU licenses](http://www.gnu.org/licenses/).
