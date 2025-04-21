from guardbear.core.config.client import Config
from guardbear.core.config.models.indexer import IndexerConfig, IndexerNode
from guardbear.core.config.models.server import NodeConfig, NodeType, ServerConfig, SSLConfig


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
