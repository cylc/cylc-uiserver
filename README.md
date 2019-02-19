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
(venv) $ pip install -r requirements.txt
...
...
Successfully built python-oauth2 alembic SQLAlchemy prometheus-client
Installing collected packages: python-oauth2, MarkupSafe, jinja2, decorator, ipython-genutils, six, traitlets, pamela, SQLAlchemy, Mako, python-editor, python-dateutil, alembic, async-generator, tornado, prometheus-client, urllib3, chardet, idna, certifi, requests, jupyterhub, pyzmq, ptyprocess, terminado, Send2Trash, entrypoints, pandocfilters, defusedxml, testpath, jupyter-core, mistune, jsonschema, nbformat, pygments, webencodings, bleach, nbconvert, jupyter-client, backcall, parso, jedi, pexpect, wcwidth, prompt-toolkit, pickleshare, ipython, ipykernel, notebook
Successfully installed Mako-1.0.7 MarkupSafe-1.1.0 SQLAlchemy-1.2.18 Send2Trash-1.5.0 alembic-1.0.7 async-generator-1.10 backcall-0.1.0 bleach-3.1.0 certifi-2018.11.29 chardet-3.0.4 decorator-4.3.2 defusedxml-0.5.0 entrypoints-0.3 idna-2.8 ipykernel-5.1.0 ipython-7.2.0 ipython-genutils-0.2.0 jedi-0.13.2 jinja2-2.10 jsonschema-2.6.0 jupyter-client-5.2.4 jupyter-core-4.4.0 jupyterhub-0.9.4 mistune-0.8.4 nbconvert-5.4.1 nbformat-4.4.0 notebook-5.7.4 pamela-1.0.0 pandocfilters-1.4.2 parso-0.3.4 pexpect-4.6.0 pickleshare-0.7.5 prometheus-client-0.5.0 prompt-toolkit-2.0.8 ptyprocess-0.6.0 pygments-2.3.1 python-dateutil-2.8.0 python-editor-1.0.4 python-oauth2-1.1.0 pyzmq-17.1.2 requests-2.21.0 six-1.12.0 terminado-0.8.1 testpath-0.4.2 tornado-5.1.1 traitlets-4.3.2 urllib3-1.24.1 wcwidth-0.1.7 webencodings-0.5.1
(venv) $ npm install -g configurable-http-proxy
/home/kinow/.nvm/versions/node/v11.6.0/bin/configurable-http-proxy -> /home/kinow/.nvm/versions/node/v11.6.0/lib/node_modules/configurable-http-proxy/bin/configurable-http-proxy
+ configurable-http-proxy@4.0.1
added 45 packages from 62 contributors in 5.53s
(venv) $ jupyterhub --version
0.9.4
(venv) $ configurable-http-proxy --version
4.0.1
```

We can start the hub with: `(venv) $ jupyterhub`, and navigate to [http://localhost:8000](http://localhost:8000).

This start a JupyterHub instance, with the authenticator **jupyterhub.auth.PAMAuthenticator**,
and the spawner **jupyterhub.spawner.LocalProcessSpawner**.

## Configuration

_Goal: list the configuration needed to have a spawner starting a web application that we will
call Cylc Web, but it is actually just a dummy application for testing purposes. Whereas JupyterHub
has a "Single-User Notebook Server", it is good to thing of Cylc Web as a
"Single-User Cylc Server".__

```bash
(venv) $ jupyterhub --generate-config
Writing default config to: jupyterhub_config.py
(venv) $ jupyterhub -f $(pwd -P)/jupyterhub_config.py
```

By default we have `jupyterhub.spawner.LocalProcessSpawner` as the spawner. It invokes
a bash shell that executes `jupyterhub-singleuser` with some parameters given via command
line and environment variables.

Alas this command cannot be changed in that spawner, so we have no other option but
writing our own spawner.

### Cylc Spawner 01

Spawners in JupyterHub can also request extra information when started. This is possibly
useful for Cylc, as we can ask what is the Suite name, or PBS job, etc.

* https://jupyterhub.readthedocs.io/en/stable/reference/spawners.html#spawner-options-form
* https://github.com/jupyterhub/jupyterhub/blob/master/examples/spawn-form/jupyterhub_config.py

```bash
(venv) $ PYTHONPATH=$(pwd -P) jupyterhub -f $(pwd -P)/jupyterhub_config.py
```

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
