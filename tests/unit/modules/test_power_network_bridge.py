from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_MODULE = "ansible_collections.ibm.power_hmc.plugins.modules.power_network_bridge"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}

_NB_FULL = {
    'load_balancing': False,
    'secondary_pvid': None,
    'jumbo_frames': False,
    'large_send': False,
    'qos_mode': None,
    'primary_vios': {'name': 'VIOS-01', 'backing_device': 'ent0',
                     'high_availability_mode': None},
    'secondary_vios': {'name': 'VIOS-02', 'backing_device': 'ent1',
                       'high_availability_mode': None},
}

_NB_PRIMARY_ONLY = {
    'load_balancing': False,
    'secondary_pvid': None,
    'jumbo_frames': False,
    'large_send': False,
    'qos_mode': None,
    'primary_vios': {'name': 'VIOS-01', 'backing_device': 'ent0',
                     'high_availability_mode': None},
    'secondary_vios': None,
}

# Minimal network_bridge dict for state=update (no name/backing_device required)
_NB_UPDATE = {
    'load_balancing': False,
    'secondary_pvid': None,
    'jumbo_frames': False,
    'large_send': False,
    'qos_mode': None,
    'primary_vios': {'high_availability_mode': None},
    'secondary_vios': None,
}


def _p(state, **kw):
    '''Build a minimal params dict for the given state with all top-level keys present.'''
    base = {
        'hmc_host': '0.0.0.0',
        'hmc_auth': hmc_auth,
        'state': state,
        'system_name': 'system1',
        'port_vlan_id': None,
        'virtual_network_name': None,
        'network_bridge': None,
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
    # network_bridge unsupported for facts
    (_p('facts', network_bridge=_NB_PRIMARY_ONLY),
     "ParameterError: unsupported parameter: network_bridge"),
]

# ---------------------------------------------------------------------------
# state=present  (port_vlan_id is NOT accepted — it is derived from the VN)
# ---------------------------------------------------------------------------
test_data_present = [
    # missing hmc_host
    (_p('present', hmc_host=None, virtual_network_name=VN_NAME, network_bridge=_NB_FULL),
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # missing system_name
    (_p('present', system_name=None, virtual_network_name=VN_NAME, network_bridge=_NB_FULL),
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # missing virtual_network_name
    (_p('present', network_bridge=_NB_FULL),
     "ParameterError: mandatory parameter 'virtual_network_name' is missing"),
    # missing network_bridge
    (_p('present', virtual_network_name=VN_NAME),
     "ParameterError: mandatory parameter 'network_bridge' is missing"),
    # port_vlan_id is unsupported for present (computed from VN)
    (_p('present', port_vlan_id=104, virtual_network_name=VN_NAME, network_bridge=_NB_FULL),
     "ParameterError: unsupported parameter: port_vlan_id"),
    # missing network_bridge.primary_vios.name
    (_p('present', virtual_network_name=VN_NAME,
        network_bridge={**_NB_FULL, 'primary_vios': None}),
     "ParameterError: network_bridge.primary_vios.name is required when state=present"),
    # missing network_bridge.primary_vios.backing_device
    (_p('present', virtual_network_name=VN_NAME,
        network_bridge={**_NB_FULL, 'primary_vios': {'name': 'VIOS-01'}}),
     "ParameterError: network_bridge.primary_vios.backing_device is required when state=present"),
    # missing secondary_vios.backing_device
    (_p('present', virtual_network_name=VN_NAME,
        network_bridge={**_NB_FULL, 'secondary_vios': {'name': 'VIOS-02'}}),
     "ParameterError: network_bridge.secondary_vios.backing_device is required when secondary_vios is configured"),
    # invalid qos_mode
    (_p('present', virtual_network_name=VN_NAME,
        network_bridge={**_NB_FULL, 'qos_mode': 'best-effort'}),
     "ParameterError: network_bridge.qos_mode must be one of disabled, loose, strict; got: best-effort"),
    # secondary_pvid requires load_balancing=True
    (_p('present', virtual_network_name=VN_NAME,
        network_bridge={**_NB_FULL, 'load_balancing': False, 'secondary_pvid': 200}),
     "ParameterError: network_bridge.secondary_pvid is only valid when network_bridge.load_balancing=true"),
    # secondary_pvid out of range
    (_p('present', virtual_network_name=VN_NAME,
        network_bridge={**_NB_FULL, 'load_balancing': True, 'secondary_pvid': 5000}),
     "ParameterError: network_bridge.secondary_pvid must be between 1 and 4094; got: 5000"),
    # tagged_virtual_networks not allowed on state=present
    (_p('present', virtual_network_name=VN_NAME,
        network_bridge={**_NB_FULL, 'tagged_virtual_networks': ['VLAN200-ETHERNET0']}),
     "ParameterError: network_bridge.tagged_virtual_networks is only valid when state=update"),
]

# ---------------------------------------------------------------------------
# state=update
# ---------------------------------------------------------------------------
test_data_update = [
    # missing hmc_host
    (_p('update', hmc_host=None, port_vlan_id=104, network_bridge=_NB_UPDATE),
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # missing system_name
    (_p('update', system_name=None, port_vlan_id=104, network_bridge=_NB_UPDATE),
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # missing port_vlan_id
    (_p('update', network_bridge=_NB_UPDATE),
     "ParameterError: mandatory parameter 'port_vlan_id' is missing"),
    # missing network_bridge
    (_p('update', port_vlan_id=104),
     "ParameterError: mandatory parameter 'network_bridge' is missing"),
    # virtual_network_name unsupported for update
    (_p('update', port_vlan_id=104, virtual_network_name=VN_NAME, network_bridge=_NB_UPDATE),
     "ParameterError: unsupported parameter: virtual_network_name"),
    # invalid qos_mode
    (_p('update', port_vlan_id=104,
        network_bridge={**_NB_UPDATE, 'qos_mode': 'best-effort'}),
     "ParameterError: network_bridge.qos_mode must be one of disabled, loose, strict; got: best-effort"),
    # secondary_pvid without load_balancing
    (_p('update', port_vlan_id=104,
        network_bridge={**_NB_UPDATE, 'load_balancing': False, 'secondary_pvid': 200}),
     "ParameterError: network_bridge.secondary_pvid is only valid when network_bridge.load_balancing=true"),
    # invalid high_availability_mode on primary_vios
    (_p('update', port_vlan_id=104,
        network_bridge={**_NB_UPDATE,
                        'primary_vios': {'high_availability_mode': 'badmode'}}),
     "ParameterError: network_bridge.primary_vios.high_availability_mode must be one of disabled, auto, standby; got: badmode"),
    # tagged_virtual_networks with non-string entries
    (_p('update', port_vlan_id=104,
        network_bridge={**_NB_UPDATE, 'tagged_virtual_networks': [42]}),
     "ParameterError: network_bridge.tagged_virtual_networks must be a non-empty list of strings"),
]

# ---------------------------------------------------------------------------
# state=absent
# ---------------------------------------------------------------------------
test_data_absent = [
    # missing hmc_host
    (_p('absent', hmc_host=None, port_vlan_id=104),
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # missing system_name
    (_p('absent', system_name=None, port_vlan_id=104),
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # missing port_vlan_id
    (_p('absent'),
     "ParameterError: mandatory parameter 'port_vlan_id' is missing"),
    # virtual_network_name unsupported for absent
    (_p('absent', port_vlan_id=104, virtual_network_name=VN_NAME),
     "ParameterError: unsupported parameter: virtual_network_name"),
    # network_bridge unsupported for absent
    (_p('absent', port_vlan_id=104, network_bridge=_NB_PRIMARY_ONLY),
     "ParameterError: unsupported parameter: network_bridge"),
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
