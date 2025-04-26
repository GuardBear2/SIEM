# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from unittest.mock import patch

import pytest

from server_management_api.uri_parser import LOWER_FIELDS, APIUriParser


@pytest.mark.parametrize('query_parm', LOWER_FIELDS)
def test_apiuriparser_resolve_params(query_parm):
    """Test Parameter Sanitization."""
    uri_parser = APIUriParser({}, {})
    with patch('connexion.uri_parsing.AbstractURIParser.resolve_params') as resolv_mock:

        def side_effect_resolve_param(params, _in):
            return params

        resolv_mock.side_effect = side_effect_resolve_param
        parm = uri_parser.resolve_params({query_parm: 'ValuE'}, 'query')
        resolv_mock.assert_called_once_with(parm, 'query')
