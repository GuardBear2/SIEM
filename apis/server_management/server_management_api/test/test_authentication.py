# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import hashlib
import json
import os
import sys
from copy import deepcopy
from unittest.mock import ANY, MagicMock, call, patch

from connexion.exceptions import Unauthorized

with patch('guardbear.core.common.guardbear_uid'):
    with patch('guardbear.core.common.guardbear_gid'):
        from guardbear.core.results import GuardBearResult

import pytest

with patch('guardbear.core.common.guardbear_uid'):
    with patch('guardbear.core.common.guardbear_gid'):
        sys.modules['guardbear.rbac.orm'] = MagicMock()
        from server_management_api import authentication

        del sys.modules['guardbear.rbac.orm']

test_path = os.path.dirname(os.path.realpath(__file__))
test_data_path = os.path.join(test_path, 'data')

security_conf = GuardBearResult({'auth_token_exp_timeout': 900, 'rbac_mode': 'black'})
decoded_payload = {
    'iss': 'guardbear',
    'aud': 'GuardBear API REST',
    'nbf': 0,
    'exp': security_conf['auth_token_exp_timeout'],
    'sub': '001',
    'rbac_policies': {'value': 'test', 'rbac_mode': security_conf['rbac_mode']},
    'rbac_roles': [1],
    'run_as': False,
}

original_payload = {
    'iss': 'guardbear',
    'aud': 'GuardBear API REST',
    'nbf': 0,
    'exp': security_conf['auth_token_exp_timeout'],
    'sub': '001',
    'run_as': False,
    'rbac_roles': [1],
    'rbac_mode': security_conf['rbac_mode'],
}


def test_check_user_master():
    """Check that the `check_user_master` function works as expected."""
    result = authentication.check_user_master('test_user', 'test_pass')
    assert result == {'result': True}


@pytest.mark.asyncio
@patch('guardbear.core.cluster.dapi.dapi.DistributedAPI.__init__', return_value=None)
@patch('guardbear.core.cluster.dapi.dapi.DistributedAPI.distribute_function', side_effect=None)
@patch('server_management_api.authentication.raise_if_exc', side_effect=None)
async def test_check_user(mock_raise_if_exc, mock_distribute_function, mock_dapi):
    """Verify if result is as expected."""
    result = authentication.check_user('test_user', 'test_pass')

    assert result == {'sub': 'test_user', 'active': True}, 'Result is not as expected'
    mock_dapi.assert_called_once_with(
        f=ANY,
        f_kwargs={'user': 'test_user', 'password': 'test_pass'},
        request_type='local_master',
        is_async=False,
        wait_for_complete=False,
        logger=ANY,
    )
    mock_distribute_function.assert_called_once_with()
    mock_raise_if_exc.assert_called_once()


def test_get_security_conf():
    """Check that returned object is as expected."""
    result = authentication.get_security_conf()
    assert isinstance(result, dict)
    assert all(x in result.keys() for x in ('auth_token_exp_timeout', 'rbac_mode'))


@pytest.mark.asyncio
@pytest.mark.parametrize('auth_context', [{'name': 'initial_auth'}, None])
@patch('server_management_api.authentication.jwt.encode', return_value='test_token')
@patch(
    'server_management_api.authentication.get_keypair',
    return_value=('-----BEGIN PRIVATE KEY-----', '-----BEGIN PUBLIC KEY-----'),
)
@patch('guardbear.core.cluster.dapi.dapi.DistributedAPI.__init__', return_value=None)
@patch('guardbear.core.cluster.dapi.dapi.DistributedAPI.distribute_function', side_effect=None)
@patch('server_management_api.authentication.raise_if_exc', side_effect=None)
async def test_generate_token(
    mock_raise_if_exc, mock_distribute_function, mock_dapi, mock_get_keypair, mock_encode, auth_context
):
    """Verify if result is as expected."""

    class NewDatetime:
        def timestamp(self) -> float:
            return 0

    mock_raise_if_exc.return_value = security_conf
    with patch('server_management_api.authentication.core_utils.get_utc_now', return_value=NewDatetime()):
        result = authentication.generate_token(user_id='001', data={'roles': [1]}, auth_context=auth_context)
    assert result == 'test_token', 'Result is not as expected'

    # Check all functions are called with expected params
    mock_dapi.assert_called_once_with(
        f=ANY, request_type='local_master', is_async=False, wait_for_complete=False, logger=ANY
    )
    mock_distribute_function.assert_called_once_with()
    mock_raise_if_exc.assert_called_once()
    mock_get_keypair.assert_called_once()
    expected_payload = original_payload | (
        {
            'hash_auth_context': hashlib.blake2b(json.dumps(auth_context).encode(), digest_size=16).hexdigest(),
            'run_as': True,
        }
        if auth_context is not None
        else {}
    )
    mock_encode.assert_called_once_with(expected_payload, '-----BEGIN PRIVATE KEY-----', algorithm='RS256')


@patch('server_management_api.authentication.TokenManager')
def test_check_token(mock_tokenmanager):
    """Check that the `check_token` function works as expected."""
    result = authentication.check_token(
        username='guardbear_user', roles=tuple([1]), token_nbf_time=3600, run_as=False, origin_node_type='master'
    )
    assert result == {'valid': ANY, 'policies': ANY}


@pytest.mark.asyncio
@patch('server_management_api.authentication.jwt.decode')
@patch(
    'server_management_api.authentication.get_keypair',
    return_value=('-----BEGIN PRIVATE KEY-----', '-----BEGIN PUBLIC KEY-----'),
)
@patch('guardbear.core.cluster.dapi.dapi.DistributedAPI.__init__', return_value=None)
@patch('guardbear.core.cluster.dapi.dapi.DistributedAPI.distribute_function', return_value=True)
@patch('server_management_api.authentication.raise_if_exc', side_effect=None)
async def test_decode_token(mock_raise_if_exc, mock_distribute_function, mock_dapi, mock_get_keypair, mock_decode):
    """Check that the `decode_token` function works as expected."""
    mock_decode.return_value = deepcopy(original_payload)
    mock_raise_if_exc.side_effect = [
        GuardBearResult({'valid': True, 'policies': {'value': 'test'}}),
        GuardBearResult(security_conf),
    ]

    result = authentication.decode_token('test_token')
    assert result == decoded_payload

    # Check all functions are called with expected params
    calls = [
        call(
            f=ANY,
            f_kwargs={
                'username': original_payload['sub'],
                'token_nbf_time': original_payload['nbf'],
                'run_as': False,
                'roles': tuple(original_payload['rbac_roles']),
                'origin_node_type': 'master',
            },
            request_type='local_master',
            is_async=False,
            wait_for_complete=False,
            logger=ANY,
        ),
        call(f=ANY, request_type='local_master', is_async=False, wait_for_complete=False, logger=ANY),
    ]
    mock_dapi.assert_has_calls(calls)
    mock_get_keypair.assert_called_once()
    mock_decode.assert_called_once_with(
        'test_token', '-----BEGIN PUBLIC KEY-----', algorithms=['RS256'], audience='GuardBear API REST'
    )
    assert mock_distribute_function.call_count == 2
    assert mock_raise_if_exc.call_count == 2


@pytest.mark.asyncio
@patch('guardbear.core.cluster.dapi.dapi.DistributedAPI.distribute_function', side_effect=None)
@patch('server_management_api.authentication.raise_if_exc', side_effect=None)
@patch(
    'server_management_api.authentication.get_keypair',
    return_value=('-----BEGIN PRIVATE KEY-----', '-----BEGIN PUBLIC KEY-----'),
)
async def test_decode_token_ko(mock_get_keypair, mock_raise_if_exc, mock_distribute_function):
    """Assert exceptions are handled as expected inside decode_token()."""
    with pytest.raises(Unauthorized):
        authentication.decode_token(token='test_token')

    with patch('server_management_api.authentication.jwt.decode') as mock_decode:
        with patch(
            'server_management_api.authentication.get_keypair',
            return_value=('-----BEGIN PRIVATE KEY-----', '-----BEGIN PUBLIC KEY-----'),
        ):
            with patch('guardbear.core.cluster.dapi.dapi.DistributedAPI.__init__', return_value=None):
                with patch('guardbear.core.cluster.dapi.dapi.DistributedAPI.distribute_function'):
                    with patch('server_management_api.authentication.raise_if_exc') as mock_raise_if_exc:
                        mock_decode.return_value = deepcopy(original_payload)

                        with pytest.raises(Unauthorized):
                            mock_raise_if_exc.side_effect = [GuardBearResult({'valid': False})]
                            authentication.decode_token(token='test_token')

                        with pytest.raises(Unauthorized):
                            mock_raise_if_exc.side_effect = [
                                GuardBearResult({'valid': True, 'policies': {'value': 'test'}}),
                                GuardBearResult({'auth_token_exp_timeout': 900, 'rbac_mode': 'white'}),
                            ]
                            authentication.decode_token(token='test_token')
