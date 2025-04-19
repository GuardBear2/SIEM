#!/usr/bin/env bash

/usr/sbin/sshd
GUARDBEAR_CONFIG_SKIP_API=true /usr/share/guardbear-server/bin/guardbear-engine
