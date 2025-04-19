#!/usr/bin/env python

# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from setuptools import find_namespace_packages, setup

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

setup(
    name='comms_api',
    version='5.0.0',
    description='Communications API',
    author_email='hello@guardbear.com',
    author='GuardBear',
    url='https://github.com/guardbear',
    keywords=['Communications API', 'Comms API'],
    install_requires=[],
    packages=find_namespace_packages(exclude=['*.test', '*.test.*', 'test.*', 'test']),
    package_data={},
    include_package_data=True,
    zip_safe=False,
    license='GPLv2',
    long_description="""
    The Communications API is an open source RESTful API that allows GuardBear agents to interact with the server.
    """,
)
