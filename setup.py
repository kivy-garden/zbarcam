import os

from setuptools import setup
from kivy_garden.zbarcam import version


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(name='zbarcam',
      version=version.__version__,
      description='Real time Barcode and QR Code scanner Edit',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      author='Andre Miras',
      url='https://github.com/AndreMiras/garden.zbarcam',
      packages=['kivy_garden.zbarcam'],
      package_data={'kivy_garden.zbarcam': ['*.kv']},
      install_requires=['pyzbar', 'kivy', 'pillow', 'numpy'])
