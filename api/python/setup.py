#!/usr/bin/env python

import imp
from setuptools import setup, find_packages

version = imp.load_source("rosa.version", "rosa/version.py")


setup(
    name="rosa",
    version=version.version,
    
    description="Rosa robot Python API",
    author="Poppy Station",
    url="https://github.com/poppy-project/ucia/",
    
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "websocket-client",
        "Pillow",
        "numpy",
        "keras==2.3",
        "tensorflow<2",  # can be replaced by tensorflow-gpu
        "matplotlib",
        "protobuf==3.20",
    ],
)
