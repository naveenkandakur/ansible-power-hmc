from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_MODULE = "ansible_collections.ibm.power_hmc.plugins.modules.power_network_bridge"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}

_SEA_FULL = {
    'load_balancing': False,
    'secondary_pvid': None,
    'jumbo_frames': False,
    'large_send': False,
    'qos_mode': None,
    'primary_vios': {'name': 'VIOS-01', 'backing_device': 'ent0',
                     'high_availability_mode': None},
    'secondary_vios': {'name': 'VIOS-02', 'backing_device': 'ent1',
                       'high_availability_mode': None},
    'tagged_virtual_networks': None,
}

_SEA_PRIMARY_ONLY = {
    'load_balancing': False,
    'secondary_pvid': None,
    'jumbo_frames': False,
    'large_send': False,
    'qos_mode': None,
    'primary_vios': {'name': 'VIOS-01', 'backing_device': 'ent0',
                     'high_availability_mode': None},
    'secondary_vios': None,
    'tagged_virtual_networks': None,
}

# Minimal shared_ethernet_adapter dict for state=update (no name/backing_device required)
_SEA_UPDATE = {
    'load_balancing': False,
    'secondary_pvid': None,
    'jumbo_frames': False,
    'large_send': False,
    'qos_mode': None,
    'primary_vios': {'high_availability_mode': None},
    'secondary_vios': None,
    'tagged_virtual_networks': None,
}


def _p(state, **kw):
    '''Build a minimal params dict for the given state with all top-level keys present.'''
    base = {
        'hmc_host': '0.0.0.0',
        'hmc_auth': hmc_auth,
        'state': state,
        'system_name': 'system1',
        'virtual_network_name': None,
        'shared_ethernet_adapter': None,
    }
    base.update(kw)
    return base


VN_NAME = 'VLAN104-ETHERNET0'


# ---------------------------------------------------------------------------
# state=facts
# ---------------------------------------------------------------------------
test_data_facts = [
    # missing hmc_host
    (_p('facts', hmc_host=None),
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # missing system_name
    (_p('facts', system_name=None),
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # virtual_network_name unsupported for facts
    (_p('facts', virtual_network_name=VN_NAME),
     "ParameterError: unsupported parameter: virtual_network_name"),
    # shared_ethernet_adapter unsupported for facts
    (_p('facts', shared_ethernet_adapter=_SEA_PRIMARY_ONLY),
     "ParameterError: unsupported parameter: shared_ethernet_adapter"),
]

# ---------------------------------------------------------------------------
# state=present
# ---------------------------------------------------------------------------
test_data_present = [
    # missing hmc_host
    (_p('present', hmc_host=None, virtual_network_name=VN_NAME, shared_ethernet_adapter=_SEA_FULL),
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # missing system_name
    (_p('present', system_name=None, virtual_network_name=VN_NAME, shared_ethernet_adapter=_SEA_FULL),
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # missing virtual_network_name
    (_p('present', shared_ethernet_adapter=_SEA_FULL),
     "ParameterError: mandatory parameter 'virtual_network_name' is missing"),
    # missing shared_ethernet_adapter
    (_p('present', virtual_network_name=VN_NAME),
     "ParameterError: mandatory parameter 'shared_ethernet_adapter' is missing"),
    # missing shared_ethernet_adapter.primary_vios.name
    (_p('present', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_FULL, 'primary_vios': None}),
     "ParameterError: shared_ethernet_adapter.primary_vios.name is required when state=present"),
    # missing shared_ethernet_adapter.primary_vios.backing_device
    (_p('present', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_FULL, 'primary_vios': {'name': 'VIOS-01'}}),
     "ParameterError: shared_ethernet_adapter.primary_vios.backing_device is required when state=present"),
    # missing secondary_vios.backing_device
    (_p('present', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_FULL, 'secondary_vios': {'name': 'VIOS-02'}}),
     "ParameterError: shared_ethernet_adapter.secondary_vios.backing_device is required when secondary_vios is configured"),
    # invalid qos_mode
    (_p('present', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_FULL, 'qos_mode': 'best-effort'}),
     "ParameterError: shared_ethernet_adapter.qos_mode must be one of disabled, loose, strict; got: best-effort"),
    # secondary_pvid requires load_balancing=True
    (_p('present', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_FULL, 'load_balancing': False, 'secondary_pvid': 200}),
     "ParameterError: shared_ethernet_adapter.secondary_pvid is only valid when shared_ethernet_adapter.load_balancing=true"),
    # secondary_pvid out of range
    (_p('present', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_FULL, 'load_balancing': True, 'secondary_pvid': 5000}),
     "ParameterError: shared_ethernet_adapter.secondary_pvid must be between 1 and 4094; got: 5000"),
    # tagged_virtual_networks not allowed on state=present
    (_p('present', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_FULL, 'tagged_virtual_networks': ['VLAN200-ETHERNET0']}),
     "ParameterError: shared_ethernet_adapter.tagged_virtual_networks is only valid when state=update"),
]

# ---------------------------------------------------------------------------
# state=update
# ---------------------------------------------------------------------------
test_data_update = [
    # missing hmc_host
    (_p('update', hmc_host=None, virtual_network_name=VN_NAME, shared_ethernet_adapter=_SEA_UPDATE),
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # missing system_name
    (_p('update', system_name=None, virtual_network_name=VN_NAME, shared_ethernet_adapter=_SEA_UPDATE),
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # missing virtual_network_name
    (_p('update', shared_ethernet_adapter=_SEA_UPDATE),
     "ParameterError: mandatory parameter 'virtual_network_name' is missing"),
    # missing shared_ethernet_adapter
    (_p('update', virtual_network_name=VN_NAME),
     "ParameterError: mandatory parameter 'shared_ethernet_adapter' is missing"),
    # invalid qos_mode
    (_p('update', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_UPDATE, 'qos_mode': 'best-effort'}),
     "ParameterError: shared_ethernet_adapter.qos_mode must be one of disabled, loose, strict; got: best-effort"),
    # secondary_pvid without load_balancing
    (_p('update', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_UPDATE, 'load_balancing': False, 'secondary_pvid': 200}),
     "ParameterError: shared_ethernet_adapter.secondary_pvid is only valid when shared_ethernet_adapter.load_balancing=true"),
    # invalid high_availability_mode on primary_vios
    (_p('update', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_UPDATE,
                                 'secondary_vios': {'high_availability_mode': None},
                                 'primary_vios': {'high_availability_mode': 'badmode'}}),
     "ParameterError: shared_ethernet_adapter.primary_vios.high_availability_mode must be one of disabled, auto, standby; got: badmode"),
    # tagged_virtual_networks with non-string entries
    (_p('update', virtual_network_name=VN_NAME,
        shared_ethernet_adapter={**_SEA_UPDATE, 'tagged_virtual_networks': [42]}),
     "ParameterError: shared_ethernet_adapter.tagged_virtual_networks must be a non-empty list of strings"),
]

# ---------------------------------------------------------------------------
# state=absent
# ---------------------------------------------------------------------------
test_data_absent = [
    # missing hmc_host
    (_p('absent', hmc_host=None, virtual_network_name=VN_NAME),
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # missing system_name
    (_p('absent', system_name=None, virtual_network_name=VN_NAME),
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # missing virtual_network_name
    (_p('absent'),
     "ParameterError: mandatory parameter 'virtual_network_name' is missing"),
    # shared_ethernet_adapter unsupported for absent
    (_p('absent', virtual_network_name=VN_NAME, shared_ethernet_adapter=_SEA_PRIMARY_ONLY),
     "ParameterError: unsupported parameter: shared_ethernet_adapter"),
]


def common_mock_setup(mocker):
    mod = importlib.import_module(IMPORT_MODULE)
    mocker.patch.object(mod, 'HmcCliConnection')
    mocker.patch.object(mod, 'Hmc', autospec=True)
    return mod


@pytest.mark.parametrize("test_input, expected_error", test_data_facts)
def test_facts_parameter_validation(mocker, test_input, expected_error):
    mod = common_mock_setup(mocker)
    with pytest.raises(ParameterError) as e:
        mod.validate_parameters(test_input)
    assert expected_error == repr(e.value)


@pytest.mark.parametrize("test_input, expected_error", test_data_present)
def test_present_parameter_validation(mocker, test_input, expected_error):
    mod = common_mock_setup(mocker)
    with pytest.raises(ParameterError) as e:
        mod.validate_parameters(test_input)
    assert expected_error == repr(e.value)


@pytest.mark.parametrize("test_input, expected_error", test_data_update)
def test_update_parameter_validation(mocker, test_input, expected_error):
    mod = common_mock_setup(mocker)
    with pytest.raises(ParameterError) as e:
        mod.validate_parameters(test_input)
    assert expected_error == repr(e.value)


@pytest.mark.parametrize("test_input, expected_error", test_data_absent)
def test_absent_parameter_validation(mocker, test_input, expected_error):
    mod = common_mock_setup(mocker)
    with pytest.raises(ParameterError) as e:
        mod.validate_parameters(test_input)
    assert expected_error == repr(e.value)
