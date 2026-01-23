from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import pytest
import importlib

IMPORT_DLPAR = "ansible_collections.ibm.power_hmc.plugins.modules.powervm_partition_profile"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}

processor_settings = {'maximum_processors': '1',
                      'processor_mode': 'dedicated',
                      'minimum_processors': '1',
                      'desired_processors': '1'}

processor_settings1 = {'maximum_processors': '1',
                       'minimum_processors': '1',
                       'desired_processors': '1'}

memory_settings = {'minimum_memory': 1,
                   'maximum_memory': 1,
                   'desired_memory': 1,
                   'desired_huge_pagecount': 2,
                   'maximum_huge_pagecount': 2,
                   'minimum_huge_pagecount': 2}

memory_settings1 = {'minimum_memory': 1,
                    'maximum_memory': 1,
                    'desired_huge_pagecount': 2,
                    'maximum_huge_pagecount': 2,
                    'minimum_huge_pagecount': 2}

test_data = [
    # All present related Testdata
    # when hmc_host key is missing
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': 'present', 'system_name': 'system_name',
      'vm_name': 'vm_name', 'name': 'prof_name', 'memory_settings': memory_settings,
      'processor_settings': processor_settings},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),

    # when system name is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'present', 'system_name': None,
      'vm_name': 'vm_name', 'name': 'prof_name', 'memory_settings': memory_settings,
      'processor_settings': processor_settings},
     "ParameterError: mandatory parameter 'system_name' is missing"),

    # when vm_name is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'present', 'system_name': 'system_name',
      'vm_name': None, 'name': 'prof_name', 'memory_settings': memory_settings,
      'processor_settings': processor_settings},
     "ParameterError: mandatory parameter 'vm_name' is missing"),

    # when name is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'present', 'system_name': 'system_name',
      'vm_name': 'vm_name', 'name': None, 'memory_settings': memory_settings,
      'processor_settings': processor_settings},
     "ParameterError: mandatory parameter 'name' is missing"),

    # when memory_settings is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'present', 'system_name': 'system_name',
      'vm_name': 'vm_name', 'name': None, 'memory_settings': None,
      'processor_settings': processor_settings},
     "ParameterError: memory_settings is required for state=present"),

    # when processor_settings is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'present', 'system_name': 'system_name',
      'vm_name': 'vm_name', 'name': None, 'memory_settings': memory_settings,
      'processor_settings': None},
     "ParameterError: processor_settings is required for state=present"),

    # when processor_mode is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'present', 'system_name': 'system_name',
      'vm_name': 'vm_name', 'name': None, 'memory_settings': memory_settings,
      'processor_settings': processor_settings1},
     "ParameterError: processor_mode is required in processor_settings"),

    # when processor_settings is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'present', 'system_name': 'system_name',
      'vm_name': 'vm_name', 'name': None, 'memory_settings': memory_settings1,
      'processor_settings': processor_settings},
     "ParameterError: Missing required memory_settings fields: desired_memory"),
]

test_data1 = [
    # All copy related Testdata
    # when hmc_host key is missing
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': 'copy', 'system_name': 'system_name',
      'vm_name': 'vm_name', 'name': 'prof_name', 'duplicate_prof_name': 'test'},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),

    # when system_name is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'copy', 'system_name': None,
      'vm_name': 'vm_name', 'name': 'prof_name', 'duplicate_prof_name': 'test'},
     "ParameterError: mandatory parameter 'system_name' is missing"),

    # when vm_name is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'copy', 'system_name': 'system_name',
      'vm_name': None, 'name': 'prof_name', 'duplicate_prof_name': 'test'},
     "ParameterError: mandatory parameter 'vm_name' is missing"),

    # when name is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'copy', 'system_name': 'system_name',
      'vm_name': 'vm_name', 'name': None, 'duplicate_prof_name': 'test'},
     "ParameterError: mandatory parameter 'name' is missing"),

    # when duplicate_prof_name is missing
    ({'hmc_host': 'host', 'hmc_auth': hmc_auth, 'state': 'copy', 'system_name': 'system_name',
      'vm_name': 'vm_name', 'name': 'prof_name', 'duplicate_prof_name': None},
     "ParameterError: mandatory parameter 'duplicate_prof_name' is missing"),
]


def common_mock_setup(mocker):
    powervm_partition_profile = importlib.import_module(IMPORT_DLPAR)
    mocker.patch.object(powervm_partition_profile, 'HmcRestClient')
    return powervm_partition_profile


@pytest.mark.parametrize("user_test_input1, expectedError", test_data)
def test_call_present(mocker, user_test_input1, expectedError):
    powervm_partition_profile = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            powervm_partition_profile.create_partition_profile(powervm_partition_profile, user_test_input1)
        assert expectedError == repr(e.value)
    else:
        powervm_partition_profile.create_partition_profile(powervm_partition_profile, user_test_input1)


@pytest.mark.parametrize("user_test_input2, expectedError", test_data1)
def test_call_copy(mocker, user_test_input2, expectedError):
    powervm_partition_profile = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            powervm_partition_profile.copy_partition_profile(powervm_partition_profile, user_test_input2)
        assert expectedError == repr(e.value)
    else:
        powervm_partition_profile.copy_partition_profile(powervm_partition_profile, user_test_input2)
