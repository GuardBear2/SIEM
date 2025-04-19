# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import json
from unittest.mock import patch

import pytest

with patch('guardbear.common.guardbear_uid'):
    with patch('guardbear.common.guardbear_gid'):
        from guardbear.core.indexer.agent import Agent
        from guardbear.core.results import GuardBearResult

        from server_management_api.encoder import dumps, prettify


def custom_hook(dct):
    """Converts a JSON string to the expected dictionary"""
    if 'id' in dct:
        return Agent(**dct)

    if 'key' in dct:
        return {'key': dct['key']}

    if 'error' in dct:
        return GuardBearResult.decode_json({'result': dct, 'str_priority': 'v2'})

    return dct


@pytest.mark.parametrize(
    'o',
    [
        {'key': 'v1'},
        GuardBearResult({'k1': 'v1'}, str_priority='v2'),
        Agent(id='0191e730-f9eb-7794-b2d1-949405d7d6ce', name='test'),
    ],
)
def test_encoder_dumps(o):
    """Test dumps method from API encoder using GuardBearAPIJSONEncoder."""
    encoded = dumps(o)
    decoded = json.loads(encoded, object_hook=custom_hook)
    assert decoded == o


def test_encoder_prettify():
    """Test prettify method from API encoder using GuardBearAPIJSONEncoder."""
    assert prettify({'k1': 'v1'}) == '{\n   "k1": "v1"\n}'
