# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2
from guardbear.core import common

CERTS_PATH = common.GUARDBEAR_ETC / 'certs'

INSTALLATION_UID_PATH = common.GUARDBEAR_LIB / 'installation_uid'
INSTALLATION_UID_KEY = 'installation_uid'
UPDATE_INFORMATION_KEY = 'update_information'

API_KEY_PATH = CERTS_PATH / 'api-key.pem'
API_CERT_PATH = CERTS_PATH / 'api.pem'
