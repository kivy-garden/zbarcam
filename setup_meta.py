"""
Creates a distribution alias that just installs kivy_garden.zbarcam.
"""
from setuptools import setup

from setup import setup_params

setup_params.update({
    'install_requires': ['kivy_garden.zbarcam'],
    'name': 'zbarcam',
})


setup(**setup_params)
