from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_HMC_VIOS_MAINTENANCE = "ansible_collections.ibm.power_hmc.plugins.modules.vios_maintenance"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}
test_data = [

    # All create backup file related testdata
    # vios details is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'viosioconfig', 'system': 'sys',
                                                                                      'vios_name': None, 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': 'data',
                                                                                      'nimol_resource': None, 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: Missing VIOS details"),
    # type is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': None, 'system': 'sys',
                                                                                      'vios_name': 'data', 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': 'data',
      'nimol_resource': None, 'volume_group_structure': None, 'media_repository': None, 'restart': None}},
     "ParameterError: mandatory parameter 'types' is missing"),
    # nimol_resource is not none
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'viosioconfig', 'system': 'sys',
                                                                                      'vios_name': 'data', 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': 'data',
                                                                                      'nimol_resource': 'data', 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: Parameters 'nimol_resource', 'media_repository' and 'volume_group_structure' are valid for only full VIOS backup"),
    # backup_name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'vios', 'system': 'sys',
                                                                                      'vios_name': 'data', 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': None,
                                                                                      'nimol_resource': None, 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: mandatory parameter 'backup_name' is missing"),
    # system is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'vios', 'system': None, 'vios_name': 'data',
                                                                                      'vios_id': None, 'vios_uuid': None, 'backup_name': 'data',
                                                                                      'nimol_resource': None, 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: mandatory parameter 'system' is missing")]

test_data1 = [

    # All remove backup file related testdata
    # vios details is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'viosioconfig', 'system': 'sys',
                                                                                      'vios_name': None, 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': 'data',
                                                                                      'nimol_resource': None, 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: Missing VIOS details"),
    # type is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': None, 'system': 'sys',
                                                                                      'vios_name': 'data', 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': 'data',
      'nimol_resource': None, 'volume_group_structure': None, 'media_repository': None, 'restart': None}},
     "ParameterError: mandatory parameter 'types' is missing"),
    # nimol_resource is not none
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'viosioconfig', 'system': 'sys',
                                                                                      'vios_name': 'data', 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': 'data',
                                                                                      'nimol_resource': 'data', 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: Parameters 'nimol_resource', 'media_repository' and 'volume_group_structure' are valid for only full VIOS backup"),
    # backup_name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'vios', 'system': 'sys',
                                                                                      'vios_name': 'data', 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': None,
                                                                                      'nimol_resource': None, 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: mandatory parameter 'backup_name' is missing"),
    # system is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'vios', 'system': None, 'vios_name': 'data',
                                                                                      'vios_id': None, 'vios_uuid': None, 'backup_name': 'data',
                                                                                      'nimol_resource': None, 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: mandatory parameter 'system' is missing")]

test_data2 = [

    # All Restore backup file related testdata
    # vios details is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'viosioconfig', 'system': 'sys',
                                                                                      'vios_name': None, 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': 'data',
                                                                                      'nimol_resource': None, 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: Missing VIOS details"),
    # type is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': None, 'system': 'sys',
                                                                                      'vios_name': 'data', 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': 'data',
      'nimol_resource': None, 'volume_group_structure': None, 'media_repository': None, 'restart': None}},
     "ParameterError: mandatory parameter 'types' is missing"),
    # nimol_resource is not none
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'viosioconfig', 'system': 'sys',
                                                                                      'vios_name': 'data', 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': 'data',
                                                                                      'nimol_resource': 'data', 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: Parameters 'nimol_resource', 'media_repository' and 'volume_group_structure' are valid for only full VIOS backup"),
    # backup_name is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'vios', 'system': 'sys',
                                                                                      'vios_name': 'data', 'vios_id': None,
                                                                                      'vios_uuid': None, 'backup_name': None,
                                                                                      'nimol_resource': None, 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: mandatory parameter 'backup_name' is missing"),
    # system is missed
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present', 'attributes': {'types': 'vios', 'system': None, 'vios_name': 'data',
                                                                                      'vios_id': None, 'vios_uuid': None, 'backup_name': 'data',
                                                                                      'nimol_resource': None, 'volume_group_structure': None,
                                                                                      'media_repository': None, 'restart': None}},
     "ParameterError: mandatory parameter 'system' is missing")]


def common_mock_setup(mocker):
    hmc_vios_maintenance = importlib.import_module(IMPORT_HMC_VIOS_MAINTENANCE)
    mocker.patch.object(hmc_vios_maintenance, 'HmcCliConnection')
    mocker.patch.object(hmc_vios_maintenance, 'Hmc', autospec=True)
    return hmc_vios_maintenance


@pytest.mark.parametrize("vios_backup_creation_test_input, expectedError", test_data)
def test_call_create_vios_backup(mocker, vios_backup_creation_test_input, expectedError):
    hmc_vios_maintenance = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios_maintenance.ensure_present(hmc_vios_maintenance, vios_backup_creation_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios_maintenance.ensure_present(hmc_vios_maintenance, vios_backup_creation_test_input)


@pytest.mark.parametrize("vios_backup_creation_test_input, expectedError", test_data1)
def test_call_remove_vios_backup(mocker, vios_backup_creation_test_input, expectedError):
    hmc_vios_maintenance = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios_maintenance.ensure_absent(hmc_vios_maintenance, vios_backup_creation_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios_maintenance.ensure_absent(hmc_vios_maintenance, vios_backup_creation_test_input)


@pytest.mark.parametrize("vios_backup_creation_test_input, expectedError", test_data2)
def test_call_restore_vios_backup(mocker, vios_backup_creation_test_input, expectedError):
    hmc_vios_maintenance = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios_maintenance.ensure_restore(hmc_vios_maintenance, vios_backup_creation_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios_maintenance.ensure_restore(hmc_vios_maintenance, vios_backup_creation_test_input)
