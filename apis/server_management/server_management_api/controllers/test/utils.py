# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from guardbear.core.config.client import Config
from guardbear.core.config.models.indexer import IndexerConfig, IndexerNode
from guardbear.core.config.models.server import NodeConfig, NodeType, ServerConfig, SSLConfig
from guardbear.core.results import AffectedItemsGuardBearResult


def get_default_configuration():
    """Get default configuration for the tests."""
    return Config(
        server=ServerConfig(
            nodes=['0'],
            node=NodeConfig(
                name='node_name',
                type=NodeType.MASTER,
                ssl=SSLConfig(key='example', cert='example', ca='example'),
            ),
        ),
        indexer=IndexerConfig(hosts=[IndexerNode(host='example', port=1516)], username='guardbear', password='guardbear'),
    )


class CustomAffectedItems(AffectedItemsGuardBearResult):
    """Mock custom values that are needed in controller tests."""

    def __init__(self, empty: bool = False):
        if not empty:
            super().__init__(dikt={'dikt_key': 'dikt_value'}, affected_items=[{'id': '001'}])
        else:
            super().__init__()

    def __getitem__(self, key):
        return self.render()[key]
