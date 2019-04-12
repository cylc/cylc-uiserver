from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cylc-uiserver',
    version='1.0',
    description='Cylc UI Server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cylc/cylc-uiserver/',
    py_modules=['handlers', 'cylc_singleuser'],
    python_requires='>=3.7',
    install_requires=[
        'jupyterhub',
        'tornado',
        'graphene-tornado'
    ],
    entry_points={
        'console_scripts': [
            'cylc-singleuser=cylc_singleuser:main'
        ]
    }
)
