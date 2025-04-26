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
    name='server_management_api',
    version='5.0.0',
    description='GuardBear API',
    author_email='hello@guardbear.com',
    author='GuardBear',
    url='https://github.com/guardbear',
    keywords=['GuardBear API'],
    install_requires=[],
    packages=find_namespace_packages(exclude=['*.test', '*.test.*', 'test.*', 'test']),
    package_data={'': ['spec/spec.yaml']},
    include_package_data=True,
    zip_safe=False,
    license='GPLv2',
    long_description="""\
    The GuardBear API is an open source RESTful API that allows for interaction with the GuardBear manager from a web browser, command line tool like cURL or any script or program that can make web requests. The GuardBear app relies on this heavily and GuardBear’s goal is to accommodate complete remote management of the GuardBear infrastructure via the GuardBear app. Use the API to easily perform everyday actions like adding an agent, restarting the manager(s) or agent(s) or looking up syscheck details.
    """,
)
