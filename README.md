# Running Cylc with JupyterHub

_This is a Work-In-Progress_

## Installing requirements

```shell
$ virtualenv venv
Using base prefix '/home/kinow/Development/python/anaconda3'
New python executable in /home/kinow/Development/python/workspace/cylc-jupyterhub/venv/bin/python
Installing setuptools, pip, wheel...
done.
$ . venv/bin/activate
(venv) $ pip install -e .
...
...
Installing collected packages: tornado, prometheus-client, chardet, idna, certifi, urllib3, requests, pamela, async-generator, python-oauth2, six, python-dateutil, SQLAlchemy, MarkupSafe, Mako, python-editor, alembic, jinja2, ipython-genutils, decorator, traitlets, jupyterhub, cylc-jupyterhub
  Running setup.py develop for cylc-jupyterhub
Successfully installed Mako-1.0.7 MarkupSafe-1.1.1 SQLAlchemy-1.2.18 alembic-1.0.7 async-generator-1.10 certifi-2018.11.29 chardet-3.0.4 cylc-jupyterhub decorator-4.3.2 idna-2.8 ipython-genutils-0.2.0 jinja2-2.10 jupyterhub-0.9.4 pamela-1.0.0 prometheus-client-0.6.0 python-dateutil-2.8.0 python-editor-1.0.4 python-oauth2-1.1.0 requests-2.21.0 six-1.12.0 tornado-5.1.1 traitlets-4.3.2 urllib3-1.24.1
(venv) $ npm install -g configurable-http-proxy
/home/kinow/.nvm/versions/node/v11.6.0/bin/configurable-http-proxy -> /home/kinow/.nvm/versions/node/v11.6.0/lib/node_modules/configurable-http-proxy/bin/configurable-http-proxy
+ configurable-http-proxy@4.0.1
added 45 packages from 62 contributors in 5.53s
(venv) $ jupyterhub --version
0.9.4
(venv) $ configurable-http-proxy --version
4.0.1
(venv) $ cylc-singleuser
usage: cylc-singleuser [-h] [-p PORT] -s STATIC
cylc-singleuser: error: the following arguments are required: -s/--static
```

We can start the hub with: `(venv) $ jupyterhub`, and navigate to [http://localhost:8000](http://localhost:8000).

This start a JupyterHub instance, with the authenticator **jupyterhub.auth.PAMAuthenticator**,
and the spawner **jupyterhub.spawner.LocalProcessSpawner**. Look at the file `jupyterhub_config.py`
in this repository to confirm the spawner used, and the parameters passed. These parameters define
the directory of static content, and also what is the command that the spawner in JupyterHub must
use (`cylc-singleuser`).

## Configuration

```bash
(venv) $ jupyterhub --generate-config
Writing default config to: jupyterhub_config.py
(venv) $ jupyterhub -f $(pwd -P)/jupyterhub_config.py
```

By default we have `jupyterhub.spawner.LocalProcessSpawner` as the spawner. It invokes
a bash shell that executes `jupyterhub-singleuser` with some parameters given via command
line and environment variables.

In order to have JupyterHub spawning our Cylc UI server, which is initialized by `cylc-singleuser`,
we have to add the following settings in `jupyterhub_config.py`:

```
# not necessary as the default, but good nonetheless
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'
c.Spawner.args = ['-s', '../cylc-web/dist/']
c.Spawner.cmd = ['cylc-singleuser']
```

The `LocalProcessSpawner` will add `--port` with a random generated port number by default. The
`c.Spawner.args` includes an extra `-s ../cylc-web/dist`, which is the location where we should
find the application `index.html` (change for your environment if necessary).

Also note that the `c.Spawner.cmd` is `cylc-singleuser`, which is put in the `$PATH` as part of
the instructions of the `setup.py` in this repository.

### Authentication

We are after the scenario where a user A can start the UI server, and another user B is able
to access it too.

With the default authenticator, `jupyterhub.auth.PAMAuthenticator`, if A starts the server,
B is not even able to authenticate to the running hub. That is because in Linux PAM has
restrictions in place, and you must be a super user, or wheel member, in order to use it.

But if you start the hub as the root user, in a location that other users can access the files
(i.e. do not start under `/root`, use something like `/opt` and watch out for _selinux_),
then you should be able to get all users in the local system authenticating fine.

### Authorization

Once authenticated, the authorization is handled in the UI server. In the vanilla installation,
Jupyter Notebook would find the Cookie of the logged in user, and then query the Hub about it.
As we do not have the notebook, the example from Cylc Spawner 01 should work.

It should work means that all users see each others UI servers.

TODO: explain whether we can use the Hub REST API and DB scheme for Cylc workflow services
authentication.

## Services

Q: Would Cylc Review be a service? Perhaps we could choose whether to start it with
the UI server or not!
