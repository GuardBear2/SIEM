#!/bin/bash
set -e

# Fix line endings in helper scripts inside container if needed
if [ -f "/usr/local/bin/helper_function.sh" ]; then
  sed -i 's/\r$//' /usr/local/bin/helper_function.sh
fi
if [ -f "/tmp/gen_permissions.sh" ]; then
  sed -i 's/\r$//' /tmp/gen_permissions.sh
fi

# Create symlinks to handle path mismatches
if [ -d "/guardbear-local-src" ] && [ ! -d "/wazuh-local-src" ]; then
  ln -s /guardbear-local-src /wazuh-local-src
elif [ -d "/wazuh-local-src" ] && [ ! -d "/guardbear-local-src" ]; then
  ln -s /wazuh-local-src /guardbear-local-src
fi

# Run the build script with all the arguments passed to this script
/wazuh-local-src/packages/build.sh "$@" 