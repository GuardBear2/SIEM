#!/usr/bin/env python

# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

from setuptools import find_namespace_packages, setup
from guardbear import __version__

setup(
    name='guardbear',
    version=__version__,
    description='GuardBear control with Python',
    url='https://github.com/guardbear',
    author='GuardBear',
    author_email='hello@guardbear.com',
    license='GPLv2',
    packages=find_namespace_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    package_data={'guardbear': ['core/guardbear.json', 'core/cluster/cluster.json', 'rbac/default/*.yaml']},
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
)
