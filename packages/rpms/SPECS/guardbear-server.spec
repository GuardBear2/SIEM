%if %{_isstage} == no
  %define _rpmfilename %%{NAME}_%%{VERSION}-%%{RELEASE}_%%{ARCH}_%{_hashcommit}.rpm
%else
  %define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%endif

Summary:     GuardBear helps you to gain security visibility into your infrastructure by monitoring hosts at an operating system and application level. It provides the following capabilities: log analysis, file integrity monitoring, intrusions detection and policy and compliance monitoring
Name:        guardbear-server
Version:     %{_version}
Release:     %{_release}
License:     GPL
Group:       System Environment/Daemons
Source0:     %{name}-%{version}.tar.gz
URL:         https://www.guardbear.com/
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:      GuardBear, Inc <info@guardbear.com>
Packager:    GuardBear, Inc <info@guardbear.com>
Requires(pre):    /usr/sbin/groupadd /usr/sbin/useradd
Requires(postun): /usr/sbin/groupdel /usr/sbin/userdel
AutoReqProv: no

Requires: coreutils
BuildRequires: coreutils glibc-devel automake autoconf libtool policycoreutils-python curl perl

ExclusiveOS: linux

%define _source_payload w9.xzdio
%define _binary_payload w9.xzdio

%define _guardbear_user guardbear-server
%define _guardbear_group guardbear-server

%description
GuardBear helps you to gain security visibility into your infrastructure by monitoring
hosts at an operating system and application level. It provides the following capabilities:
log analysis, file integrity monitoring, intrusions detection and policy and compliance monitoring

# Don't generate build_id links to prevent conflicts with other
# packages.
%global _build_id_links none

# Build debuginfo package
%debug_package
%package guardbear-server-debuginfo
Summary: Debug information for package %{name}.
%description guardbear-server-debuginfo
This package provides debug information for package %{name}.

%prep
%setup -q
%build
%install
# Clean BUILDROOT
rm -fr %{buildroot}
echo 'VCPKG_ROOT="/root/vcpkg"' > ./etc/preloaded-vars.conf
echo 'USER_LANGUAGE="en"' > ./etc/preloaded-vars.conf
echo 'USER_NO_STOP="y"' >> ./etc/preloaded-vars.conf
echo 'USER_INSTALL_TYPE="server"' >> ./etc/preloaded-vars.conf
echo 'USER_DIR="%{_localstatedir}"' >> ./etc/preloaded-vars.conf
echo 'USER_DELETE_DIR="y"' >> ./etc/preloaded-vars.conf
echo 'USER_UPDATE="n"' >> ./etc/preloaded-vars.conf
echo 'USER_ENABLE_EMAIL="n"' >> ./etc/preloaded-vars.conf
echo 'USER_WHITE_LIST="n"' >> ./etc/preloaded-vars.conf
echo 'USER_ENABLE_SYSLOG="y"' >> ./etc/preloaded-vars.conf
echo 'USER_ENABLE_AUTHD="y"' >> ./etc/preloaded-vars.conf
echo 'USER_SERVER_IP="MANAGER_IP"' >> ./etc/preloaded-vars.conf
echo 'USER_CA_STORE="/path/to/my_cert.pem"' >> ./etc/preloaded-vars.conf
echo 'USER_GENERATE_AUTHD_CERT="y"' >> ./etc/preloaded-vars.conf
echo 'USER_AUTO_START="n"' >> ./etc/preloaded-vars.conf
echo 'USER_CREATE_SSL_CERT="n"' >> ./etc/preloaded-vars.conf
echo 'DOWNLOAD_CONTENT="y"' >> ./etc/preloaded-vars.conf
export VCPKG_ROOT="/root/vcpkg"
export PATH="${PATH}:${VCPKG_ROOT}"
scl enable devtoolset-11 ./install.sh

# Create directories
mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}

# Copy the installed files into RPM_BUILD_ROOT directory
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}var/lib/guardbear-server
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}usr/bin
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}var/log
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}usr/share/guardbear-server
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}usr/share/guardbear-server/bin
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}etc/guardbear-server

cp -p %{_localstatedir}usr/share/guardbear-server/bin/guardbear-engine ${RPM_BUILD_ROOT}%{_localstatedir}usr/share/guardbear-server/bin/
cp -p %{_localstatedir}usr/share/guardbear-server/bin/guardbear-server-management-apid ${RPM_BUILD_ROOT}%{_localstatedir}usr/share/guardbear-server/bin/
cp -p %{_localstatedir}usr/share/guardbear-server/bin/guardbear-comms-apid ${RPM_BUILD_ROOT}%{_localstatedir}usr/share/guardbear-server/bin/
cp -p %{_localstatedir}usr/share/guardbear-server/bin/guardbear-server ${RPM_BUILD_ROOT}%{_localstatedir}usr/share/guardbear-server/bin/
cp -p %{_localstatedir}usr/share/guardbear-server/bin/guardbear-keystore ${RPM_BUILD_ROOT}%{_localstatedir}usr/share/guardbear-server/bin/

cp -pr %{_localstatedir}var/lib/guardbear-server ${RPM_BUILD_ROOT}%{_localstatedir}var/lib/
cp -pr %{_localstatedir}usr/share/guardbear-server ${RPM_BUILD_ROOT}%{_localstatedir}usr/share/
cp -pr %{_localstatedir}etc/guardbear-server ${RPM_BUILD_ROOT}%{_localstatedir}etc/

sed -i "s:GUARDBEAR_HOME_TMP:%{_localstatedir}:g" src/init/templates/guardbear-server-rh.init
install -m 0755 src/init/templates/guardbear-server-rh.init ${RPM_BUILD_ROOT}%{_initrddir}/guardbear-server

mkdir -p ${RPM_BUILD_ROOT}/usr/lib/systemd/system/
sed -i "s:GUARDBEAR_HOME_TMP:%{_localstatedir}:g" src/init/templates/guardbear-server.service
install -m 0644 src/init/templates/guardbear-server.service ${RPM_BUILD_ROOT}/usr/lib/systemd/system/

%{_rpmconfigdir}/find-debuginfo.sh

%pre

# Create the guardbear group if it doesn't exists
if command -v getent > /dev/null 2>&1 && ! getent group %{_guardbear_user} > /dev/null 2>&1; then
  groupadd -r %{_guardbear_user}
elif ! getent group %{_guardbear_user} > /dev/null 2>&1; then
  groupadd -r %{_guardbear_user}
fi

# Create the guardbear user if it doesn't exists
if ! getent passwd %{_guardbear_user} > /dev/null 2>&1; then
  useradd -g %{_guardbear_user} -G %{_guardbear_user} -d %{_localstatedir} -r -s /sbin/nologin %{_guardbear_user}
fi

# Stop the services to upgrade the package
if [ $1 = 2 ]; then
  if command -v systemctl > /dev/null 2>&1 && systemctl > /dev/null 2>&1 && systemctl is-active --quiet guardbear-server > /dev/null 2>&1; then
    systemctl stop guardbear-server.service > /dev/null 2>&1
    touch %{_localstatedir}/tmp/guardbear.restart
  # Check for SysV
  elif command -v service > /dev/null 2>&1 && service guardbear-server status 2>/dev/null | grep "is running" > /dev/null 2>&1; then
    service guardbear-server stop > /dev/null 2>&1
    touch %{_localstatedir}/tmp/guardbear.restart
  else
    echo "Unable to stop guardbear-server. Neither systemctl nor service are available."
  fi
fi

%post

%define _vdfilename vd_1.0.0_vd_4.10.0.tar.xz

if [[ -d /run/systemd/system ]]; then
  rm -f %{_initrddir}/guardbear-server
fi

%preun

if [ $1 = 0 ]; then

  # Stop the services before uninstall the package
  # Check for systemd
  if command -v systemctl > /dev/null 2>&1 && systemctl > /dev/null 2>&1 && systemctl is-active --quiet guardbear-server > /dev/null 2>&1; then
    systemctl stop guardbear-server.service > /dev/null 2>&1
  # Check for SysV
  elif command -v service > /dev/null 2>&1 && service guardbear-server status 2>/dev/null | grep "is running" > /dev/null 2>&1; then
    service guardbear-server stop > /dev/null 2>&1
  else
    echo "Unable to stop guardbear-server. Neither systemctl nor service are available."
  fi
fi

%postun

# If the package is been uninstalled
if [ $1 = 0 ];then
  # Remove the guardbear user if it exists
  if getent passwd %{_guardbear_user} > /dev/null 2>&1; then
    userdel %{_guardbear_user} >/dev/null 2>&1
  fi
  # Remove the guardbear group if it exists
  if command -v getent > /dev/null 2>&1 && getent group %{_guardbear_group} > /dev/null 2>&1; then
    groupdel %{_guardbear_group} >/dev/null 2>&1
  elif getent group %{_guardbear_group} > /dev/null 2>&1; then
    groupdel %{_guardbear_group} >/dev/null 2>&1
  fi

  # Remove lingering folders and files
  rm -rf %{_localstatedir}run/guardbear-server
  rm -rf %{_localstatedir}var/lib/guardbear-server
  rm -rf %{_localstatedir}usr/share/guardbear-server
  rm -rf %{_localstatedir}etc/guardbear-server
fi

# posttrans code is the last thing executed in a install/upgrade
%posttrans
if [ -f %{_sysconfdir}/systemd/system/guardbear-server.service ]; then
  rm -rf %{_sysconfdir}/systemd/system/guardbear-server.service
  systemctl daemon-reload > /dev/null 2>&1
fi

if [ -f %{_localstatedir}/tmp/guardbear.restart ]; then
  rm -f %{_localstatedir}/tmp/guardbear.restart
  if command -v systemctl > /dev/null 2>&1 && systemctl > /dev/null 2>&1 ; then
    systemctl daemon-reload > /dev/null 2>&1
    systemctl restart guardbear-server.service > /dev/null 2>&1
  elif command -v service > /dev/null 2>&1 ; then
    service guardbear-server restart > /dev/null 2>&1
  fi
fi

chown -R %{_guardbear_user}:%{_guardbear_group} %{_localstatedir}var/lib/guardbear-server
find %{_localstatedir}var/lib/guardbear-server -type d -exec chmod 750 {} \; -o -type f -exec chmod 640 {} \;
chown -R %{_guardbear_user}:%{_guardbear_group} %{_localstatedir}usr/share/guardbear-server
find %{_localstatedir}usr/share/guardbear-server -type d -exec chmod 755 {} \; -o -type f -exec chmod 644 {} \;
chown -R %{_guardbear_user}:%{_guardbear_group} %{_localstatedir}etc/guardbear-server
find %{_localstatedir}etc/guardbear-server -type d -exec chmod 755 {} \; -o -type f -exec chmod 644 {} \;

# Binaries
chmod 750 %{_localstatedir}usr/share/guardbear-server/bin/guardbear-engine
chown %{_guardbear_user}:%{_guardbear_group} %{_localstatedir}usr/share/guardbear-server/bin/guardbear-engine
chmod 750 %{_localstatedir}usr/share/guardbear-server/bin/guardbear-server-management-apid
chown %{_guardbear_user}:%{_guardbear_group} %{_localstatedir}usr/share/guardbear-server/bin/guardbear-server-management-apid
chmod 750 %{_localstatedir}usr/share/guardbear-server/bin/guardbear-comms-apid
chown %{_guardbear_user}:%{_guardbear_group} %{_localstatedir}usr/share/guardbear-server/bin/guardbear-comms-apid
chmod 750 %{_localstatedir}usr/share/guardbear-server/bin/guardbear-server
chown %{_guardbear_user}:%{_guardbear_group} %{_localstatedir}usr/share/guardbear-server/bin/guardbear-server

# Scripts
chmod 750 %{_localstatedir}usr/share/guardbear-server/framework/scripts/guardbear-server.py
chown %{_guardbear_user}:%{_guardbear_group} %{_localstatedir}usr/share/guardbear-server/framework/scripts/guardbear-server.py
chmod 750 %{_localstatedir}usr/share/guardbear-server/apis/scripts/guardbear-comms-apid.py
chown %{_guardbear_user}:%{_guardbear_group} %{_localstatedir}usr/share/guardbear-server/apis/scripts/guardbear-comms-apid.py
chmod 750 %{_localstatedir}usr/share/guardbear-server/apis/scripts/guardbear-server-management-apid.py
chown %{_guardbear_user}:%{_guardbear_group} %{_localstatedir}usr/share/guardbear-server/apis/scripts/guardbear-server-management-apid.py

# Fix Python permissions
chmod -R 0750 %{_localstatedir}usr/share/guardbear-server/framework/python/bin

# Fix binaries permissions
chmod -R 0750 %{_localstatedir}usr/share/guardbear-server/bin

%triggerin -- glibc

%clean
rm -fr %{buildroot}

%files
%defattr(-, %{_guardbear_user}, %{_guardbear_group})
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}var/lib/guardbear-server
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}var/lib/guardbear-server/vd
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}var/lib/guardbear-server/tmp
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}var/lib/guardbear-server/engine
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}var/lib/guardbear-server/engine/tzdb
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}etc/guardbear-server
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}etc/guardbear-server/certs
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}etc/guardbear-server/cluster
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}etc/guardbear-server/groups
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}usr/share/guardbear-server/lib
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}usr/share/guardbear-server/framework
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}usr/share/guardbear-server/apis
%{_localstatedir}var/lib/guardbear-server/engine/tzdb/*
%{_localstatedir}etc/guardbear-server/*
%{_localstatedir}usr/share/guardbear-server/lib/*
%{_localstatedir}usr/share/guardbear-server/framework/*
%{_localstatedir}usr/share/guardbear-server/apis/*
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}var/lib/guardbear-server/engine/store
%{_localstatedir}var/lib/guardbear-server/engine/store/*
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}var/lib/guardbear-server/engine/kvdb
%{_localstatedir}var/lib/guardbear-server/engine/kvdb/*
%dir %attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}var/lib/guardbear-server/indexer-connector

%attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}usr/share/guardbear-server/bin/guardbear-engine
%attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}usr/share/guardbear-server/bin/guardbear-server-management-apid
%attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}usr/share/guardbear-server/bin/guardbear-comms-apid
%attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}usr/share/guardbear-server/bin/guardbear-server
%attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}usr/share/guardbear-server/bin/guardbear-keystore
# This will be correctly added in #26936
%attr(750, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}usr/share/guardbear-server/bin/rbac_control
%attr(640, %{_guardbear_user}, %{_guardbear_group}) %{_localstatedir}var/lib/guardbear-server/tmp/vd_1.0.0_vd_4.10.0.tar.xz

%config(missingok) %{_initrddir}/guardbear-server
/usr/lib/systemd/system/guardbear-server.service

%changelog
* Mon Jun 2 2025 support <info@guardbear.com> - 5.0.0
- More info: https://documentation.guardbear.com/current/release-notes/release-5-0-0.html
