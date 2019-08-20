[![Build Status](https://travis-ci.org/cylc/cylc-uiserver.svg?branch=master)](https://travis-ci.org/cylc/cylc-uiserver)
[![codecov](https://codecov.io/gh/cylc/cylc-uiserver/branch/master/graph/badge.svg)](https://codecov.io/gh/cylc/cylc-uiserver)

# Cylc UI Server

This project contains the Cylc UI Server. A JupyterHub-compatible application,
used to display the Cylc UI (or simply UI) to users, and to communicate with
Workflow Services (WFS).

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

