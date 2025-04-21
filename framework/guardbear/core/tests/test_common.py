# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import json
from contextvars import ContextVar
from grp import getgrnam
from pwd import getpwnam
from unittest.mock import patch

import pytest
from guardbear.core.common import (
    async_context_cached,
    context_cached,
    find_guardbear_path,
    get_context_cache,
    reset_context_cache,
    guardbear_gid,
    guardbear_uid,
)


@pytest.mark.parametrize(
    'fake_path, expected',
    [
        ('/var/ossec/framework/python/lib/python3.7/site-packages/guardbear-3.10.0-py3.7.egg/guardbear', '/var/ossec'),
        (
            '/my/custom/path/framework/python/lib/python3.7/site-packages/guardbear-3.10.0-py3.7.egg/guardbear',
            '/my/custom/path',
        ),
        ('/my/fake/path', ''),
    ],
)
def test_find_guardbear_path(fake_path, expected):
    """Test the `find_guardbear_path` function with various fake paths."""
    with patch('guardbear.core.common.__file__', new=fake_path):
        assert find_guardbear_path.__wrapped__() == expected


def test_find_guardbear_path_relative_path():
    """Test the `find_guardbear_path` function with a relative path."""
    with patch('os.path.abspath', return_value='~/framework'):
        assert find_guardbear_path.__wrapped__() == '~'


def test_guardbear_uid():
    """Test the `guardbear_uid` function by mocking the `getpwnam` call."""
    with patch('guardbear.core.common.getpwnam', return_value=getpwnam('root')):
        guardbear_uid()


def test_guardbear_gid():
    """Test the `guardbear_gid` function by mocking the `getgrnam` call."""
    with patch('guardbear.core.common.getgrnam', return_value=getgrnam('root')):
        guardbear_gid()


async def test_async_context_cached():
    """Verify that async_context_cached decorator correctly saves and returns saved value when called again."""
    test_async_context_cached.calls_to_foo = 0

    @async_context_cached('foobar')
    async def foo(arg='bar', **data):
        test_async_context_cached.calls_to_foo += 1
        return arg

    # The result of function 'foo' is being cached and it has been called once
    assert await foo() == 'bar' and test_async_context_cached.calls_to_foo == 1
    assert await foo() == 'bar' and test_async_context_cached.calls_to_foo == 1
    assert isinstance(get_context_cache()[json.dumps({'key': 'foobar', 'args': [], 'kwargs': {}})], ContextVar)

    # foo called with an argument
    assert await foo('other_arg') == 'other_arg' and test_async_context_cached.calls_to_foo == 2
    assert isinstance(
        get_context_cache()[json.dumps({'key': 'foobar', 'args': ['other_arg'], 'kwargs': {}})], ContextVar
    )

    # foo called with the same argument as default, a new context var is created in the cache
    assert await foo('bar') == 'bar' and test_async_context_cached.calls_to_foo == 3
    assert isinstance(get_context_cache()[json.dumps({'key': 'foobar', 'args': ['bar'], 'kwargs': {}})], ContextVar)

    # Reset cache and calls to foo
    reset_context_cache()
    test_async_context_cached.calls_to_foo = 0

    # foo called with kwargs, a new context var is created with kwargs not empty
    assert await foo(data='bar') == 'bar' and test_async_context_cached.calls_to_foo == 1
    assert isinstance(
        get_context_cache()[json.dumps({'key': 'foobar', 'args': [], 'kwargs': {'data': 'bar'}})], ContextVar
    )


def test_context_cached():
    """Verify that context_cached decorator correctly saves and returns saved value when called again."""
    test_context_cached.calls_to_foo = 0

    @context_cached('foobar')
    def foo(arg='bar', **data):
        test_context_cached.calls_to_foo += 1
        return arg

    # The result of function 'foo' is being cached and it has been called once
    assert foo() == 'bar' and test_context_cached.calls_to_foo == 1, '"bar" should be returned with 1 call to foo.'
    assert foo() == 'bar' and test_context_cached.calls_to_foo == 1, '"bar" should be returned with 1 call to foo.'
    assert isinstance(get_context_cache()[json.dumps({'key': 'foobar', 'args': [], 'kwargs': {}})], ContextVar)

    # foo called with an argument
    assert foo('other_arg') == 'other_arg' and test_context_cached.calls_to_foo == 2, (
        '"other_arg" should be returned with 2 calls to foo. '
    )
    assert isinstance(
        get_context_cache()[json.dumps({'key': 'foobar', 'args': ['other_arg'], 'kwargs': {}})], ContextVar
    )

    # foo called with the same argument as default, a new context var is created in the cache
    assert foo('bar') == 'bar' and test_context_cached.calls_to_foo == 3, (
        '"bar" should be returned with 3 calls to foo. '
    )
    assert isinstance(get_context_cache()[json.dumps({'key': 'foobar', 'args': ['bar'], 'kwargs': {}})], ContextVar)

    # Reset cache and calls to foo
    reset_context_cache()
    test_context_cached.calls_to_foo = 0

    # foo called with kwargs, a new context var is created with kwargs not empty
    assert foo(data='bar') == 'bar' and test_context_cached.calls_to_foo == 1, (
        '"bar" should be returned with 1 calls to foo. '
    )
    assert isinstance(
        get_context_cache()[json.dumps({'key': 'foobar', 'args': [], 'kwargs': {'data': 'bar'}})], ContextVar
    )
