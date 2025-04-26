#!/usr/bin/env bash

# Clone the GuardBear repository
git clone "https://github.com/guardbear/guardbear.git" -b ${GUARDBEAR_BRANCH} --single-branch --depth=1 ${GUARDBEAR_ROOT}

cd ${GUARDBEAR_ROOT}

git submodule update --init --recursive

# Install the server
USER_LANGUAGE="en"                   \
USER_NO_STOP="y"                     \
USER_CA_STORE="/path/to/my_cert.pem" \
DOWNLOAD_CONTENT="y"                 \
./install.sh
