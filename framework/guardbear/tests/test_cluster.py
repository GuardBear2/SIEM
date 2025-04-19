# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import sys
from unittest.mock import MagicMock, patch

import pytest
from guardbear.core.config.client import CentralizedConfig
from guardbear.core.config.models.server import ValidateFilePathMixin
from guardbear.tests.util import get_default_configuration

with patch('guardbear.core.common.guardbear_uid'):
    with patch('guardbear.core.common.guardbear_gid'):
        with patch.object(ValidateFilePathMixin, '_validate_file_path', return_value=None):
            default_config = get_default_configuration()
            CentralizedConfig._config = default_config

            sys.modules['guardbear.rbac.orm'] = MagicMock()
            import guardbear.rbac.decorators

            del sys.modules['guardbear.rbac.orm']

            from guardbear.tests.util import RBAC_bypasser

            guardbear.rbac.decorators.expose_resources = RBAC_bypasser
            from guardbear import cluster
            from guardbear.core import common
            from guardbear.core.cluster.local_client import LocalClient
            from guardbear.core.exception import GuardBearError, GuardBearResourceNotFound
            from guardbear.core.results import GuardBearResult


async def test_node_wrapper():
    """Verify that the node_wrapper returns the default node information."""
    result = await cluster.get_node_wrapper()
    assert result.affected_items == [{'node': default_config.server.node.name, 'type': default_config.server.node.type}]


@patch('guardbear.cluster.get_node', side_effect=GuardBearError(1001))
async def test_node_wrapper_exception(mock_get_node):
    """Verify the exceptions raised in get_node_wrapper."""
    result = await cluster.get_node_wrapper()
    assert list(result.failed_items.keys())[0] == GuardBearError(1001)


async def test_get_status_json():
    """Verify that get_status_json returns the default status information."""
    result = await cluster.get_status_json()
    expected = GuardBearResult({'data': {'running': 'no'}})
    assert result == expected


@pytest.mark.asyncio
@patch('guardbear.core.cluster.local_client.LocalClient.start', side_effect=None)
async def test_get_health_nodes(mock_unix_connection):
    """Verify that get_health_nodes returns the health of all nodes."""

    async def async_mock(lc=None, filter_node=None):
        return {'nodes': {'manager': {'info': {'name': 'master'}}}}

    local_client = LocalClient()
    with patch('guardbear.cluster.get_health', side_effect=async_mock):
        result = await cluster.get_health_nodes(lc=local_client)
    expected = await async_mock()

    assert result.affected_items == [expected['nodes']['manager']]


@pytest.mark.asyncio
async def test_get_nodes_info():
    """Verify that get_nodes_info returns the information of all nodes."""

    async def valid_node(lc=None, filter_node=None):
        return {'items': ['master', 'worker1'], 'totalItems': 2}

    local_client = LocalClient()
    common.cluster_nodes.set(['master', 'worker1', 'worker2'])
    with patch('guardbear.cluster.get_nodes', side_effect=valid_node):
        result = await cluster.get_nodes_info(lc=local_client, filter_node=['master', 'worker1', 'noexists'])
    expected = await valid_node()

    assert result.affected_items == expected['items']
    assert result.total_affected_items == expected['totalItems']
    assert result.failed_items[GuardBearResourceNotFound(1730)] == {'noexists'}
    assert result.total_failed_items == 1
