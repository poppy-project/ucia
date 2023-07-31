#!/usr/bin/env python

import imp
from setuptools import setup, find_packages

version = imp.load_source('rosa.version', 'rosa/version.py')


setup(name='rosa',
      version=version.version,

      description='Rosa robot Python API',
      author='Poppy Station',
      url='https://github.com/poppy-project',
      include_package_data=True,
      packages=find_packages(),
      install_requires=[
          'websocket-client',
          'opencv-python>3, <4',
          'Pillow',
          'numpy',
          'keras==2.3.0',
          'tensorflow',  # can be replaced by tensorflow-gpu
          'matplotlib',
      ])
