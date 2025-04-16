from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_VIOS_UPDATE_UPGRADE = "ansible_collections.ibm.power_hmc.plugins.modules.vios_update_upgrade"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}
test_data = [

    # All sftp update related testcases
    # host name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': None,
      'image_name': 'data', 'host_name': None, 'user_id': 'data',
      'password': 'data', 'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': 'data'}},
     "ParameterError: mandatory parameter 'host_name' is missing"),

    # system name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': None, 'vios_id': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data',
      'password': 'data', 'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': 'data'}},
     "ParameterError: mandatory parameter 'system_name' is missing"),

    # providing both vios_name and vios_id
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data',
      'password': 'data', 'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': 'data'}},
     "ParameterError: Parameters 'vios_id' and 'vios_name' are mutually exclusive"),

    # both vios_name and vios_id are missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data',
      'password': 'data', 'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': None}},
     "ParameterError: Missing VIOS details"),

    # user_id is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': None,
      'password': 'data', 'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': None}},
     "ParameterError: mandatory parameter 'user_id' is missing"),

    # password and ssh_key_file are missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data',
      'password': None, 'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': None}},
     "ParameterError: Either 'ssh_key_file' or 'password' is mandatory"),

    # both password and ssh_key_file are provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data',
      'password': 'data', 'ssh_key_file': 'data', 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': None}},
     "ParameterError: Parameters 'ssh_key_file' and 'password' are mutually exclusive"),

    # mount_loc is provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data',
      'password': 'data', 'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': None}},
     "ParameterError: unsupported parameter: mount_loc"),

    # providing both vios_name and vios_id
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data',
      'password': 'data', 'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': 'data'}},
     "ParameterError: Parameters 'vios_id' and 'vios_name' are mutually exclusive"),

    # both vios_name and vios_id are missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': 'data',
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': None}},
     "ParameterError: Missing VIOS details"),

    # disks is provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': 'data',
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'vios_name': None}},
     "ParameterError: unsupported parameter: disks"),

    # All nfs update related testcases
    # host name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': None,
      'image_name': 'data', 'host_name': None, 'user_id': None, 'password': None,
      'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': 'data'}},
     "ParameterError: mandatory parameter 'host_name' is missing"),

    # system name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'nfs', 'system_name': None, 'vios_id': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': None, 'password': None,
      'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': 'data'}},
     "ParameterError: mandatory parameter 'system_name' is missing"),

    # both password and ssh_key_file are provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': None, 'password': 'data',
      'ssh_key_file': 'data', 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': None}},
     "ParameterError: unsupported parameters: password,ssh_key_file"),

    # password is provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': None,
      'password': 'data', 'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': None}},
     "ParameterError: unsupported parameter: password"),

    # providing both vios_name and vios_id
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data',
      'password': 'data', 'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': 'data'}},
     "ParameterError: Parameters 'vios_id' and 'vios_name' are mutually exclusive"),

    # both vios_name and vios_id are missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': None,
      'password': None, 'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'vios_name': None}},
     "ParameterError: Missing VIOS details"),

    # disks is provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'updated', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': None, 'password': None,
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'vios_name': None}},
     "ParameterError: unsupported parameter: disks")]

test_data1 = [

    # All upgrade related testcases
    # host name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': None, 'vios_name': 'data',
      'image_name': 'data', 'host_name': None, 'user_id': 'data', 'password': 'data',
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'files': 'data'}},
     "ParameterError: mandatory parameter 'host_name' is missing"),

    # system name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'sftp', 'system_name': None, 'vios_id': None, 'vios_name': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': 'data',
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'files': 'data'}},
     "ParameterError: mandatory parameter 'system_name' is missing"),

    # providing both vios_name and vios_id
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data', 'vios_name': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': 'data',
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'files': 'data'}},
     "ParameterError: Parameters 'vios_id' and 'vios_name' are mutually exclusive"),

    # both vios_name and vios_id are missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': None, 'vios_name': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': 'data',
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'files': 'data'}},
     "ParameterError: Missing VIOS details"),

    # user_id is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data', 'vios_name': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': None, 'password': 'data',
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'files': 'data'}},
     "ParameterError: mandatory parameter 'user_id' is missing"),

    # password and ssh_key_file are missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data', 'vios_name': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': None,
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'files': None}},
     "ParameterError: Either 'ssh_key_file' or 'password' is mandatory"),

    # both password and ssh_key_file are provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data', 'vios_name': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': 'data',
      'ssh_key_file': 'data', 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'files': None}},
     "ParameterError: Parameters 'ssh_key_file' and 'password' are mutually exclusive"),

    # files is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data', 'vios_name': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': 'data',
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'files': None}},
     "ParameterError: mandatory parameter 'files' is missing"),

    # disks is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'sftp', 'system_name': 'data', 'vios_id': 'data', 'vios_name': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': 'data',
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'files': 'data'}},
     "ParameterError: mandatory parameter 'disks' is missing"),

    # All nfs upgrade related testcases
    # host name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': None, 'vios_name': 'data',
      'image_name': 'data', 'host_name': None, 'user_id': None, 'password': None,
      'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'files': 'data'}},
     "ParameterError: mandatory parameter 'host_name' is missing"),

    # system name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'nfs', 'system_name': None, 'vios_id': None, 'vios_name': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': None, 'password': None,
      'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'files': 'data'}},
     "ParameterError: mandatory parameter 'system_name' is missing"),

    # both password and ssh_key_file are provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': 'data', 'vios_name': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': None, 'password': 'data',
      'ssh_key_file': 'data', 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'files': 'data'}},
     "ParameterError: unsupported parameters: password,ssh_key_file"),

    # password is provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': 'data', 'vios_name': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': None, 'password': 'data',
      'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'files': 'data'}},
     "ParameterError: unsupported parameter: password"),

    # providing both vios_name and vios_id
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': 'data', 'vios_name': 'data',
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': 'data',
      'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'files': 'data'}},
     "ParameterError: Parameters 'vios_id' and 'vios_name' are mutually exclusive"),

    # both vios_name and vios_id are missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': None, 'vios_name': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': 'data', 'password': 'data',
      'ssh_key_file': None, 'mount_loc': 'data', 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': None, 'files': 'data'}},
     "ParameterError: Missing VIOS details"),

    # mount_loc is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'upgraded', 'attributes':
     {'repository': 'nfs', 'system_name': 'data', 'vios_id': 'data', 'vios_name': None,
      'image_name': 'data', 'host_name': 'data', 'user_id': None, 'password': None,
      'ssh_key_file': None, 'mount_loc': None, 'directory': None,
      'option': None, 'save': None, 'restart': None, 'disks': 'data', 'files': 'data'}},
     "ParameterError: mandatory parameter 'mount_loc' is missing")]


def common_mock_setup(mocker):
    vios_update_upgrade = importlib.import_module(IMPORT_VIOS_UPDATE_UPGRADE)
    mocker.patch.object(vios_update_upgrade, 'HmcCliConnection')
    mocker.patch.object(vios_update_upgrade, 'Hmc', autospec=True)
    return vios_update_upgrade


@pytest.mark.parametrize("update_teset_input, expectedError", test_data)
def test_update_vios(mocker, update_teset_input, expectedError):
    vios_update_upgrade = common_mock_setup(mocker)
    vios_update_upgrade.Hmc.checkIfHMCFullyBootedUp.return_value = (True, {})
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            vios_update_upgrade.ensure_update_upgrade(vios_update_upgrade, update_teset_input)
        assert expectedError == repr(e.value)
    else:
        vios_update_upgrade.ensure_update_upgrade(vios_update_upgrade, update_teset_input)


@pytest.mark.parametrize("update_teset_input, expectedError", test_data1)
def test_upgrade_vios(mocker, update_teset_input, expectedError):
    vios_update_upgrade = common_mock_setup(mocker)
    vios_update_upgrade.Hmc.checkIfHMCFullyBootedUp.return_value = (True, {})
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            vios_update_upgrade.ensure_update_upgrade(vios_update_upgrade, update_teset_input)
        assert expectedError == repr(e.value)
    else:
        vios_update_upgrade.ensure_update_upgrade(vios_update_upgrade, update_teset_input)
