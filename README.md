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