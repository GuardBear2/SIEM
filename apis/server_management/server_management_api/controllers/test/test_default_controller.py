# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import sys
from unittest.mock import MagicMock, patch

import pytest
from connexion.lifecycle import ConnexionResponse

with patch('guardbear.common.guardbear_uid'):
    with patch('guardbear.common.guardbear_gid'):
        sys.modules['guardbear.rbac.orm'] = MagicMock()
        import guardbear.rbac.decorators
        from guardbear.core.utils import get_utc_now
        from guardbear.tests.util import RBAC_bypasser

        from server_management_api.controllers.default_controller import DATE_FORMAT, BasicInfo, default_info, socket

        guardbear.rbac.decorators.expose_resources = RBAC_bypasser
        del sys.modules['guardbear.rbac.orm']


@pytest.mark.asyncio
@patch('server_management_api.controllers.default_controller.load_spec', return_value=MagicMock())
@patch('server_management_api.controllers.default_controller.GuardBearResult', return_value={})
async def test_default_info(mock_wresult, mock_lspec):
    """Verify 'default_info' endpoint is working as expected."""
    result = await default_info()
    data = {
        'title': mock_lspec.return_value['info']['title'],
        'api_version': mock_lspec.return_value['info']['version'],
        'revision': mock_lspec.return_value['info']['x-revision'],
        'license_name': mock_lspec.return_value['info']['license']['name'],
        'license_url': mock_lspec.return_value['info']['license']['url'],
        'hostname': socket.gethostname(),
        'timestamp': get_utc_now().strftime(DATE_FORMAT),
    }
    mock_lspec.assert_called_once_with()
    mock_wresult.assert_called_once_with({'data': BasicInfo.from_dict(data)})
    assert isinstance(result, ConnexionResponse)
