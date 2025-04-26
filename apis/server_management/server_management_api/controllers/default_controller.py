# # Copyright (C) 2015, GuardBear Inc.
# # Created by GuardBear, Inc. <info@guardbear.com>.
# # This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import logging
import socket

from connexion.lifecycle import ConnexionResponse
from guardbear.core.common import DATE_FORMAT
from guardbear.core.results import GuardBearResult
from guardbear.core.security import load_spec
from guardbear.core.utils import get_utc_now

from server_management_api.controllers.util import json_response
from server_management_api.models.basic_info_model import BasicInfo

logger = logging.getLogger('guardbear-api')


async def default_info(pretty: bool = False) -> ConnexionResponse:
    """Return basic information about the GuardBear API.

    Parameters
    ----------
    pretty: bool
        Show results in human-readable format.

    Returns
    -------
    ConnexionResponse
        API response.
    """
    info_data = load_spec()
    data = {
        'title': info_data['info']['title'],
        'api_version': info_data['info']['version'],
        'revision': info_data['info']['x-revision'],
        'license_name': info_data['info']['license']['name'],
        'license_url': info_data['info']['license']['url'],
        'hostname': socket.gethostname(),
        'timestamp': get_utc_now().strftime(DATE_FORMAT),
    }
    data = GuardBearResult({'data': BasicInfo.from_dict(data)})

    return json_response(data, pretty=pretty)
