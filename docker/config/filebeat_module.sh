## variables
REPOSITORY="packages-dev.guardbear.com/pre-release"
GUARDBEAR_TAG=$(curl --silent https://api.github.com/repos/guardbear/guardbear/git/refs/tags | grep '["]ref["]:' | sed -E 's/.*\"([^\"]+)\".*/\1/'  | cut -c 11- | grep ^v${GUARDBEAR_VERSION}$)

## check tag to use the correct repository
if [[ -n "${GUARDBEAR_TAG}" ]]; then
  REPOSITORY="packages.guardbear.com/4.x"
fi

curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/${FILEBEAT_CHANNEL}-${FILEBEAT_VERSION}-x86_64.rpm &&\
yum install -y ${FILEBEAT_CHANNEL}-${FILEBEAT_VERSION}-x86_64.rpm && rm -f ${FILEBEAT_CHANNEL}-${FILEBEAT_VERSION}-x86_64.rpm && \
curl -s https://${REPOSITORY}/filebeat/${GUARDBEAR_FILEBEAT_MODULE} | tar -xvz -C /usr/share/filebeat/module
