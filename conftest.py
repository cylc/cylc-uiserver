pytest_plugins = [
    'jupyter_server.pytest_plugin'
]


def pytest_ignore_collect(path):
    # --doctest-modules seems to ignore the value if configured in pyproject
    if 'jupyter_config.py' in str(path):
        return True
