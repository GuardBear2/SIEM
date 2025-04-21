## variables
APT_KEY=https://packages-dev.guardbear.com/key/GPG-KEY-GUARDBEAR
GPG_SIGN="gpgcheck=1\ngpgkey=${APT_KEY}]"
REPOSITORY="[guardbear]\n${GPG_SIGN}\nenabled=1\nname=EL-\$releasever - GuardBear\nbaseurl=https://packages-dev.guardbear.com/pre-release/yum/\nprotect=1"
GUARDBEAR_TAG=$(curl --silent https://api.github.com/repos/guardbear/guardbear/git/refs/tags | grep '["]ref["]:' | sed -E 's/.*\"([^\"]+)\".*/\1/'  | cut -c 11- | grep ^v${GUARDBEAR_VERSION}$)

## check tag to use the correct repository
if [[ -n "${GUARDBEAR_TAG}" ]]; then
  APT_KEY=https://packages.guardbear.com/key/GPG-KEY-GUARDBEAR
  GPG_SIGN="gpgcheck=1\ngpgkey=${APT_KEY}]"
  REPOSITORY="[guardbear]\n${GPG_SIGN}\nenabled=1\nname=EL-\$releasever - GuardBear\nbaseurl=https://packages.guardbear.com/4.x/yum/\nprotect=1"
fi

rpm --import "${APT_KEY}"
echo -e "${REPOSITORY}" | tee /etc/yum.repos.d/guardbear.repo
