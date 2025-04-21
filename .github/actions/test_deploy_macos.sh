#!/bin/bash

# Copyright (C) 2015, GuardBear Inc.
#
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.

# Global variables
VERSION="$(sed 's/v//' src/VERSION)"
MAJOR=$(echo "${VERSION}" | cut -dv -f2 | cut -d. -f1)
MINOR=$(echo "${VERSION}" | cut -d. -f2)
SHA="$(git rev-parse --short=7 "$1")"

GUARDBEAR_MACOS_AGENT_DEPLOYMENT_VARS="/tmp/guardbear_envs"
conf_path="/Library/Ossec/etc/ossec.conf"

VARS=( "GUARDBEAR_MANAGER" "GUARDBEAR_MANAGER_PORT" "GUARDBEAR_PROTOCOL" "GUARDBEAR_REGISTRATION_SERVER" "GUARDBEAR_REGISTRATION_PORT" "GUARDBEAR_REGISTRATION_PASSWORD" "GUARDBEAR_KEEP_ALIVE_INTERVAL" "GUARDBEAR_TIME_RECONNECT" "GUARDBEAR_REGISTRATION_CA" "GUARDBEAR_REGISTRATION_CERTIFICATE" "GUARDBEAR_REGISTRATION_KEY" "GUARDBEAR_AGENT_NAME" "GUARDBEAR_AGENT_GROUP" "ENROLLMENT_DELAY" )
VALUES=( "1.1.1.1" "7777" "udp" "2.2.2.2" "8888" "password" "10" "10" "/Library/Ossec/etc/testsslmanager.cert" "/Library/Ossec/etc/testsslmanager.cert" "/Library/Ossec/etc/testsslmanager.key" "test-agent" "test-group" "10" )
TAGS1=( "<address>" "<port>" "<protocol>" "<manager_address>" "<port>" "<password>" "<notify_time>" "<time-reconnect>" "<server_ca_path>" "<agent_certificate_path>" "<agent_key_path>" "<agent_name>" "<groups>" "<delay_after_enrollment>" )
TAGS2=( "</address>" "</port>" "</protocol>" "</manager_address>" "</port>" "</password>" "</notify_time>" "</time-reconnect>" "</server_ca_path>" "</agent_certificate_path>" "</agent_key_path>" "</agent_name>" "</groups>" "</delay_after_enrollment>" )
GUARDBEAR_REGISTRATION_PASSWORD_PATH="/Library/Ossec/etc/authd.pass"

function install_guardbear(){

  echo "Testing the following variables $1"

  eval "echo \"$1\" > ${GUARDBEAR_MACOS_AGENT_DEPLOYMENT_VARS} && installer -pkg guardbear-agent-${VERSION}-0.commit${SHA}.pkg -target / > /dev/null 2>&1"
  
}

function remove_guardbear () {

  /bin/rm -r /Library/Ossec > /dev/null 2>&1
  /bin/launchctl unload /Library/LaunchDaemons/com.guardbear.agent.plist > /dev/null 2>&1
  /bin/rm -f /Library/LaunchDaemons/com.guardbear.agent.plist > /dev/null 2>&1
  /bin/rm -rf /Library/StartupItems/GUARDBEAR > /dev/null 2>&1
  /usr/bin/dscl . -delete "/Users/guardbear" > /dev/null 2>&1
  /usr/bin/dscl . -delete "/Groups/guardbear" > /dev/null 2>&1
  /usr/sbin/pkgutil --forget com.guardbear.pkg.guardbear-agent > /dev/null 2>&1

}

function test() {

  for i in "${!VARS[@]}"; do
    if ( echo "${@}" | grep -q -w "${VARS[i]}" ); then
      if [ "${VARS[i]}" == "GUARDBEAR_MANAGER" ] || [ "${VARS[i]}" == "GUARDBEAR_PROTOCOL" ]; then
        LIST=( "${VALUES[i]//,/ }" )
        for j in "${!LIST[@]}"; do
          if ( grep -q "${TAGS1[i]}${LIST[j]}${TAGS2[i]}" "${conf_path}" ); then
            echo "The variable ${VARS[i]} is set correctly"
          else
            echo "The variable ${VARS[i]} is not set correctly"
            exit 1
          fi
        done
      elif [ "${VARS[i]}" == "GUARDBEAR_REGISTRATION_PASSWORD" ]; then
        if ( grep -q "${VALUES[i]}" "${GUARDBEAR_REGISTRATION_PASSWORD_PATH}" ); then
          echo "The variable ${VARS[i]} is set correctly"
        else
          echo "The variable ${VARS[i]} is not set correctly"
          exit 1
        fi
      else
        if ( grep -q "${TAGS1[i]}${VALUES[i]}${TAGS2[i]}" "${conf_path}" ); then
          echo "The variable ${VARS[i]} is set correctly"
        else
          echo "The variable ${VARS[i]} is not set correctly"
          exit 1
        fi
      fi
    fi
  done

}

echo "Download package https://s3.us-west-1.amazonaws.com/packages-dev.guardbear.com/warehouse/pullrequests/${MAJOR}.${MINOR}/macos/guardbear-agent-${VERSION}-0.commit${SHA}.pkg"
wget "https://s3.us-west-1.amazonaws.com/packages-dev.guardbear.com/warehouse/pullrequests/${MAJOR}.${MINOR}/macos/guardbear-agent-${VERSION}-0.commit${SHA}.pkg" > /dev/null 2>&1

install_guardbear "GUARDBEAR_MANAGER='1.1.1.1' && GUARDBEAR_MANAGER_PORT='7777' && GUARDBEAR_PROTOCOL='udp' && GUARDBEAR_REGISTRATION_SERVER='2.2.2.2' && GUARDBEAR_REGISTRATION_PORT='8888' && GUARDBEAR_REGISTRATION_PASSWORD='password' && GUARDBEAR_KEEP_ALIVE_INTERVAL='10' && GUARDBEAR_TIME_RECONNECT='10' && GUARDBEAR_REGISTRATION_CA='/Library/Ossec/etc/testsslmanager.cert' && GUARDBEAR_REGISTRATION_CERTIFICATE='/Library/Ossec/etc/testsslmanager.cert' && GUARDBEAR_REGISTRATION_KEY='/Library/Ossec/etc/testsslmanager.key' && GUARDBEAR_AGENT_NAME='test-agent' && GUARDBEAR_AGENT_GROUP='test-group' && ENROLLMENT_DELAY='10'" 
test "GUARDBEAR_MANAGER GUARDBEAR_MANAGER_PORT GUARDBEAR_PROTOCOL GUARDBEAR_REGISTRATION_SERVER GUARDBEAR_REGISTRATION_PORT GUARDBEAR_REGISTRATION_PASSWORD GUARDBEAR_KEEP_ALIVE_INTERVAL GUARDBEAR_TIME_RECONNECT GUARDBEAR_REGISTRATION_CA GUARDBEAR_REGISTRATION_CERTIFICATE GUARDBEAR_REGISTRATION_KEY GUARDBEAR_AGENT_NAME GUARDBEAR_AGENT_GROUP ENROLLMENT_DELAY" 
remove_guardbear

install_guardbear "GUARDBEAR_MANAGER='1.1.1.1'"
test "GUARDBEAR_MANAGER"
remove_guardbear

install_guardbear "GUARDBEAR_MANAGER_PORT='7777'"
test "GUARDBEAR_MANAGER_PORT"
remove_guardbear

install_guardbear "GUARDBEAR_PROTOCOL='udp'"
test "GUARDBEAR_PROTOCOL"
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_SERVER='2.2.2.2'"
test "GUARDBEAR_REGISTRATION_SERVER"
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_PORT='8888'"
test "GUARDBEAR_REGISTRATION_PORT"
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_PASSWORD='password'"
test "GUARDBEAR_REGISTRATION_PASSWORD"
remove_guardbear

install_guardbear "GUARDBEAR_KEEP_ALIVE_INTERVAL='10'"
test "GUARDBEAR_KEEP_ALIVE_INTERVAL"
remove_guardbear

install_guardbear "GUARDBEAR_TIME_RECONNECT='10'"
test "GUARDBEAR_TIME_RECONNECT"
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_CA='/Library/Ossec/etc/testsslmanager.cert'"
test "GUARDBEAR_REGISTRATION_CA"
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_CERTIFICATE='/Library/Ossec/etc/testsslmanager.cert'"
test "GUARDBEAR_REGISTRATION_CERTIFICATE"
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_KEY='/Library/Ossec/etc/testsslmanager.key'"
test "GUARDBEAR_REGISTRATION_KEY"
remove_guardbear

install_guardbear "GUARDBEAR_AGENT_NAME='test-agent'"
test "GUARDBEAR_AGENT_NAME"
remove_guardbear

install_guardbear "GUARDBEAR_AGENT_GROUP='test-group'"
test "GUARDBEAR_AGENT_GROUP"
remove_guardbear

install_guardbear "ENROLLMENT_DELAY='10'"
test "ENROLLMENT_DELAY"
remove_guardbear
