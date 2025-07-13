from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_SVCEVENT = "ansible_collections.ibm.power_hmc.plugins.modules.create_service_event"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}
test_data = [
    # title is missed
    ({'hmc_host': 'data', 'hmc_auth': hmc_auth, 'state': 'created', 'system': None,
      'description': 'test', 'types': 'vios', 'attributes':
     {'title': None, 'severity': '2', 'contact_name': 'Test',
      'contact_phone': 'data', 'contact_email': 'data', 'service_file': ['pedbgq4'],
      'target_lpar_name': None, 'target_mtms': None, 'lpar_name': 'data'}},
     "ParameterError: title is mandatory in 'attributes' parameter"),

    # severity is missed
    ({'hmc_host': 'data', 'hmc_auth': hmc_auth, 'state': 'created', 'system': None,
      'description': 'test', 'types': 'vios', 'attributes':
     {'title': 'data', 'severity': None, 'contact_name': 'Test',
      'contact_phone': 'data', 'contact_email': 'data', 'service_file': ['pedbgq4'],
      'target_lpar_name': None, 'target_mtms': None, 'lpar_name': 'data'}},
     "ParameterError: severity is mandatory in 'attributes' parameter"),

    # contact_name is missed
    ({'hmc_host': 'data', 'hmc_auth': hmc_auth, 'state': 'created', 'system': None,
      'description': 'test', 'types': 'vios', 'attributes':
     {'title': 'data', 'severity': '2', 'contact_name': None,
      'contact_phone': 'data', 'contact_email': 'data', 'service_file': ['pedbgq4'],
      'target_lpar_name': None, 'target_mtms': None, 'lpar_name': 'data'}},
     "ParameterError: contact_name is mandatory in 'attributes' parameter"),

    # contact_phone is missed
    ({'hmc_host': 'data', 'hmc_auth': hmc_auth, 'state': 'created', 'system': None,
      'description': 'test', 'types': 'vios', 'attributes':
     {'title': 'data', 'severity': '2', 'contact_name': 'data',
      'contact_phone': None, 'contact_email': 'data', 'service_file': ['pedbgq4'],
      'target_lpar_name': None, 'target_mtms': None, 'lpar_name': 'data'}},
     "ParameterError: contact_phone is mandatory in 'attributes' parameter"),

    # contact_email is missed
    ({'hmc_host': 'data', 'hmc_auth': hmc_auth, 'state': 'created', 'system': None,
      'description': 'test', 'types': 'vios', 'attributes':
     {'title': 'data', 'severity': '2', 'contact_name': 'data',
      'contact_phone': 'data', 'contact_email': None, 'service_file': ['pedbgq4'],
      'target_lpar_name': None, 'target_mtms': None, 'lpar_name': 'data'}},
     "ParameterError: contact_email is mandatory in 'attributes' parameter"),

    # service_file is missed
    ({'hmc_host': 'data', 'hmc_auth': hmc_auth, 'state': 'created', 'system': None,
      'description': 'test', 'types': 'vios', 'attributes':
     {'title': 'data', 'severity': '2', 'contact_name': 'data',
      'contact_phone': 'data', 'contact_email': 'data', 'service_file': None,
      'target_lpar_name': None, 'target_mtms': None, 'lpar_name': 'data'}},
     "ParameterError: service_file is mandatory in 'attributes' parameter"),

    # lpar_name is missed for vios type
    ({'hmc_host': 'data', 'hmc_auth': hmc_auth, 'state': 'created', 'system': None,
      'description': 'test', 'types': 'vios', 'attributes':
     {'title': 'data', 'severity': '2', 'contact_name': 'data',
      'contact_phone': 'data', 'contact_email': 'data', 'service_file': None,
      'target_lpar_name': None, 'target_mtms': None, 'lpar_name': None}},
     "ParameterError: 'lpar_name' is mandatory for types: vios, lpm"),

    # lpar_name is missed for lpm type
    ({'hmc_host': 'data', 'hmc_auth': hmc_auth, 'state': 'created', 'system': None,
      'description': 'test', 'types': 'lpm', 'attributes':
     {'title': 'data', 'severity': '2', 'contact_name': 'data',
      'contact_phone': 'data', 'contact_email': 'data', 'service_file': None,
      'target_lpar_name': None, 'target_mtms': None, 'lpar_name': None}},
     "ParameterError: 'lpar_name' is mandatory for types: vios, lpm"),

    # target_lpar_name is missed for lpm type
    ({'hmc_host': 'data', 'hmc_auth': hmc_auth, 'state': 'created', 'system': None,
      'description': 'test', 'types': 'lpm', 'attributes':
     {'title': 'data', 'severity': '2', 'contact_name': 'data',
      'contact_phone': 'data', 'contact_email': 'data', 'service_file': None,
      'target_lpar_name': None, 'target_mtms': 'data', 'lpar_name': 'data'}},
     "ParameterError: 'target_lpar_name' is mandatory for types: lpm"),

    # target_mtms is missed for lpm type
    ({'hmc_host': 'data', 'hmc_auth': hmc_auth, 'state': 'created', 'system': None,
      'description': 'test', 'types': 'lpm', 'attributes':
     {'title': 'data', 'severity': '2', 'contact_name': 'data',
      'contact_phone': 'data', 'contact_email': 'data', 'service_file': None,
      'target_lpar_name': 'data', 'target_mtms': None, 'lpar_name': 'data'}},
     "ParameterError: 'target_mtms' is mandatory for types: lpm"),
]


def common_mock_setup(mocker):
    svcevent = importlib.import_module(IMPORT_SVCEVENT)
    mocker.patch.object(svcevent, 'HmcCliConnection')
    mocker.patch.object(svcevent, 'Hmc', autospec=True)
    return svcevent


@pytest.mark.parametrize("test_input, expectedError", test_data)
def test_update_vios(mocker, test_input, expectedError):
    svcevent_created = common_mock_setup(mocker)
    svcevent_created.Hmc.checkIfHMCFullyBootedUp.return_value = (True, {})
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            svcevent_created.create_svc_events(svcevent_created, test_input)
        assert expectedError == repr(e.value)
    else:
        svcevent_created.create_svc_events(svcevent_created, test_input)
