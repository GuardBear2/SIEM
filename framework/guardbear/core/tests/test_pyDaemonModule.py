# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest.mock import MagicMock, patch

import pytest
from guardbear.core.exception import GuardBearException
from guardbear.core.pyDaemonModule import *


@patch('guardbear.core.pyDaemonModule.common.GUARDBEAR_RUN', new=Path('/tmp'))
def test_create_pid():
    """Tests create_pid function works."""
    with TemporaryDirectory() as tmpdirname:
        tmpfile = NamedTemporaryFile(dir=tmpdirname, delete=False, suffix='-255.pid')
        create_pid(tmpfile.name.split('/')[3].split('-')[0], '255')


@patch('guardbear.core.pyDaemonModule.common.GUARDBEAR_RUN', new=Path('/tmp'))
@patch('guardbear.core.pyDaemonModule.os.chmod', side_effect=OSError)
def test_create_pid_ko(mock_chmod):
    """Tests create_pid function exception works."""
    with TemporaryDirectory() as tmpdirname:
        tmpfile = NamedTemporaryFile(dir=tmpdirname, delete=False, suffix='-255.pid')
        with pytest.raises(GuardBearException, match='.* 3002 .*'):
            create_pid(tmpfile.name.split('/')[3].split('-')[0], '255')


@pytest.mark.parametrize(
    'process_name, expected_pid',
    [('foo', 123), ('bar', 456), ('guardbear-server-management-apid', 789), ('guardbear-clusterd', None)],
)
@patch('os.listdir', return_value=['foo-123.pid', 'bar-456.pid', 'guardbear-server-management-apid-789.pid'])
def test_get_parent_pid(os_listdir_mock, expected_pid, process_name):
    """Validates that the get_parent_pid function works as expected."""
    actual_pid = get_parent_pid(process_name)
    assert expected_pid == actual_pid


def test_delete_pid():
    """Tests delete_pid function works."""
    with TemporaryDirectory() as tmpdirname:
        tmpfile = NamedTemporaryFile(dir=tmpdirname, delete=False, suffix='-255.pid')
        with patch('guardbear.core.pyDaemonModule.common.GUARDBEAR_RUN', new=Path(tmpdirname.split('/')[2])):
            delete_pid(tmpfile.name.split('/')[3].split('-')[0], '255')


@patch('guardbear.core.pyDaemonModule.next')
@patch('guardbear.core.pyDaemonModule.Path')
def test_get_guardbear_server_pid(path_mock, next_mock):
    """Validate that `get_guardbear_server_pid` works as expected."""
    pid = 123
    daemon_name = 'guardbear-server'
    guardbear_server_pid = f'{daemon_name}-{pid}'
    next_mock.return_value = MagicMock(stem=guardbear_server_pid)

    assert get_guardbear_server_pid(daemon_name) == pid


@patch('guardbear.core.pyDaemonModule.next', side_effect=StopIteration)
@patch('guardbear.core.pyDaemonModule.Path')
def test_get_guardbear_server_pid_ko(path_mock, next_mock):
    """Validate that `get_guardbear_server_pid` works as expected when the server is not running."""
    daemon_name = 'guardbear-server'
    with pytest.raises(StopIteration):
        get_guardbear_server_pid(daemon_name)


@patch('guardbear.core.pyDaemonModule.Path')
def test_get_running_processes(path_mock):
    """Validate that `get_running_processes` works as expected."""
    daemons = ['guardbear-server', 'guardbear-server-management-apid', 'guardbear-comms-apid', 'guardbear-engine']
    path_mock.return_value.glob.return_value = (MagicMock(stem=f'{daemon}-{i}') for i, daemon in enumerate(daemons))

    assert get_running_processes() == daemons


@pytest.mark.parametrize(
    'running_processes,expected',
    (
        (['guardbear-server-management-apid', 'guardbear-comms-apid', 'guardbear-engine'], True),
        (['guardbear-server-management-apid', 'guardbear-comms-apid'], True),
        ([], False),
    ),
)
@patch('guardbear.core.pyDaemonModule.get_running_processes')
def test_check_for_daemons_shutdown(get_running_processes_mock, running_processes, expected):
    """Validate that `check_for_daemons_shutdown` works as expected."""
    daemons = ['guardbear-server-management-apid', 'guardbear-comms-apid', 'guardbear-engine']
    get_running_processes_mock.return_value = running_processes

    assert check_for_daemons_shutdown(daemons) == expected
