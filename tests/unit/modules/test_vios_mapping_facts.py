from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_VIOS_MAPPING_FACTS = "ansible_collections.ibm.power_hmc.plugins.modules.vios_mapping_facts"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}

# Test data for vios_mapping_facts with state='facts'
test_data_facts = [
    # Missing hmc_host
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'all', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),

    # Missing hmc_auth
    ({'hmc_host': '0.0.0.0', 'hmc_auth': None, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'all', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: mandatory parameter 'hmc_auth' is missing"),

    # Missing vios_name
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': None,
      'component': 'all', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: mandatory parameter 'vios_name' is missing"),

    # Missing multiple mandatory parameters
    ({'hmc_host': None, 'hmc_auth': None, 'state': 'facts', 'system_name': 'sys', 'vios_name': None,
      'component': 'all', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: mandatory parameters 'hmc_host,hmc_auth,vios_name' are missing"),
]

# Test data for vscsi component
test_data_vscsi = [
    # vscsi with unsupported vtd parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'vscsi', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': 'vtd0', 'hostname': None},
     "ParameterError: unsupported parameter: vtd"),

    # vscsi with unsupported hostname parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'vscsi', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': 'host1'},
     "ParameterError: unsupported parameter: hostname"),

    # vscsi with multiple unsupported parameters
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'vscsi', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': 'vtd0', 'hostname': 'host1'},
     "ParameterError: unsupported parameters: vtd, hostname"),
]

# Test data for npiv component
test_data_npiv = [
    # npiv with unsupported vtd parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'npiv', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': ['disk'], 'vtd': 'vtd0', 'hostname': None},
     "ParameterError: unsupported parameters: vtd, types"),

    # npiv with unsupported types parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'npiv', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': ['disk'], 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: types"),

    # npiv with unsupported hostname parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'npiv', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': 'host1'},
     "ParameterError: unsupported parameter: hostname"),

    # npiv with multiple unsupported parameters
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'npiv', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': ['disk'], 'vtd': 'vtd0', 'hostname': 'host1'},
     "ParameterError: unsupported parameters: vtd, types, hostname"),
]

# Test data for vnic component
test_data_vnic = [
    # vnic with unsupported vtd parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'vnic', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': 'vtd0', 'hostname': None},
     "ParameterError: unsupported parameter: vtd"),

    # vnic with unsupported types parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'vnic', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': ['lv'], 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: types"),

    # vnic with unsupported hostname parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'vnic', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': 'host1'},
     "ParameterError: unsupported parameter: hostname"),
]

# Test data for net component
test_data_net = [
    # net with unsupported vtd parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'net', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': 'vtd0', 'hostname': None},
     "ParameterError: unsupported parameter: vtd"),

    # net with unsupported types parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'net', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': ['optical'], 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: types"),

    # net with unsupported cpid parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'net', 'vadapter': None, 'physloc': None, 'cpid': 1, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: cpid"),

    # net with unsupported hostname parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'net', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': 'host1'},
     "ParameterError: unsupported parameter: hostname"),

    # net with multiple unsupported parameters
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'net', 'vadapter': None, 'physloc': None, 'cpid': 1, 'types': ['tape'], 'vtd': 'vtd0', 'hostname': 'host1'},
     "ParameterError: unsupported parameters: vtd, types, cpid, hostname"),
]

# Test data for ams component
test_data_ams = [
    # ams with unsupported vadapter parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'ams', 'vadapter': 'vhost0', 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: vadapter"),

    # ams with unsupported physloc parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'ams', 'vadapter': None, 'physloc': 'U1234', 'cpid': None, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: physloc"),

    # ams with unsupported cpid parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'ams', 'vadapter': None, 'physloc': None, 'cpid': 2, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: cpid"),

    # ams with unsupported hostname parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'ams', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': 'host1'},
     "ParameterError: unsupported parameter: hostname"),
]

# Test data for suspend component
test_data_suspend = [
    # suspend with unsupported physloc parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'suspend', 'vadapter': None, 'physloc': 'U1234', 'cpid': None, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: physloc"),

    # suspend with unsupported vtd parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'suspend', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': 'vtd0', 'hostname': None},
     "ParameterError: unsupported parameter: vtd"),

    # suspend with unsupported cpid parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'suspend', 'vadapter': None, 'physloc': None, 'cpid': 3, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: cpid"),

    # suspend with unsupported hostname parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'suspend', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': 'host1'},
     "ParameterError: unsupported parameter: hostname"),
]

# Test data for cluster component
test_data_cluster = [
    # cluster with unsupported physloc parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'cluster', 'vadapter': None, 'physloc': 'U1234', 'cpid': None, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: physloc"),

    # cluster with unsupported vtd parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'cluster', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': None, 'vtd': 'vtd0', 'hostname': None},
     "ParameterError: unsupported parameter: vtd"),

    # cluster with unsupported cpid parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'cluster', 'vadapter': None, 'physloc': None, 'cpid': 4, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: cpid"),

    # cluster with unsupported types parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'cluster', 'vadapter': None, 'physloc': None, 'cpid': None, 'types': ['file'], 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: types"),

    # cluster with unsupported vadapter parameter
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'cluster', 'vadapter': 'vhost0', 'physloc': None, 'cpid': None, 'types': None, 'vtd': None, 'hostname': None},
     "ParameterError: unsupported parameter: vadapter"),

    # cluster with multiple unsupported parameters
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys', 'vios_name': 'vios',
      'component': 'cluster', 'vadapter': 'vhost0', 'physloc': 'U1234', 'cpid': 4, 'types': ['usb_disk'], 'vtd': 'vtd0', 'hostname': None},
     "ParameterError: unsupported parameters: physloc, vtd, cpid, types, vadapter"),
]


def common_mock_setup(mocker):
    vios_mapping_facts = importlib.import_module(IMPORT_VIOS_MAPPING_FACTS)
    mocker.patch.object(vios_mapping_facts, 'HmcCliConnection')
    mocker.patch.object(vios_mapping_facts, 'Hmc', autospec=True)
    return vios_mapping_facts


@pytest.mark.parametrize("mapping_facts_test_input, expectedError", test_data_facts)
def test_vios_mapping_facts_mandatory_params(mocker, mapping_facts_test_input, expectedError):
    vios_mapping_facts = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            vios_mapping_facts.validate_parameters(mapping_facts_test_input)
        assert expectedError == repr(e.value)


@pytest.mark.parametrize("mapping_facts_test_input, expectedError", test_data_vscsi)
def test_vios_mapping_facts_vscsi_component(mocker, mapping_facts_test_input, expectedError):
    vios_mapping_facts = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            vios_mapping_facts.validate_parameters(mapping_facts_test_input)
        assert expectedError == repr(e.value)


@pytest.mark.parametrize("mapping_facts_test_input, expectedError", test_data_npiv)
def test_vios_mapping_facts_npiv_component(mocker, mapping_facts_test_input, expectedError):
    vios_mapping_facts = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            vios_mapping_facts.validate_parameters(mapping_facts_test_input)
        assert expectedError == repr(e.value)


@pytest.mark.parametrize("mapping_facts_test_input, expectedError", test_data_vnic)
def test_vios_mapping_facts_vnic_component(mocker, mapping_facts_test_input, expectedError):
    vios_mapping_facts = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            vios_mapping_facts.validate_parameters(mapping_facts_test_input)
        assert expectedError == repr(e.value)


@pytest.mark.parametrize("mapping_facts_test_input, expectedError", test_data_net)
def test_vios_mapping_facts_net_component(mocker, mapping_facts_test_input, expectedError):
    vios_mapping_facts = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            vios_mapping_facts.validate_parameters(mapping_facts_test_input)
        assert expectedError == repr(e.value)


@pytest.mark.parametrize("mapping_facts_test_input, expectedError", test_data_ams)
def test_vios_mapping_facts_ams_component(mocker, mapping_facts_test_input, expectedError):
    vios_mapping_facts = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            vios_mapping_facts.validate_parameters(mapping_facts_test_input)
        assert expectedError == repr(e.value)


@pytest.mark.parametrize("mapping_facts_test_input, expectedError", test_data_suspend)
def test_vios_mapping_facts_suspend_component(mocker, mapping_facts_test_input, expectedError):
    vios_mapping_facts = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            vios_mapping_facts.validate_parameters(mapping_facts_test_input)
        assert expectedError == repr(e.value)


@pytest.mark.parametrize("mapping_facts_test_input, expectedError", test_data_cluster)
def test_vios_mapping_facts_cluster_component(mocker, mapping_facts_test_input, expectedError):
    vios_mapping_facts = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            vios_mapping_facts.validate_parameters(mapping_facts_test_input)
        assert expectedError == repr(e.value)
