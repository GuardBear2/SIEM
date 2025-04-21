#!/bin/bash

[ "$(/usr/share/guardbear-server/bin/guardbear-server status | grep -E 'guardbear-server is running' | wc -l)" == 1 ] || exit 1
exit 0
