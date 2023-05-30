#!/usr/bin/env python

import imp
from setuptools import setup, find_packages

version = imp.load_source('rosa.version', 'rosa/version.py')


setup(name='rosa',
      version=version.version,

      description='Rosa robot Python API',
      author='Pollen Robotics',
      url='https://github.com/pollen-robotics/rosa',

      packages=find_packages(),
      install_requires=[
          'websocket-client',
          'opencv-python>3, <4',
          'Pillow',
          'numpy',
          'keras',
          'tensorflow<2',  # can be replaced by tensorflow-gpu
          'matplotlib',
      ])
