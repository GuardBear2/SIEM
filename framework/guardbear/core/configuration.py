# Copyright (C) 2015, GuardBear Inc.
# Created by GuardBear, Inc. <info@guardbear.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import json
import logging
import os
from os import path as os_path
from typing import Union

import guardbear.core.config.client
from guardbear.core import common, guardbear_socket
from guardbear.core.exception import GuardBearError, GuardBearInternalError, GuardBearResourceNotFound
from guardbear.core.InputValidator import InputValidator
from guardbear.core.utils import get_group_file_path, load_guardbear_yaml, validate_guardbear_configuration

logger = logging.getLogger('guardbear')

# Aux functions

# Type of configuration sections:
#   * Duplicate -> there can be multiple independent sections. Must be returned as multiple json entries.
#   * Merge -> there can be multiple sections but all are dependent with each other. Must be returned as a single json
#   entry.
#   * Last -> there can be multiple sections in the configuration but only the last one will be returned.
#   The rest are ignored.
GETCONFIG_COMMAND = 'getconfig'
UPDATE_CHECK_OSSEC_FIELD = 'update_check'
GLOBAL_KEY = 'global'
YES_VALUE = 'yes'
CTI_URL_FIELD = 'cti-url'
DEFAULT_CTI_URL = 'https://cti.guardbear.com'


def get_group_conf(group_id: str = None, raw: bool = False) -> Union[dict, str]:
    """Return group configuration as dictionary.

    Parameters
    ----------
    group_id : str
        ID of the group with the configuration we want to get.
    raw : bool
        Respond in raw format.

    Raises
    ------
    GuardBearResourceNotFound(1710)
        Group was not found.
    GuardBearError(1006)
        group configuration does not exist or there is a problem with the permissions.

    Returns
    -------
    dict or str
        Group configuration as dictionary.
    """
    filepath = get_group_file_path(group_id)
    if not os_path.exists(filepath):
        raise GuardBearResourceNotFound(1710, group_id)

    if raw:
        try:
            # Read RAW file
            with open(filepath, 'r') as raw_data:
                data = raw_data.read()
                return data
        except Exception as e:
            raise GuardBearError(1006, str(e))

    # Parse YAML
    data = load_guardbear_yaml(filepath)

    return {'total_affected_items': len(data), 'affected_items': data}


def update_group_configuration(group_id: str, file_content: str) -> str:
    """Update group configuration.

    Parameters
    ----------
    group_id : str
        Group to update.
    file_content : str
        File content of the new configuration in a string.

    Raises
    ------
    GuardBearResourceNotFound(1710)
        Group was not found.
    GuardBearInternalError(1006)
        Error writing file.

    Returns
    -------
    str
        Confirmation message.
    """
    filepath = get_group_file_path(group_id)

    if not os_path.exists(filepath):
        raise GuardBearResourceNotFound(1710, group_id)

    validate_guardbear_configuration(file_content)

    try:
        with open(filepath, 'w') as f:
            f.write(file_content)
    except Exception as e:
        raise GuardBearError(1006, extra_message=str(e))

    return 'Agent configuration was successfully updated'


def update_group_file(group_id: str, file_data: str) -> str:
    """Update a group file.

    Parameters
    ----------
    group_id : str
        Group to update.
    file_data : str
        Upload data.

    Raises
    ------
    GuardBearError(1722)
        If there was a validation error.
    GuardBearResourceNotFound(1710)
        Group was not found.
    GuardBearError(1112)
        Empty files are not supported.

    Returns
    -------
    str
        Confirmation message in string.
    """
    if not InputValidator().group(group_id):
        raise GuardBearError(1722)

    if not os_path.exists(get_group_file_path(group_id)):
        raise GuardBearResourceNotFound(1710, group_id)

    if len(file_data) == 0:
        raise GuardBearError(1112)

    return update_group_configuration(group_id, file_data)


def get_active_configuration(component: str, configuration: str, agent_id: str = None) -> dict:
    """Get an agent's component active configuration.

    Parameters
    ----------
    agent_id : str
        Agent ID. All possible values from 001 onwards.
    component : str
        Selected agent's component.
    configuration : str
        Configuration to get, written on disk.

    Raises
    ------
    GuardBearError(1307)
        If the component or configuration are not specified.
    GuardBearError(1101)
        If the specified component is not valid.
    GuardBearError(1121)
        If the component is not properly configured.
    GuardBearInternalError(1121)
        If the socket cant be created.
    GuardBearInternalError(1118)
        If the socket is not able to receive a response.
    GuardBearError(1117)
        If there's no such file or directory in agent node, or the socket cannot send the request.
    GuardBearError(1116)
        If the reply from the node contains an error.

    Returns
    -------
    dict
        The active configuration the agent is currently using.
    """
    sockets_json_protocol = {'remote', 'analysis', 'wdb'}
    component_socket_mapping = {
        'agent': 'analysis',
        'agentless': 'agentless',
        'analysis': 'analysis',
        'auth': 'auth',
        'com': 'com',
        'csyslog': 'csyslog',
        'integrator': 'integrator',
        'logcollector': 'logcollector',
        'mail': 'mail',
        'monitor': 'monitor',
        'request': 'remote',
        'syscheck': 'syscheck',
        'guardbear-db': 'wdb',
        'wmodules': 'wmodules',
    }
    component_socket_dir_mapping = {
        'agent': 'sockets',
        'agentless': 'sockets',
        'analysis': 'sockets',
        'auth': 'sockets',
        'com': 'sockets',
        'csyslog': 'sockets',
        'integrator': 'sockets',
        'logcollector': 'sockets',
        'mail': 'sockets',
        'monitor': 'sockets',
        'request': 'sockets',
        'syscheck': 'sockets',
        'guardbear-db': 'db',
        'wmodules': 'sockets',
    }

    if not component or not configuration:
        raise GuardBearError(1307)

    # Check if the component is correct
    components = component_socket_mapping.keys()
    if component not in components:
        raise GuardBearError(1101, f'Valid components: {", ".join(components)}')

    def get_active_configuration_manager():
        """Get manager active configuration."""
        # Communicate with the socket that corresponds to the component requested
        dest_socket = common.GUARDBEAR_QUEUE / component_socket_dir_mapping[component] / component_socket_mapping[component]

        # Verify component configuration
        if not os.path.exists(dest_socket):
            raise GuardBearError(
                1121, extra_message=f"Please verify that the component '{component}' is properly configured"
            )

        # Simple socket message
        if component_socket_mapping[component] not in sockets_json_protocol:
            msg = f'{GETCONFIG_COMMAND} {configuration}'

            # Socket connection
            try:
                s = guardbear_socket.GuardBearSocket(dest_socket)
            except GuardBearInternalError:
                raise
            except Exception as unhandled_exc:
                raise GuardBearInternalError(1121, extra_message=str(unhandled_exc))

            # Send message
            s.send(msg.encode())

            # Receive response
            try:
                # Receive data length
                rec_msg_ok, rec_msg = s.receive().decode().split(' ', 1)
            except ValueError:
                raise GuardBearInternalError(1118, extra_message='Data could not be received')
            finally:
                s.close()

            return rec_msg_ok, rec_msg

        # JSON socket message
        else:  # component_socket_mapping[component] in sockets_json_protocol
            msg = guardbear_socket.create_guardbear_socket_message(
                origin={'module': common.origin_module.get()},
                command=GETCONFIG_COMMAND,
                parameters={'section': configuration},
            )

            # Socket connection
            try:
                s = guardbear_socket.GuardBearSocketJSON(dest_socket)
            except GuardBearInternalError:
                raise
            except Exception as unhandled_exc:
                raise GuardBearInternalError(1121, extra_message=str(unhandled_exc))

            # Send message
            s.send(msg)

            # Receive response
            try:
                response = s.receive(raw=True)
            except ValueError:
                raise GuardBearInternalError(1118, extra_message='Data could not be received')
            finally:
                s.close()

            return response['error'], response['data']

    def get_active_configuration_agent():
        """Get agent active configuration."""
        # Always communicate with remote socket
        dest_socket = common.REMOTED_SOCKET

        # Simple socket message
        msg = f'{str(agent_id).zfill(3)} {component} {GETCONFIG_COMMAND} {configuration}'

        # Socket connection
        try:
            s = guardbear_socket.GuardBearSocket(dest_socket)
        except GuardBearInternalError:
            raise
        except Exception as unhandled_exc:
            raise GuardBearInternalError(1121, extra_message=str(unhandled_exc))

        # Send message
        s.send(msg.encode())

        # Receive response
        try:
            # Receive data length
            rec_msg_ok, rec_msg = s.receive().decode().split(' ', 1)
        except ValueError:
            raise GuardBearInternalError(1118, extra_message='Data could not be received')
        finally:
            s.close()

        return rec_msg_ok, rec_msg

    rec_error, rec_data = get_active_configuration_agent() if agent_id else get_active_configuration_manager()

    if rec_error == 'ok' or rec_error == 0:
        data = json.loads(rec_data) if isinstance(rec_data, str) else rec_data

        # Include password if auth->use_password enabled and authd.pass file exists
        if data.get('auth', {}).get('use_password') == 'yes':
            try:
                with open(os_path.join(common.GUARDBEAR_PATH, 'etc', 'authd.pass'), 'r') as f:
                    data['authd.pass'] = f.read().rstrip()
            except IOError:
                pass

        return data
    else:
        raise GuardBearError(
            1117 if 'No such file or directory' in rec_data or 'Cannot send request' in rec_data else 1116,
            extra_message=f'{component}:{configuration}',
        )


def update_check_is_enabled() -> bool:
    """Read the ossec.conf and check UPDATE_CHECK_OSSEC_FIELD value.

    Returns
    -------
    bool
        True if UPDATE_CHECK_OSSEC_FIELD is 'yes' or isn't present, else False.
    """
    try:
        config_value = guardbear.core.config.client.CentralizedConfig.get_server_config().cti.update_check
        return config_value
    except GuardBearError as e:
        if e.code != 1106:
            raise e
        return True


def get_cti_url() -> str:
    """Get the CTI service URL from the configuration.

    Returns
    -------
    str
        CTI service URL. The default value is returned if CTI_URL_FIELD isn't present.
    """
    try:
        return guardbear.core.config.client.CentralizedConfig.get_server_config().cti.url
    except GuardBearError as e:
        if e.code != 1106:
            raise e
        return DEFAULT_CTI_URL
