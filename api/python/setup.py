#!/usr/bin/env python

import importlib.util
from setuptools import setup, find_packages

spec = importlib.util.spec_from_file_location("rosa.version", "rosa/version.py")
version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version)

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
        "matplotlib",
        "protobuf==3.20",
        "ultralytics"
    ],
)
