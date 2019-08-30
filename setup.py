#!/usr/bin/env python

from distutils.core import setup

setup(name='zbarcam',
      version='20171220',
      description='Real time Barcode and QR Code scanner Edit',
      author='Andre Miras',
      url='https://github.com/AndreMiras/garden.zbarcam',
      packages=['kivy_garden.zbarcam'],
      package_data={'kivy_garden.zbarcam': ['*.kv']},
      install_requires=['pyzbar', 'kivy', 'pillow', 'numpy'])
