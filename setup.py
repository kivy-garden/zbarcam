#!/usr/bin/env python

from distutils.core import setup

setup(name='zbarcam',
      version='20171020',
      description='Real time Barcode and QR Code scanner Edit',
      author='Andre Miras',
      url='https://github.com/AndreMiras/garden.zbarcam',
      py_modules=['zbarcam'],
      install_requires=['zbar', 'kivy', 'pillow', 'numpy'])
