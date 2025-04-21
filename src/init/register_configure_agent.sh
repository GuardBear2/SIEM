#!/bin/bash

# Copyright (C) 2015, GuardBear Inc.
#
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.

# Global variables
INSTALLDIR=${1}
CONF_FILE="${INSTALLDIR}/etc/ossec.conf"
TMP_ENROLLMENT="${INSTALLDIR}/tmp/enrollment-configuration"
TMP_SERVER="${INSTALLDIR}/tmp/server-configuration"
GUARDBEAR_REGISTRATION_PASSWORD_PATH="etc/authd.pass"
GUARDBEAR_MACOS_AGENT_DEPLOYMENT_VARS="/tmp/guardbear_envs"


# Set default sed alias
sed="sed -ri"
# By default, use gnu sed (gsed).
use_unix_sed="False"

# Special function to use generic sed
unix_sed() {

    sed_expression="$1"
    target_file="$2"
    special_args="$3"

    sed ${special_args} "${sed_expression}" "${target_file}" > "${target_file}.tmp"
    cat "${target_file}.tmp" > "${target_file}"
    rm "${target_file}.tmp"

}

# Update the value of a XML tag inside the ossec.conf
edit_value_tag() {

    file=""

    if [ -z "$3" ]; then
        file="${CONF_FILE}"
    else
        file="${TMP_ENROLLMENT}"
    fi

    if [ -n "$1" ] && [ -n "$2" ]; then
        start_config="$(grep -n "<$1>" "${file}" | cut -d':' -f 1)"
        end_config="$(grep -n "</$1>" "${file}" | cut -d':' -f 1)"
        if [ -z "${start_config}" ] && [ -z "${end_config}" ] && [ "${file}" = "${TMP_ENROLLMENT}" ]; then
            echo "      <$1>$2</$1>" >> "${file}"
        elif [ "${use_unix_sed}" = "False" ] ; then
            ${sed} "s#<$1>.*</$1>#<$1>$2</$1>#g" "${file}"
        else
            unix_sed "s#<$1>.*</$1>#<$1>$2</$1>#g" "${file}"
        fi
    fi
    
    if [ "$?" != "0" ]; then
        echo "$(date '+%Y/%m/%d %H:%M:%S') agent-auth: Error updating $2 with variable $1." >> "${INSTALLDIR}/logs/ossec.log"
    fi

}

delete_blank_lines() {

    file=$1
    if [ "${use_unix_sed}" = "False" ] ; then
        ${sed} '/^$/d' "${file}"
    else
        unix_sed '/^$/d' "${file}"
    fi

}

delete_auto_enrollment_tag() {

    # Delete the configuration tag if its value is empty
    # This will allow using the default value
    if [ "${use_unix_sed}" = "False" ] ; then
        ${sed} "s#.*<$1>.*</$1>.*##g" "${TMP_ENROLLMENT}"
    else
        unix_sed "s#.*<$1>.*</$1>.*##g" "${TMP_ENROLLMENT}"
    fi

    cat -s "${TMP_ENROLLMENT}" > "${TMP_ENROLLMENT}.tmp"
    mv "${TMP_ENROLLMENT}.tmp" "${TMP_ENROLLMENT}"

}

# Change address block of the ossec.conf
add_adress_block() {

    # Remove the server configuration
    if [ "${use_unix_sed}" = "False" ] ; then
        ${sed} "/<server>/,/\/server>/d" "${CONF_FILE}"
    else
        unix_sed "/<server>/,/\/server>/d" "${CONF_FILE}"
    fi

    # Write the client configuration block
    for i in "${!ADDRESSES[@]}";
    do
        {
            echo "    <server>"
            echo "      <address>${ADDRESSES[i]}</address>"
            echo "      <port>1514</port>"
            if [ -n "${PROTOCOLS[i]}" ]; then
                echo "      <protocol>${PROTOCOLS[i]}</protocol>"
            else
                echo "      <protocol>tcp</protocol>"
            fi 
            echo "    </server>"
        } >> "${TMP_SERVER}"
    done

    if [ "${use_unix_sed}" = "False" ] ; then
        ${sed} "/<client>/r ${TMP_SERVER}" "${CONF_FILE}"
    else
        unix_sed "/<client>/r ${TMP_SERVER}" "${CONF_FILE}"
    fi

    rm -f "${TMP_SERVER}"

}

add_parameter () {

    if [ -n "$3" ]; then
        OPTIONS="$1 $2 $3"
    fi
    echo "${OPTIONS}"

}

get_deprecated_vars () {

    if [ -n "${GUARDBEAR_MANAGER_IP}" ] && [ -z "${GUARDBEAR_MANAGER}" ]; then
        GUARDBEAR_MANAGER=${GUARDBEAR_MANAGER_IP}
    fi
    if [ -n "${GUARDBEAR_AUTHD_SERVER}" ] && [ -z "${GUARDBEAR_REGISTRATION_SERVER}" ]; then
        GUARDBEAR_REGISTRATION_SERVER=${GUARDBEAR_AUTHD_SERVER}
    fi
    if [ -n "${GUARDBEAR_AUTHD_PORT}" ] && [ -z "${GUARDBEAR_REGISTRATION_PORT}" ]; then
        GUARDBEAR_REGISTRATION_PORT=${GUARDBEAR_AUTHD_PORT}
    fi
    if [ -n "${GUARDBEAR_PASSWORD}" ] && [ -z "${GUARDBEAR_REGISTRATION_PASSWORD}" ]; then
        GUARDBEAR_REGISTRATION_PASSWORD=${GUARDBEAR_PASSWORD}
    fi
    if [ -n "${GUARDBEAR_NOTIFY_TIME}" ] && [ -z "${GUARDBEAR_KEEP_ALIVE_INTERVAL}" ]; then
        GUARDBEAR_KEEP_ALIVE_INTERVAL=${GUARDBEAR_NOTIFY_TIME}
    fi
    if [ -n "${GUARDBEAR_CERTIFICATE}" ] && [ -z "${GUARDBEAR_REGISTRATION_CA}" ]; then
        GUARDBEAR_REGISTRATION_CA=${GUARDBEAR_CERTIFICATE}
    fi
    if [ -n "${GUARDBEAR_PEM}" ] && [ -z "${GUARDBEAR_REGISTRATION_CERTIFICATE}" ]; then
        GUARDBEAR_REGISTRATION_CERTIFICATE=${GUARDBEAR_PEM}
    fi
    if [ -n "${GUARDBEAR_KEY}" ] && [ -z "${GUARDBEAR_REGISTRATION_KEY}" ]; then
        GUARDBEAR_REGISTRATION_KEY=${GUARDBEAR_KEY}
    fi
    if [ -n "${GUARDBEAR_GROUP}" ] && [ -z "${GUARDBEAR_AGENT_GROUP}" ]; then
        GUARDBEAR_AGENT_GROUP=${GUARDBEAR_GROUP}
    fi

}

set_vars () {

    export GUARDBEAR_MANAGER
    export GUARDBEAR_MANAGER_PORT
    export GUARDBEAR_PROTOCOL
    export GUARDBEAR_REGISTRATION_SERVER
    export GUARDBEAR_REGISTRATION_PORT
    export GUARDBEAR_REGISTRATION_PASSWORD
    export GUARDBEAR_KEEP_ALIVE_INTERVAL
    export GUARDBEAR_TIME_RECONNECT
    export GUARDBEAR_REGISTRATION_CA
    export GUARDBEAR_REGISTRATION_CERTIFICATE
    export GUARDBEAR_REGISTRATION_KEY
    export GUARDBEAR_AGENT_NAME
    export GUARDBEAR_AGENT_GROUP
    export ENROLLMENT_DELAY
    # The following variables are yet supported but all of them are deprecated
    export GUARDBEAR_MANAGER_IP
    export GUARDBEAR_NOTIFY_TIME
    export GUARDBEAR_AUTHD_SERVER
    export GUARDBEAR_AUTHD_PORT
    export GUARDBEAR_PASSWORD
    export GUARDBEAR_GROUP
    export GUARDBEAR_CERTIFICATE
    export GUARDBEAR_KEY
    export GUARDBEAR_PEM

    if [ -r "${GUARDBEAR_MACOS_AGENT_DEPLOYMENT_VARS}" ]; then
        . ${GUARDBEAR_MACOS_AGENT_DEPLOYMENT_VARS}
        rm -rf "${GUARDBEAR_MACOS_AGENT_DEPLOYMENT_VARS}"
    fi

}

unset_vars() {

    vars=(GUARDBEAR_MANAGER_IP GUARDBEAR_PROTOCOL GUARDBEAR_MANAGER_PORT GUARDBEAR_NOTIFY_TIME \
          GUARDBEAR_TIME_RECONNECT GUARDBEAR_AUTHD_SERVER GUARDBEAR_AUTHD_PORT GUARDBEAR_PASSWORD \
          GUARDBEAR_AGENT_NAME GUARDBEAR_GROUP GUARDBEAR_CERTIFICATE GUARDBEAR_KEY GUARDBEAR_PEM \
          GUARDBEAR_MANAGER GUARDBEAR_REGISTRATION_SERVER GUARDBEAR_REGISTRATION_PORT \
          GUARDBEAR_REGISTRATION_PASSWORD GUARDBEAR_KEEP_ALIVE_INTERVAL GUARDBEAR_REGISTRATION_CA \
          GUARDBEAR_REGISTRATION_CERTIFICATE GUARDBEAR_REGISTRATION_KEY GUARDBEAR_AGENT_GROUP \
          ENROLLMENT_DELAY)

    for var in "${vars[@]}"; do
        unset "${var}"
    done

}

# Function to convert strings to lower version
tolower () {

    echo "$1" | tr '[:upper:]' '[:lower:]'

}


# Add auto-enrollment configuration block
add_auto_enrollment () {

    start_config="$(grep -n "<enrollment>" "${CONF_FILE}" | cut -d':' -f 1)"
    end_config="$(grep -n "</enrollment>" "${CONF_FILE}" | cut -d':' -f 1)"
    if [ -n "${start_config}" ] && [ -n "${end_config}" ]; then
        start_config=$(( start_config + 1 ))
        end_config=$(( end_config - 1 ))
        sed -n "${start_config},${end_config}p" "${INSTALLDIR}/etc/ossec.conf" >> "${TMP_ENROLLMENT}"
    else
        # Write the client configuration block
        {
            echo "    <enrollment>"
            echo "      <enabled>yes</enabled>"
            echo "      <manager_address>MANAGER_IP</manager_address>"
            echo "      <port>1515</port>"
            echo "      <agent_name>agent</agent_name>"
            echo "      <groups>Group1</groups>"
            echo "      <server_ca_path>/path/to/server_ca</server_ca_path>"
            echo "      <agent_certificate_path>/path/to/agent.cert</agent_certificate_path>"
            echo "      <agent_key_path>/path/to/agent.key</agent_key_path>"
            echo "      <authorization_pass_path>/path/to/authd.pass</authorization_pass_path>"
            echo "      <delay_after_enrollment>20</delay_after_enrollment>"
            echo "    </enrollment>" 
        } >> "${TMP_ENROLLMENT}"
    fi

}

# Add the auto_enrollment block to the configuration file
concat_conf() {

    if [ "${use_unix_sed}" = "False" ] ; then
        ${sed} "/<\/crypto_method>/r ${TMP_ENROLLMENT}" "${CONF_FILE}"
    else
        unix_sed "/<\/crypto_method>/r ${TMP_ENROLLMENT}/" "${CONF_FILE}"
    fi

    rm -f "${TMP_ENROLLMENT}"

}

# Set autoenrollment configuration
set_auto_enrollment_tag_value () {

    tag="$1"
    value="$2"

    if [ -n "${value}" ]; then
        edit_value_tag "${tag}" "${value}" "auto_enrollment"
    else
        delete_auto_enrollment_tag "${tag}" "auto_enrollment"
    fi

}

# Main function the script begin here
main () {

    uname_s=$(uname -s)

    # Check what kind of system we are working with
    if [ "${uname_s}" = "Darwin" ]; then
        sed="sed -ire"
        set_vars
    elif [ "${uname_s}" = "AIX" ] || [ "${uname_s}" = "SunOS" ] || [ "${uname_s}" = "HP-UX" ]; then
        use_unix_sed="True"
    fi

    get_deprecated_vars

    if [ -z "${GUARDBEAR_MANAGER}" ] && [ -n "${GUARDBEAR_PROTOCOL}" ]; then
        PROTOCOLS=( $(tolower "${GUARDBEAR_PROTOCOL//,/ }") )
        edit_value_tag "protocol" "${PROTOCOLS[0]}"
    fi

    if [ -n "${GUARDBEAR_MANAGER}" ]; then
        if [ ! -f "${INSTALLDIR}/logs/ossec.log" ]; then
            touch -f "${INSTALLDIR}/logs/ossec.log"
            chmod 660 "${INSTALLDIR}/logs/ossec.log"
            chown root:guardbear "${INSTALLDIR}/logs/ossec.log"
        fi

        # Check if multiples IPs are defined in variable GUARDBEAR_MANAGER
        ADDRESSES=( ${GUARDBEAR_MANAGER//,/ } ) 
        PROTOCOLS=( $(tolower "${GUARDBEAR_PROTOCOL//,/ }") )
        # Get uniques values if all protocols are the same
        if ( [ "${#PROTOCOLS[@]}" -ge "${#ADDRESSES[@]}" ] && ( ( ! echo "${PROTOCOLS[@]}" | grep -q -w "tcp" ) || ( ! echo "${PROTOCOLS[@]}" | grep -q -w "udp" ) ) ) || [ ${#PROTOCOLS[@]} -eq 0 ] || ( ! echo "${PROTOCOLS[@]}" | grep -q -w "udp" ) ; then
            ADDRESSES=( $(echo "${ADDRESSES[@]}" |  tr ' ' '\n' | cat -n | sort -uk2 | sort -n | cut -f2- | tr '\n' ' ') ) 
        fi
        
        add_adress_block
    fi

    edit_value_tag "port" "${GUARDBEAR_MANAGER_PORT}"

    if [ -n "${GUARDBEAR_REGISTRATION_SERVER}" ] || [ -n "${GUARDBEAR_REGISTRATION_PORT}" ] || [ -n "${GUARDBEAR_REGISTRATION_CA}" ] || [ -n "${GUARDBEAR_REGISTRATION_CERTIFICATE}" ] || [ -n "${GUARDBEAR_REGISTRATION_KEY}" ] || [ -n "${GUARDBEAR_AGENT_NAME}" ] || [ -n "${GUARDBEAR_AGENT_GROUP}" ] || [ -n "${ENROLLMENT_DELAY}" ] || [ -n "${GUARDBEAR_REGISTRATION_PASSWORD}" ]; then
        add_auto_enrollment
        set_auto_enrollment_tag_value "manager_address" "${GUARDBEAR_REGISTRATION_SERVER}"
        set_auto_enrollment_tag_value "port" "${GUARDBEAR_REGISTRATION_PORT}"
        set_auto_enrollment_tag_value "server_ca_path" "${GUARDBEAR_REGISTRATION_CA}"
        set_auto_enrollment_tag_value "agent_certificate_path" "${GUARDBEAR_REGISTRATION_CERTIFICATE}"
        set_auto_enrollment_tag_value "agent_key_path" "${GUARDBEAR_REGISTRATION_KEY}"
        set_auto_enrollment_tag_value "authorization_pass_path" "${GUARDBEAR_REGISTRATION_PASSWORD_PATH}"
        set_auto_enrollment_tag_value "agent_name" "${GUARDBEAR_AGENT_NAME}"
        set_auto_enrollment_tag_value "groups" "${GUARDBEAR_AGENT_GROUP}"
        set_auto_enrollment_tag_value "delay_after_enrollment" "${ENROLLMENT_DELAY}"
        delete_blank_lines "${TMP_ENROLLMENT}"
        concat_conf
    fi

            
    if [ -n "${GUARDBEAR_REGISTRATION_PASSWORD}" ]; then
        echo "${GUARDBEAR_REGISTRATION_PASSWORD}" > "${INSTALLDIR}/${GUARDBEAR_REGISTRATION_PASSWORD_PATH}"
        chmod 640 "${INSTALLDIR}"/"${GUARDBEAR_REGISTRATION_PASSWORD_PATH}"
        chown root:guardbear "${INSTALLDIR}"/"${GUARDBEAR_REGISTRATION_PASSWORD_PATH}"
    fi

    # Options to be modified in ossec.conf
    edit_value_tag "notify_time" "${GUARDBEAR_KEEP_ALIVE_INTERVAL}"
    edit_value_tag "time-reconnect" "${GUARDBEAR_TIME_RECONNECT}"

    unset_vars

}

# Start script execution
main "$@"
