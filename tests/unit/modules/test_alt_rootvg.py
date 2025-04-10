from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_HMC_VIOS_MAINTENANCE = "ansible_collections.ibm.power_hmc.plugins.modules.vios_alt_root_vg"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}
test_data = [

    # All copy alt_rootvg related testdata
    # Not providing hmc host
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': 'copy', 'system_name': 'sys', 'vios_name': 'vios', 'targets': 'targets', 'disk_size_policy': None},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),

    # vios details missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'copy', 'system_name': 'sys', 'vios_name': None, 'targets': 'targets', 'disk_size_policy': None},
     "ParameterError: mandatory parameter 'vios_name' is missing"),

    # System details missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'copy', 'system_name': None, 'vios_name': 'vios', 'targets': 'disk', 'disk_size_policy': None},
     "ParameterError: mandatory parameter 'system_name' is missing"),

    # Both targets and disk size policy is not provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'copy', 'system_name': 'sys', 'vios_name': 'vios', 'targets': None, 'disk_size_policy': None},
     "ParameterError: Either disk_size_policy or targets should be propvided."),

    # Both targets and disk size policy are provided
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'copy', 'system_name': 'sys', 'vios_name': 'vios', 'targets': 'disk', 'disk_size_policy': 'min'},
     "ParameterError: disk_size_policy and targets are mutually exclusive.")]

test_data1 = [

    # All clean alt_rootvg related testdata
    # Not providing hmc host
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': 'clean', 'system_name': 'sys', 'vios_name': 'vios', 'targets': 'targets', 'disk_size_policy': None,
      'force': None}, "ParameterError: mandatory parameter 'hmc_host' is missing"),

    # vios details missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'clean', 'system_name': 'sys', 'vios_name': None, 'targets': 'targets', 'disk_size_policy': None,
      'force': None}, "ParameterError: mandatory parameter 'vios_name' is missing"),

    # System details missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'clean', 'system_name': None, 'vios_name': 'vios', 'targets': 'disk', 'disk_size_policy': None,
      'force': None}, "ParameterError: mandatory parameter 'system_name' is missing"),

    # Providing disk_size_policy parameter
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'clean', 'system_name': 'sys', 'vios_name': 'vios', 'targets': None, 'force': None,
     'disk_size_policy': 'min'}, "ParameterError: unsupported parameter: disk_size_policy")]


def common_mock_setup(mocker):
    hmc_alt_rootvg = importlib.import_module(IMPORT_HMC_VIOS_MAINTENANCE)
    mocker.patch.object(hmc_alt_rootvg, 'HmcCliConnection')
    mocker.patch.object(hmc_alt_rootvg, 'Hmc', autospec=True)
    return hmc_alt_rootvg


@pytest.mark.parametrize("alt_rootvg_test_input, expectedError", test_data)
def test_call_alt_rootvg(mocker, alt_rootvg_test_input, expectedError):
    hmc_alt_rootvg = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_alt_rootvg.alt_disk_copy(hmc_alt_rootvg, alt_rootvg_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_alt_rootvg.alt_disk_copy(hmc_alt_rootvg, alt_rootvg_test_input)


@pytest.mark.parametrize("alt_rootvg_test_input, expectedError", test_data1)
def test_call_alt_rootvg(mocker, alt_rootvg_test_input, expectedError):
    hmc_alt_rootvg = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_alt_rootvg.alt_disk_clean(hmc_alt_rootvg, alt_rootvg_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_alt_rootvg.alt_disk_copy(hmc_alt_rootvg, alt_rootvg_test_input)
