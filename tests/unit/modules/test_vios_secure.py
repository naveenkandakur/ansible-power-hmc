from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_HMC_VIOS_MAINTENANCE = "ansible_collections.ibm.power_hmc.plugins.modules.vios_secure"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}
setting_security_test_data = [

    # All setting_security related testdata
    # Not providing hmc host
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': 'setting_security', 'system_name': 'sys',
      'vios_name': 'vios', 'level': 'test', 'rule': None, 'file': None, 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),

    # Unsupported parameter firewall_config
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'setting_security', 'system_name': 'sys',
      'vios_name': 'vios', 'level': 'test', 'rule': None, 'file': None, 'firewall_config': 'test',
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: unsupported parameter: firewall_config"),

    # Providing both level and file parameter
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'setting_security', 'system_name': 'sys',
      'vios_name': 'vios', 'level': 'test', 'rule': None, 'file': 'test', 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: level and file parameter are mutually exclusive."),

    # Not providing both level and file parameter
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'setting_security', 'system_name': 'sys',
      'vios_name': 'vios', 'level': None, 'rule': None, 'file': None, 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: Either level or file parameter should be propvided."),

    # Providing both level and file parameter
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'setting_security', 'system_name': 'sys',
      'vios_name': 'vios', 'level': None, 'rule': None, 'file': None, 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: Either level or file parameter should be propvided."),

    # Not providing vios_name parameter
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'setting_security', 'system_name': 'sys',
      'vios_name': None, 'level': 'test', 'rule': 'test', 'file': None, 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: mandatory parameter 'vios_name' is missing"),

    # Not providing system_name parameter
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'setting_security', 'system_name': None,
      'vios_name': 'vios', 'level': 'test', 'rule': 'test', 'file': None, 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: mandatory parameter 'system_name' is missing")]

firewall_facts_test_data = [

    # All firewall_facts related testdata
    # Not providing hmc host
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': 'firewall_facts', 'system_name': 'sys',
      'vios_name': 'vios', 'level': 'test', 'rule': None, 'file': None, 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),

    # Providing firewall_config parameter
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'firewall_facts', 'system_name': 'sys',
      'vios_name': 'vios', 'level': None, 'rule': None, 'file': None, 'firewall_config': 'test',
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: unsupported parameter: firewall_config"),

    # Providing level parameter
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'firewall_facts', 'system_name': 'sys',
      'vios_name': 'vios', 'level': 'test', 'rule': None, 'file': None, 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: unsupported parameter: level"),

    # Providing rule parameter
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'firewall_facts', 'system_name': 'sys',
      'vios_name': 'vios', 'level': None, 'rule': 'test', 'file': None, 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: unsupported parameter: rule"),

    # Not providing vios_name parameter
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'firewall_facts', 'system_name': 'sys',
      'vios_name': None, 'level': None, 'rule': 'test', 'file': None, 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: mandatory parameter 'vios_name' is missing"),

    # Not providing system_name parameter
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'firewall_facts', 'system_name': None,
      'vios_name': 'vios', 'level': None, 'rule': 'test', 'file': None, 'firewall_config': None,
      'ip_version': None, 'active': None, 'reload': None},
     "ParameterError: mandatory parameter 'system_name' is missing")]


def common_mock_setup(mocker):
    hmc_alt_rootvg = importlib.import_module(IMPORT_HMC_VIOS_MAINTENANCE)
    mocker.patch.object(hmc_alt_rootvg, 'HmcCliConnection')
    mocker.patch.object(hmc_alt_rootvg, 'Hmc', autospec=True)
    return hmc_alt_rootvg


@pytest.mark.parametrize("vios_secure_test_input, expectedError", setting_security_test_data)
def test_call_security_apply(mocker, vios_secure_test_input, expectedError):
    hmc_vios_secure = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios_secure.apply_security_setting(hmc_vios_secure, vios_secure_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios_secure.apply_security_setting(hmc_vios_secure, vios_secure_test_input)


@pytest.mark.parametrize("vios_secure_test_input, expectedError", firewall_facts_test_data)
def test_call_firewall_facts(mocker, vios_secure_test_input, expectedError):
    hmc_vios_secure = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios_secure.display_firewall_setting(hmc_vios_secure, vios_secure_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios_secure.display_firewall_setting(hmc_vios_secure, vios_secure_test_input)
