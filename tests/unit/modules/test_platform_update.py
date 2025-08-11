from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_HMC_PLATFORM_UPDATE = "ansible_collections.ibm.power_hmc.plugins.modules.platform_update"


class FakeModule:
    def __init__(self, params):
        self.params = params
        self.fail_msg = None

    def fail_json(self, msg):
        raise Exception(f"ParameterError: {msg}")


hmc_auth = {'username': 'hscroot', 'password': 'password_value'}
facts_test_data = [
    # All Facts related test cases
    # Not providing hmc host
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys'},
        "ParameterError: mandatory parameter [hmc_host] is missing"),

    # Not providing hmc_auth
    ({'hmc_host': 'hmc_host', 'hmc_auth': None, 'state': 'facts', 'system_name': 'sys'},
        "ParameterError: mandatory parameter [hmc_auth] is missing"),

    # Not providing system_name
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': None},
        "ParameterError: mandatory parameter [system_name] is missing"),

    # providing both state and platform_config
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'state': 'facts', 'system_name': 'sys',
        'platform_config': {'vios_update': [{'update_type': 'NoUpdate', 'vios_name': 'vios_name', 'update_order': 1, 'resource_type': None}]}},
        "ParameterError: Invalid parameter combination: 'state' and 'platform_config' cannot be used together. Please provide only one of them."),

    # Not providing state and platform_config
    ({'hmc_host': 'hmc_host', 'hmc_auth': hmc_auth, 'system_name': None},
        "ParameterError: Missing required parameter: Please provide either 'state' or 'platform_config'."),
]

platform_config_test_data = [
    # All platform_config test cases

    # Missing hmc_host
    (
        {'hmc_host': None, 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'state': None, 'system_name': 'sys',
         'platform_config': {'vios_update': [{'update_type': 'NoUpdate', 'vios_name': 'vios1', 'update_order': 1}]}},
        "ParameterError: mandatory parameter [hmc_host] is missing"
    ),

    # Missing hmc_auth
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': None, 'state': None, 'system_name': 'sys',
         'platform_config': {'vios_update': [{'update_type': 'NoUpdate', 'vios_name': 'vios1', 'update_order': 1}]}},
        "ParameterError: mandatory parameter [hmc_auth] is missing"
    ),

    # Missing system_name
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'state': None, 'system_name': None,
         'platform_config': {'vios_update': [{'update_type': 'NoUpdate', 'vios_name': 'vios1', 'update_order': 1}]}},
        "ParameterError: mandatory parameter [system_name] is missing"
    ),

    # Both state and platform_config provided
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'state': 'facts', 'system_name': 'sys',
         'platform_config': {'vios_update': [{'update_type': 'Update', 'vios_name': 'vios1', 'update_order': 1}]}},
        "ParameterError: Invalid parameter combination: 'state' and 'platform_config' cannot be used together. Please provide only one of them."
    ),

    # Neither state nor platform_config provided
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'state': None, 'system_name': 'sys'},
        "ParameterError: Missing required parameter: Please provide either 'state' or 'platform_config'."
    ),

    # vios_update with NoUpdate and level not latest
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
         'platform_config': {'vios_update': [{'update_type': 'NoUpdate', 'vios_name': 'vios1', 'update_order': 1, 'level': 'fixpack-3'}]}},
        "ParameterError: Parameter 'level' is not supported for vios_update when update_type = 'noupdate'"
    ),

    # system_firmware_update with update_type=NoUpdate and no sriov_adapter_update
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
         'platform_config': {'system_firmware_update': {'update_type': 'NoUpdate', 'update_order': 1}}},
        "ParameterError: Missing parameter sriov_adapter_update for system_firmware_update"
    ),

    # sriov_adapter_update missing both 'all' and 'adapter_id'
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
            'platform_config': {'system_firmware_update': {'update_type': 'NoUpdate', 'update_order': 1, 'level': 'latest',
                                                           'sriov_adapter_update': [{'subtype': 'DriverOnly'}]}}},
        "ParameterError: either all or adapter_id parameter is required"
    ),

    # sriov_adapter_update has both 'all' and 'adapter_id'
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
            'platform_config': {'system_firmware_update': {'update_type': 'NoUpdate', 'update_order': 1, 'level': 'latest',
                                                           'sriov_adapter_update': [{'all': True, 'adapter_id': 'adapter1',
                                                                                      'subtype': 'Adapter'}]}}},
        "ParameterError: Parameter all and adapter_id are mutually exculsive"
    ),

    # partition_migration without vios_update or system_firmware_update
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
            'platform_config': {'partition_migration': [{'is_quick_evac': True, 'destination_managed_system': 'ms1'}]}},
        "ParameterError: Invalid usage: 'partition_migration' must be specified along with either 'vios_update' or 'system_firmware_update'"
    ),

    # system_firmware_update with update_type 'update' and sriov_adapter_update present (invalid combo)
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
         'platform_config': {
            'system_firmware_update': {
                'update_type': 'Update',
                'update_order': 1,
                'sriov_adapter_update': [{'all': True, 'subtype': 'Adapter'}]
            }
        }},
        "ParameterError: Invalid combination: sriov_adapter_update is not allowed with update_type = 'update'"
    ),

    # system_firmware_update with update_type 'NoUpdate' and level != 'latest'
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
         'platform_config': {
             'system_firmware_update': {
                 'update_type': 'NoUpdate',
                 'update_order': 1,
                 'level': 'fixpack-10',
                 'sriov_adapter_update': [{'all': True, 'subtype': 'Adapter'}]
             }
        }},
        "ParameterError: Parameter 'level' is not supported for system_firmware_update when update_type = 'noupdate'"
    ),

    # sriov_adapter_update missing subtype (mandatory)
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
         'platform_config': {
             'system_firmware_update': {
                 'update_type': 'NoUpdate',
                 'update_order': 1,
                 'level': 'latest',
                 'sriov_adapter_update': [{'all': True}]
             }
        }},
        "ParameterError: mandatory parameter subtype is missing for sriov_adapter_update"
    ),

    # io_adapter_update with 'all' and 'device' together (invalid combo)
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
         'platform_config': {
             'vios_update': [{
                 'update_type': 'Update',
                 'vios_name': 'vios1',
                 'update_order': 1,
                 'io_adapter_update': [{'all': True, 'device': 'dev1'}]
             }]
        }},
        "ParameterError: 'all' is mutually exclusive with 'device'."
    ),

    # io_adapter_update missing device (mandatory when all not given)
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
         'platform_config': {
             'vios_update': [{
                 'update_type': 'Update',
                 'vios_name': 'vios1',
                 'update_order': 1,
                 'io_adapter_update': [{}]
             }]
        }},
        "ParameterError: mandatory parameter device is missing for io_adapter_update"
    ),

    # partition_migration missing is_quick_evac (mandatory)
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
         'platform_config': {
             'system_firmware_update': {
                 'update_type': 'NoUpdate',
                 'update_order': 1,
                 'level': 'latest',
                 'sriov_adapter_update': [{'all': True, 'subtype': 'DriverOnly'}]
             },
             'partition_migration': [{'destination_managed_system': 'sys2'}]
        }},
        "ParameterError: mandatory parameter [is_quick_evac] is missing for partition_migration"
    ),

    # partition_migration with unsupported field 'vios_name'
    (
        {'hmc_host': '1.2.3.4', 'hmc_auth': {'username': 'user', 'password': 'pass'}, 'system_name': 'sys', 'state': None,
         'platform_config': {
             'system_firmware_update': {
                 'update_type': 'NoUpdate',
                 'update_order': 1,
                 'level': 'latest',
                 'sriov_adapter_update': [{'all': True, 'subtype': 'DriverOnly'}]
             },
             'partition_migration': [{'is_quick_evac': True, 'destination_managed_system': 'sys2', 'vios_name': 'v1'}]
        }},
        "ParameterError: unsupported parameter [vios_name] for partition_migration"
    ),

]


def common_mock_setup(mocker):
    hmc_platform_update = importlib.import_module(IMPORT_HMC_PLATFORM_UPDATE)
    mocker.patch.object(hmc_platform_update, 'HmcCliConnection')
    mocker.patch.object(hmc_platform_update, 'Hmc', autospec=True)
    mocker.patch.object(hmc_platform_update, 'HmcRestClient', autospec=True)
    return hmc_platform_update


@pytest.mark.parametrize("fact_test_input, expectedError", facts_test_data)
def test_call_facts(mocker, fact_test_input, expectedError):
    module = FakeModule(fact_test_input)

    hmc_module = common_mock_setup(mocker)

    with pytest.raises(Exception) as excinfo:
        hmc_module.facts(module)

    assert "ParameterError:" in str(excinfo.value)
    assert expectedError in str(excinfo.value)


@pytest.mark.parametrize("platform_config_test_input, expectedError", platform_config_test_data)
def test_call_platform_config(mocker, platform_config_test_input, expectedError):
    module = FakeModule(platform_config_test_input)

    hmc_module = common_mock_setup(mocker)

    with pytest.raises(Exception) as excinfo:
        hmc_module.platform_update(module)

    assert "ParameterError:" in str(excinfo.value)
    assert expectedError in str(excinfo.value)
