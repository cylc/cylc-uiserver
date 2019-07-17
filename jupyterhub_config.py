# general settings
c.JupyterHub.logo_file = '../cylc-ui/dist/img/logo.png'

# proxy settings
import secrets
PROXY_AUTH_TOKEN = secrets.token_hex(30)
PROXY_URL='http://localhost:8001'
c.ConfigurableHTTPProxy.should_start = True
c.ConfigurableHTTPProxy.api_url = PROXY_URL
# this defines the proxy auth token
c.ConfigurableHTTPProxy.auth_token=PROXY_AUTH_TOKEN

# spawner settings
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'
c.Spawner.cmd = ['cylc-singleuser']
import os
script_dir = os.path.dirname(__file__)
static_path = os.path.join(script_dir, '../cylc-ui/dist/')
c.Spawner.args = ['-s', static_path]
c.Spawner.environment = {
    # this line exports the proxy auth token to the cylc-uiserver process
    'CONFIGPROXY_AUTH_TOKEN': PROXY_AUTH_TOKEN,
    'CONFIGPROXY_URL': PROXY_URL
}
