import os

from setuptools import find_namespace_packages, setup

from src.kivy_garden.zbarcam import version


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


# exposing the params so it can be imported
setup_params = {
    'name': 'kivy_garden.zbarcam',
    'version': version.__version__,
    'description': 'Real time Barcode and QR Code scanner Edit',
    'long_description': read('README.md'),
    'long_description_content_type': 'text/markdown',
    'author': 'Andre Miras',
    'url': 'https://github.com/kivy-garden/zbarcam',
    'packages': find_namespace_packages(where='src'),
    'package_data': {'kivy_garden.zbarcam': ['*.kv']},
    'package_dir': {'': 'src'},
    'install_requires': [
        'kivy',
        'numpy',
        'opencv-python>=4',
        'pillow',
        'pyzbar',
        'xcamera>=2019.928',
    ],
}


def run_setup():
    setup(**setup_params)


# makes sure the setup doesn't run at import time
if __name__ == '__main__':
    run_setup()
