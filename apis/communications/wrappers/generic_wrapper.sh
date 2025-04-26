#!/bin/sh
# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

WPYTHON_BIN="framework/python/bin/python3"
GUARDBEAR_SHARE="/usr/share/guardbear-server"

SCRIPT_PATH_NAME="$0"
SCRIPT_NAME="$(basename ${SCRIPT_PATH_NAME})"

PYTHON_SCRIPT="${GUARDBEAR_SHARE}/apis/scripts/${SCRIPT_NAME}.py"

${PYTHON_SCRIPT} $@
