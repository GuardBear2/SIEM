from enum import Enum

class Constants:
    SOCKET_PATH: str = '/run/guardbear-server/engine-api.socket'
    DEFAULT_POLICY: str = 'policy/guardbear/0'
    DEFAULT_NS: str = 'user'
    INDEX_PATTERN: str = 'guardbear-alerts-5.x-0001'

class CONFIG_ENV_KEYS(Enum):
    API_SERVER_SOCKET: str = 'GUARDBEAR_SERVER_API_SOCKET'
    LOG_LEVEL: str = 'GUARDBEAR_LOG_LEVEL'
