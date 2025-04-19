# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import os
import sys
from unittest.mock import ANY, MagicMock, mock_open, patch

import pytest
from guardbear.core.common import REMOTED_SOCKET

with patch('guardbear.core.common.guardbear_uid'):
    with patch('guardbear.core.common.guardbear_gid'):
        sys.modules['guardbear.rbac.orm'] = MagicMock()
        import guardbear.rbac.decorators

        del sys.modules['guardbear.rbac.orm']
        from guardbear.tests.util import RBAC_bypasser

        guardbear.rbac.decorators.expose_resources = RBAC_bypasser
        from guardbear.core import configuration
        from guardbear.core.exception import GuardBearError, GuardBearInternalError

parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
tmp_path = 'tests/data'


def test_get_group_conf():
    """Test get_group_conf functionality."""
    with pytest.raises(GuardBearError, match='.* 1710 .*'):
        configuration.get_group_conf(group_id='noexists')

    with patch('guardbear.core.common.GUARDBEAR_GROUPS', new=os.path.join(parent_directory, tmp_path, 'configuration')):
        with patch('guardbear.core.configuration.load_guardbear_yaml', side_effect=GuardBearError(1101)):
            with pytest.raises(GuardBearError, match='.* 1101 .*'):
                result = configuration.get_group_conf(group_id='default')
                assert isinstance(result, dict)

    with patch('guardbear.core.common.GUARDBEAR_GROUPS', new=os.path.join(parent_directory, tmp_path, 'configuration')):
        assert configuration.get_group_conf(group_id='default')['total_affected_items'] == 1


@patch('guardbear.core.configuration.common.guardbear_gid')
@patch('guardbear.core.configuration.common.guardbear_uid')
@patch('builtins.open')
def test_update_group_configuration(mock_open, mock_guardbear_uid, mock_guardbear_gid):
    """Test update_group_configuration functionality."""
    with pytest.raises(GuardBearError, match='.* 1710 .*'):
        configuration.update_group_configuration('noexists', 'noexists')

    with patch('guardbear.core.common.GUARDBEAR_GROUPS', new=os.path.join(parent_directory, tmp_path, 'configuration')):
        with patch('guardbear.core.configuration.open', return_value=Exception):
            with pytest.raises(GuardBearError, match='.* 1006 .*'):
                configuration.update_group_configuration('default', '')

    with patch('guardbear.core.common.GUARDBEAR_GROUPS', new=os.path.join(parent_directory, tmp_path, 'configuration')):
        with patch('guardbear.core.configuration.open'):
            configuration.update_group_configuration('default', 'key: value')


@patch('guardbear.core.configuration.common.guardbear_gid')
@patch('guardbear.core.configuration.common.guardbear_uid')
@patch('builtins.open')
def test_update_group_file(mock_open, mock_guardbear_uid, mock_guardbear_gid):
    """Test update_group_file functionality."""
    with pytest.raises(GuardBearError, match='.* 1710 .*'):
        configuration.update_group_file('noexists', 'given')

    with pytest.raises(GuardBearError, match='.* 1722 .*'):
        configuration.update_group_file('.invalid', '')

    with patch('guardbear.core.common.GUARDBEAR_GROUPS', new=os.path.join(parent_directory, tmp_path, 'configuration')):
        with pytest.raises(GuardBearError, match='.* 1112 .*'):
            configuration.update_group_file('default', [])


@pytest.mark.parametrize(
    'agent_id, component, socket, socket_dir, rec_msg',
    [
        (None, 'auth', 'auth', 'sockets', 'ok {"auth": {"use_password": "yes"}}'),
        (None, 'auth', 'auth', 'sockets', 'ok {"auth": {"use_password": "no"}}'),
        (None, 'auth', 'auth', 'sockets', 'ok {"auth": {}}'),
        (None, 'agent', 'analysis', 'sockets', {'error': 0, 'data': {'enabled': 'yes'}}),
        (None, 'agentless', 'agentless', 'sockets', 'ok {"agentless": {"enabled": "yes"}}'),
        (None, 'analysis', 'analysis', 'sockets', {'error': 0, 'data': {'enabled': 'yes'}}),
        (None, 'com', 'com', 'sockets', 'ok {"com": {"enabled": "yes"}}'),
        (None, 'csyslog', 'csyslog', 'sockets', 'ok {"csyslog": {"enabled": "yes"}}'),
        (None, 'integrator', 'integrator', 'sockets', 'ok {"integrator": {"enabled": "yes"}}'),
        (None, 'logcollector', 'logcollector', 'sockets', 'ok {"logcollector": {"enabled": "yes"}}'),
        (None, 'mail', 'mail', 'sockets', 'ok {"mail": {"enabled": "yes"}}'),
        (None, 'monitor', 'monitor', 'sockets', 'ok {"monitor": {"enabled": "yes"}}'),
        (None, 'request', 'remote', 'sockets', {'error': 0, 'data': {'enabled': 'yes'}}),
        (None, 'syscheck', 'syscheck', 'sockets', 'ok {"syscheck": {"enabled": "yes"}}'),
        (None, 'guardbear-db', 'wdb', 'db', {'error': 0, 'data': {'enabled': 'yes'}}),
        (None, 'wmodules', 'wmodules', 'sockets', 'ok {"wmodules": {"enabled": "yes"}}'),
        ('001', 'auth', 'remote', 'sockets', 'ok {"auth": {"use_password": "yes"}}'),
        ('001', 'auth', 'remote', 'sockets', 'ok {"auth": {"use_password": "no"}}'),
        ('001', 'auth', 'remote', 'sockets', 'ok {"auth": {}}'),
        ('001', 'agent', 'remote', 'sockets', 'ok {"agent": {"enabled": "yes"}}'),
        ('001', 'agentless', 'remote', 'sockets', 'ok {"agentless": {"enabled": "yes"}}'),
        ('001', 'analysis', 'remote', 'sockets', 'ok {"analysis": {"enabled": "yes"}}'),
        ('001', 'com', 'remote', 'sockets', 'ok {"com": {"enabled": "yes"}}'),
        ('001', 'csyslog', 'remote', 'sockets', 'ok {"csyslog": {"enabled": "yes"}}'),
        ('001', 'integrator', 'remote', 'sockets', 'ok {"integrator": {"enabled": "yes"}}'),
        ('001', 'logcollector', 'remote', 'sockets', 'ok {"logcollector": {"enabled": "yes"}}'),
        ('001', 'mail', 'remote', 'sockets', 'ok {"mail": {"enabled": "yes"}}'),
        ('001', 'monitor', 'remote', 'sockets', 'ok {"monitor": {"enabled": "yes"}}'),
        ('001', 'request', 'remote', 'sockets', 'ok {"request": {"enabled": "yes"}}'),
        ('001', 'syscheck', 'remote', 'sockets', 'ok {"syscheck": {"enabled": "yes"}}'),
        ('001', 'wmodules', 'remote', 'sockets', 'ok {"wmodules": {"enabled": "yes"}}'),
    ],
)
@patch('builtins.open', mock_open(read_data='test_password'))
@patch('guardbear.core.guardbear_socket.create_guardbear_socket_message')
@patch('os.path.exists')
@patch('guardbear.core.common.GUARDBEAR_PATH', new='/var/ossec')
@pytest.mark.xfail(reason='This module it is deprecated.', run=False)
def test_get_active_configuration(
    mock_exists, mock_create_guardbear_socket_message, agent_id, component, socket, socket_dir, rec_msg
):
    """This test checks the proper working of get_active_configuration function."""
    sockets_json_protocol = {'remote', 'analysis', 'wdb'}
    config = MagicMock()

    socket_class = 'GuardBearSocket' if socket not in sockets_json_protocol or agent_id else 'GuardBearSocketJSON'
    with patch(f'guardbear.core.guardbear_socket.{socket_class}.close') as mock_close:
        with patch(f'guardbear.core.guardbear_socket.{socket_class}.send') as mock_send:
            with patch(f'guardbear.core.guardbear_socket.{socket_class}.__init__', return_value=None) as mock__init__:
                with patch(
                    f'guardbear.core.guardbear_socket.{socket_class}.receive',
                    return_value=rec_msg.encode() if socket_class == 'GuardBearSocket' else rec_msg,
                ) as mock_receive:
                    result = configuration.get_active_configuration(component, config, agent_id)

                    mock__init__.assert_called_with(
                        f'/var/ossec/queue/{socket_dir}/{socket}' if not agent_id else REMOTED_SOCKET
                    )

                    if socket_class == 'GuardBearSocket':
                        mock_send.assert_called_with(
                            f'getconfig {config}'.encode()
                            if not agent_id
                            else f'{agent_id} {component} getconfig {config}'.encode()
                        )
                    else:  # socket_class == "GuardBearSocketJSON"
                        mock_create_guardbear_socket_message.assert_called_with(
                            origin={'module': ANY}, command='getconfig', parameters={'section': config}
                        )
                        mock_send.assert_called_with(mock_create_guardbear_socket_message.return_value)

                    mock_receive.assert_called_once()
                    mock_close.assert_called_once()

                    if result.get('auth', {}).get('use_password') == 'yes':
                        assert result.get('authd.pass') == 'test_password'
                    else:
                        assert 'authd.pass' not in result


@pytest.mark.parametrize(
    'agent_id, component, config, socket_exist, socket_class, expected_error, expected_id',
    [
        # Checks for the manager or any other agent
        (None, 'test_component', None, ANY, 'GuardBearSocket', GuardBearError, 1307),  # No configuration
        (None, None, 'test_config', ANY, 'GuardBearSocket', GuardBearError, 1307),  # No component
        (None, 'test_component', 'test_config', ANY, 'GuardBearSocket', GuardBearError, 1101),  # Component not in components
        ('001', 'syscheck', 'syscheck', ANY, 'GuardBearSocket', GuardBearError, 1116),  # Cannot send request
        ('001', 'syscheck', 'syscheck', ANY, 'GuardBearSocket', GuardBearError, 1117),  # No such file or directory
        # Checks for manager - Simple messages
        (None, 'syscheck', 'syscheck', False, 'GuardBearSocket', GuardBearError, 1121),  # Socket does not exist
        (None, 'syscheck', 'syscheck', True, 'GuardBearSocket', GuardBearInternalError, 1121),  # Error connecting with socket
        (None, 'syscheck', 'syscheck', True, 'GuardBearSocket', GuardBearInternalError, 1118),  # Data could not be received
        # Checks for manager - JSON messages
        (None, 'request', 'global', False, 'GuardBearSocketJSON', GuardBearError, 1121),  # Socket does not exist
        (None, 'request', 'global', True, 'GuardBearSocketJSON', GuardBearInternalError, 1121),  # Error connecting with socket
        (None, 'request', 'global', True, 'GuardBearSocketJSON', GuardBearInternalError, 1118),  # Data could not be received
        # Checks for 001
        ('001', 'syscheck', 'syscheck', ANY, 'GuardBearSocket', GuardBearInternalError, 1121),  # Error connecting with socket
        ('001', 'syscheck', 'syscheck', ANY, 'GuardBearSocket', GuardBearInternalError, 1118),  # Data could not be received
    ],
)
@patch('os.path.exists')
def test_get_active_configuration_ko(
    mock_exists, agent_id, component, config, socket_exist, socket_class, expected_error, expected_id
):
    """Test all raised exceptions."""
    mock_exists.return_value = socket_exist
    with patch(
        f'guardbear.core.guardbear_socket.{socket_class}.__init__',
        return_value=MagicMock() if expected_id == 1121 and socket_exist else None,
    ):
        with patch(f'guardbear.core.guardbear_socket.{socket_class}.send'):
            with patch(
                f'guardbear.core.guardbear_socket.{socket_class}.receive',
                side_effect=ValueError if expected_id == 1118 else None,
                return_value=b'test 1' if expected_id == 1116 else b'test No such file or directory',
            ):
                with patch(f'guardbear.core.guardbear_socket.{socket_class}.close'):
                    with pytest.raises(expected_error, match=f'.* {expected_id} .*'):
                        configuration.get_active_configuration(component, config, agent_id)


@pytest.mark.parametrize(
    'update_check_value, expected',
    [
        (True, True),
        (False, False),
    ],
)
def test_update_check_is_enabled(update_check_value, expected):
    """Test that update_check_is_enabled returns the expected value based on update_check."""
    with patch('guardbear.core.config.client.CentralizedConfig.get_server_config') as mock_get_server_config:
        cti_mock = MagicMock()
        cti_mock.update_check = update_check_value
        server_config_mock = MagicMock()
        server_config_mock.cti = cti_mock
        mock_get_server_config.return_value = server_config_mock

        result = configuration.update_check_is_enabled()
        assert result == expected


@pytest.mark.parametrize(
    'error_code, expected',
    [
        (1101, None),
        (1103, None),
        (1106, True),
    ],
)
def test_update_check_is_enabled_exceptions(error_code, expected):
    """Test that update_check_is_enabled properly handles exceptions."""
    with patch('guardbear.core.config.client.CentralizedConfig.get_server_config', side_effect=GuardBearError(error_code)):
        if expected is not None:
            assert configuration.update_check_is_enabled() == expected
        else:
            with pytest.raises(GuardBearError, match=f'.* {error_code} .*'):
                configuration.update_check_is_enabled()


@pytest.mark.parametrize(
    'cti_url, expected',
    [
        ('https://default-cti.com', 'https://default-cti.com'),
        ('https://test-cti.com', 'https://test-cti.com'),
    ],
)
def test_get_cti_url(cti_url, expected):
    """Test that get_cti_url returns the expected URL based on configuration."""
    with patch('guardbear.core.config.client.CentralizedConfig.get_server_config') as mock_get_server_config:
        cti_mock = MagicMock()
        cti_mock.url = cti_url
        server_config_mock = MagicMock()
        server_config_mock.cti = cti_mock
        mock_get_server_config.return_value = server_config_mock

        result = configuration.get_cti_url()
        assert result == expected


@pytest.mark.parametrize(
    'error_code, expected',
    [
        (1101, None),
        (1103, None),
        (1106, configuration.DEFAULT_CTI_URL),
    ],
)
def test_get_cti_url_exceptions(error_code, expected):
    """Test that get_cti_url properly handles exceptions."""
    with patch('guardbear.core.config.client.CentralizedConfig.get_server_config', side_effect=GuardBearError(error_code)):
        if expected is not None:
            assert configuration.get_cti_url() == expected
        else:
            with pytest.raises(GuardBearError, match=f'.* {error_code} .*'):
                configuration.get_cti_url()
