#!/usr/bin/env bash

shutdown() {
    echo "Container stopped, shutting down server..."
    /usr/share/guardbear-server/bin/guardbear-server stop
}

# Trap SIGTERM
trap 'shutdown' SIGTERM

cp /tmp/guardbear-server.yml /etc/guardbear-server/guardbear-server.yml

# Set node's name
sed -i "s:name\: server_01:name\: $2:g" /etc/guardbear-server/guardbear-server.yml

if [ "$3" != "manager" ]
then
    # TODO: rename type name to 'manager' once we do the name migration
    sed -i "s:type\: master:type\: worker:g" /etc/guardbear-server/guardbear-server.yml
fi

chown -R guardbear-server:guardbear-server /etc/guardbear-server/certs

/usr/share/guardbear-server/bin/guardbear-server start &

wait $!
