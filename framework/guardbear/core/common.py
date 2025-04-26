# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import json
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from contextvars import ContextVar
from copy import deepcopy
from functools import lru_cache, wraps
from grp import getgrnam
from multiprocessing import Event
from pathlib import Path
from pwd import getpwnam
from typing import Any, Dict


# ===================================================== Functions ======================================================
@lru_cache(maxsize=None)
def find_guardbear_path() -> str:
    """Get the GuardBear installation path.

    Returns
    -------
    str
        Path where GuardBear is installed or empty string if there is no framework in the environment.
    """
    abs_path = os.path.abspath(os.path.dirname(__file__))
    allparts = []
    while 1:
        parts = os.path.split(abs_path)
        if parts[0] == abs_path:  # sentinel for absolute paths.
            allparts.insert(0, parts[0])
            break
        elif parts[1] == abs_path:  # sentinel for relative paths.
            allparts.insert(0, parts[1])
            break
        else:
            abs_path = parts[0]
            allparts.insert(0, parts[1])

    guardbear_path = ''
    try:
        for i in range(0, allparts.index('framework')):
            guardbear_path = os.path.join(guardbear_path, allparts[i])
    except ValueError:
        pass

    return guardbear_path


def guardbear_uid() -> int:
    """Retrieve the numerical user ID for the guardbear user.

    Returns
    -------
    int
        Numerical user ID.
    """
    return getpwnam(USER_NAME).pw_uid if globals()['_GUARDBEAR_UID'] is None else globals()['_GUARDBEAR_UID']


def guardbear_gid() -> int:
    """Retrieve the numerical group ID for the guardbear group.

    Returns
    -------
    int
        Numerical group ID.
    """
    return getgrnam(GROUP_NAME).gr_gid if globals()['_GUARDBEAR_GID'] is None else globals()['_GUARDBEAR_GID']


def async_context_cached(key: str = '') -> Any:
    """Save the result of the asynchronous decorated function in a cache.

    Next calls to the asynchronous decorated function returns the saved result saving time and resources. The cache gets
    invalidated at the end of the request.

    Parameters
    ----------
    key : str
        Part of the cache entry identifier. The identifier will be the key + args + kwargs.

    Returns
    -------
    Any
        The result of the first call to the asynchronous decorated function.

    Notes
    -----
    The returned object will be a deep copy of the cached one.
    """

    def decorator(func) -> Any:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            cached_key = json.dumps({'key': key, 'args': args, 'kwargs': kwargs})
            if cached_key not in _context_cache:
                _context_cache[cached_key] = ContextVar(cached_key, default=None)
            if _context_cache[cached_key].get() is None:
                result = await func(*args, **kwargs)
                _context_cache[cached_key].set(result)
            return deepcopy(_context_cache[cached_key].get())

        return wrapper

    return decorator


def context_cached(key: str = '') -> Any:
    """Save the result of the decorated function in a cache.

    Next calls to the decorated function returns the saved result saving time and resources. The cache gets
    invalidated at the end of the request.

    Parameters
    ----------
    key : str
        Part of the cache entry identifier. The identifier will be the key + args + kwargs.

    Returns
    -------
    Any
        The result of the first call to the decorated function.

    Notes
    -----
    The returned object will be a deep copy of the cached one.
    """

    def decorator(func) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            cached_key = json.dumps({'key': key, 'args': args, 'kwargs': kwargs})
            if cached_key not in _context_cache:
                _context_cache[cached_key] = ContextVar(cached_key, default=None)
            if _context_cache[cached_key].get() is None:
                result = func(*args, **kwargs)
                _context_cache[cached_key].set(result)
            return deepcopy(_context_cache[cached_key].get())

        return wrapper

    return decorator


def reset_context_cache() -> None:
    """Reset context cache."""
    for context_var in _context_cache.values():
        context_var.set(None)


def get_context_cache() -> dict:
    """Get the context cache.

    Returns
    -------
    dict
        Dictionary with the context variables representing the cache.
    """
    return _context_cache


# ================================================= Context variables ==================================================
rbac: ContextVar[Dict] = ContextVar('rbac', default={'rbac_mode': 'black'})
current_user: ContextVar[str] = ContextVar('current_user', default='')
broadcast: ContextVar[bool] = ContextVar('broadcast', default=False)
cluster_nodes: ContextVar[list] = ContextVar('cluster_nodes', default=list())
origin_module: ContextVar[str] = ContextVar('origin_module', default='framework')
try:
    mp_pools: ContextVar[Dict] = ContextVar(
        'mp_pools',
        default={
            'process_pool': ProcessPoolExecutor(max_workers=1),
            'authentication_pool': ProcessPoolExecutor(max_workers=1),
            'events_pool': ProcessPoolExecutor(max_workers=1),
        },
    )
# Handle exception when the user running GuardBear cannot access /dev/shm.
except (FileNotFoundError, PermissionError):
    mp_pools: ContextVar[Dict] = ContextVar('mp_pools', default={'thread_pool': ThreadPoolExecutor(max_workers=1)})
_context_cache = dict()


# =========================================== GuardBear constants and variables ============================================
# Clear cache event.
cache_event = Event()
_GUARDBEAR_UID = None
_GUARDBEAR_GID = None
GROUP_NAME = 'guardbear-server'
USER_NAME = 'guardbear-server'

# TODO: Keep until we remove the different deprecated functionalities that are importing it.
GUARDBEAR_PATH = ''

USR_ROOT = Path('/usr')
ETC_ROOT = Path('/etc')
RUN_ROOT = Path('/run')
VAR_ROOT = Path('/var')
BIN_ROOT = Path('/bin')

USR_SHARE = USR_ROOT / Path('share')
VAR_LOG = VAR_ROOT / Path('log')
VAR_LIB = VAR_ROOT / Path('lib')

GUARDBEAR_SERVER = 'guardbear-server'
GUARDBEAR_SHARE = USR_SHARE / GUARDBEAR_SERVER
GUARDBEAR_ETC = ETC_ROOT / GUARDBEAR_SERVER
GUARDBEAR_RUN = RUN_ROOT / GUARDBEAR_SERVER
GUARDBEAR_LOG = VAR_LOG / GUARDBEAR_SERVER
GUARDBEAR_LIB = VAR_LIB / GUARDBEAR_SERVER

GUARDBEAR_QUEUE = GUARDBEAR_RUN / 'cluster'

GUARDBEAR_GROUPS = GUARDBEAR_ETC / 'groups'

LOCAL_SERVER_SOCKET = 'local-server.sock'
LOCAL_SERVER_SOCKET_PATH = GUARDBEAR_RUN / LOCAL_SERVER_SOCKET

CONFIG_SERVER_SOCKET = 'config-server.sock'
CONFIG_SERVER_SOCKET_PATH = GUARDBEAR_RUN / CONFIG_SERVER_SOCKET

COMMS_API_SOCKET = 'comms-api.sock'
COMMS_API_SOCKET_PATH = GUARDBEAR_RUN / COMMS_API_SOCKET


# ============================================= GuardBear constants - Commands =============================================
CHECK_CONFIG_COMMAND = 'check-manager-configuration'
RESTART_GUARDBEAR_COMMAND = 'restart-guardbear'


# =========================================== GuardBear constants - Date format ============================================
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DECIMALS_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


# ========================================= GuardBear constants - Size and limits ==========================================
MAX_SOCKET_BUFFER_SIZE = 64 * 1024  # 64KB.
MAX_QUERY_FILTERS_RESERVED_SIZE = MAX_SOCKET_BUFFER_SIZE - 4 * 1024  # MAX_BUFFER_SIZE - 4KB.
AGENT_NAME_LEN_LIMIT = 128
DATABASE_LIMIT = 500
MAXIMUM_DATABASE_LIMIT = 100000


# ================================================ GuardBear path - Config =================================================
GUARDBEAR_SERVER_YML = GUARDBEAR_ETC / 'guardbear-server.yml'
GUARDBEAR_INDEXER_CA_BUNDLE = GUARDBEAR_ETC / 'certs' / 'root-ca-merged.pem'

# ================================================= GuardBear path - Misc ==================================================
DEFAULT_RBAC_RESOURCES = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'rbac', 'default')

# TODO: Constants asociate to functionality next to deprecate.
GUARDBEAR_LOG_JSON = os.path.join('', 'ossec.json')
WDB_PATH = os.path.join(GUARDBEAR_PATH, 'queue', 'db')


# ================================================ GuardBear path - Sockets ================================================
ENGINE_SOCKET = GUARDBEAR_RUN / 'engine.socket'
# TODO: Constants asociated to functionality next to deprecate.
AR_SOCKET = os.path.join(GUARDBEAR_PATH, 'queue', 'alerts', 'ar')
EXECQ_SOCKET = os.path.join(GUARDBEAR_PATH, 'queue', 'alerts', 'execq')
AUTHD_SOCKET = os.path.join(GUARDBEAR_PATH, 'queue', 'sockets', 'auth')
WCOM_SOCKET = os.path.join(GUARDBEAR_PATH, 'queue', 'sockets', 'com')
REMOTED_SOCKET = os.path.join(GUARDBEAR_PATH, 'queue', 'sockets', 'remote')
WDB_SOCKET = os.path.join(GUARDBEAR_PATH, 'queue', 'db', 'wdb')
