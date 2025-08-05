#!/usr/bin/python

# Copyright: (c) 2018- IBM, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: create_service_event
author:
    - Sreenidhi S(@SreenidhiS1)
short_description: Creates a serviceable event on the Hardware Management Console (HMC) to report a problem that occurred on managed-system.
notes:
    - This module requires the HMC which has Power10 systems licensed for advanced automation and monitoring or for Power11 systems.
description:
    - Creates a serviceable event on the Hardware Management Console (HMC) to report a problem that occurred on managed-system
      or this HMC and to request service to repair it.
version_added: 1.0.0
requirements:
- Python >= 3
options:
    hmc_host:
        description:
            - The IP Address or hostname of the HMC.
        required: true
        type: str
    hmc_auth:
        description:
            - Username and Password credential of the HMC.
        required: true
        type: dict
        suboptions:
            username:
                description:
                    - Username of the HMC to login.
                required: true
                type: str
            password:
                description:
                    - Password of the HMC.
                type: str
    system_name:
        description:
            - The name of the managed system for which to create the serviceable event.
        required: true
        type: str
    description:
        description:
            - The problem description.
        required: true
        type: str
    types:
        description:
            - The type of event to create.
            - C(sys) to report a problem with managed-system.
            - C(vios) to report a problem with a Virtual I/O Server on managed-system.
            - C(lpm) to report a partition migration problem where managed-system is the source system for the partition migration operation.
            - C(hmc) to report a problem with this HMC.
            - C(cloudconnector) to report a problem with the cloud connector on this HMC.
        required: true
        type: str
        choices: ['cloudconnector', 'sys', 'lpm', 'vios', 'hmc']
    attributes:
        description:
            - The serviceable event attributes to set.
        type: dict
        required: true
        suboptions:
            title:
                description:
                    - Title for the serviceable event.
                type: str
                required: true
            severity:
                description:
                    - The priority for the serviceable event.
                type: int
                required: true
                choices: [1, 2, 3, 4]
            contact_name:
                description:
                    - The contact name for the serviceable event.
                required: true
                type: str
            contact_email:
                description:
                    - The contact email for the serviceable event.
                required: true
                type: str
            contact_phone:
                description:
                    - The contact phone number for the serviceable event.
                required: true
                type: int
            target_lpar_name:
                description:
                    - The target partition name for the serviceable event.
                    - Required for C(lpm)
                type: str
            target_mtms:
                description:
                    - The target managed system MTMS for the serviceable event.
                    - Required for C(lpm)
                type: str
            lpar_name:
                description:
                    - The partition name for the serviceable event.
                    - Required for C(lpm) and C(vios)
                type: str
            service_file:
                description:
                    - The partition name for the serviceable event.
                    - Required for C(lpm) and C(vios)
                type: list
                elements: str
                required: true
                choices: ['pedbgq4', 'pedbgq8', 'vios', 'lpmffdc', 'rscdump', 'spdump']
    state:
        description:
            - C(created) to create a serviceable event.
        type: str
        choices: ['created']
'''

EXAMPLES = '''
- name: Create a serviceable event for collection of vios logs
  svcevent:
    hmc_host: '{{ inventory_hostname }}'
    hmc_auth: "{{ curr_hmc_auth }}"
    system_name: <system name>
    description: Test Description
    types: vios
    attributes:
        title: test
        severity: 4
        contact_name: Test
        contact_phone: < phone-num >
        contact_email: test@abc.com
        lpar_name: < partition >
        service_file:
            - pedbgq4
            - vios
    state: created

- name: Create a serviceable event for collection of lpm logs
  svcevent:
    hmc_host: '{{ inventory_hostname }}'
    hmc_auth: "{{ curr_hmc_auth }}"
    system_name: <system name>
    description: Test Description
    types: vios
    attributes:
        title: test
        severity: 4
        contact_name: Test
        contact_phone: < phone-num >
        contact_email: test@abc.com
        lpar_name: < partition1 >
        target_lpar_name: <partition2 >
        target_mtms: < target-sys >
        service_file:
            - pedbgq4
            - vios
    state: created
'''

import logging
LOG_FILENAME = "/tmp/ansible_power_hmc.log"
logger = logging.getLogger(__name__)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_cli_client import HmcCliConnection
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_resource import Hmc
import sys

USER_AUTHORITY_ERR = "HSCL350B The user does not have the appropriate authority"


def init_logger():
    logging.basicConfig(
        filename=LOG_FILENAME,
        format='[%(asctime)s] %(levelname)s: [%(funcName)s] %(message)s',
        level=logging.DEBUG)


def validate_parameters(params):
    '''Check that the input parameters satisfy the mutual exclusiveness of HMC'''
    attributes = params['attributes']
    madatory_attribures = ['title', 'severity', 'contact_name', 'contact_phone', 'contact_email']
    for each in madatory_attribures:
        if attributes[each] is None:
            raise ParameterError(f"{each} is mandatory in 'attributes' parameter")
    if params['types'] in ['lpm', 'vios']:
        if attributes['lpar_name'] is None:
            raise ParameterError("'lpar_name' is mandatory for types: vios, lpm")
    if params['types'] == 'lpm':
        if attributes['target_mtms'] is None:
            raise ParameterError("'target_mtms' is mandatory for types: lpm")
        if attributes['target_lpar_name'] is None:
            raise ParameterError("'target_lpar_name' is mandatory for types: lpm")

    if attributes['service_file'] is not None:
        valid_service_files = {
            'sys': {'pedbgq4', 'rscdump', 'spdump'},
            'hmc': {'pedbgq4'},
            'vios': {'pedbgq4', 'vios'},
            'lpm': {'pedbgq4', 'lpmffdc'},
            'cloudconnector': {'pedbgq8'},
        }
        selected_type = params['types']
        service_files = attributes['service_file']
        invalid_files = [
            f for f in service_files
            if f not in valid_service_files.get(selected_type, set())
        ]
        if invalid_files:
            raise ParameterError(
                f"Invalid service_file(s): {', '.join(invalid_files)} for types '{selected_type}'. "
            )
    else:
        raise ParameterError("service_file is mandatory in 'attributes' parameter")


def create_svc_events(module, params):
    created = []
    hmc_host = params['hmc_host']
    hmc_user = params['hmc_auth']['username']
    password = params['hmc_auth']['password']
    hmc_conn = HmcCliConnection(module, hmc_host, hmc_user, password)
    hmc = Hmc(hmc_conn)
    validate_parameters(params)
    m_system = params['system_name']
    sys_list = hmc.list_all_managed_system_details("name") + hmc.list_all_managed_system_details("type_model*serial_num")
    sys_list = [list(d.values())[0] for d in sys_list]
    if m_system not in sys_list:
        module.fail_json(msg="The managed system is not available in HMC")
    if hmc.getManagedSystemDetails(m_system, "advanced_hmc_automation_and_monitoring_capable").strip() != '1':
        module.fail_json(msg="This module is supported only for systems where advanced hmc automation and monitoring capablity is enabled")
    lpar_list = hmc.list_all_lpars_details(m_system, "name")
    if params['attributes']['lpar_name'] is not None:
        if params['attributes']['lpar_name'] not in lpar_list:
            module.fail_json(msg="The partition is not available in HMC")
    if params['attributes']['target_mtms'] is not None:
        target_system = params['attributes']['target_mtms']
        if target_system not in sys_list:
            module.fail_json(msg="The target managed system is not available in HMC")
        target_lpar_name = params['attributes']['target_lpar_name']
        target_lpar_list = hmc.list_all_lpars_details(target_system, "name")
        if target_lpar_name not in target_lpar_list:
            module.fail_json(msg="The target partition is not available in HMC")
    try:
        output = hmc.create_svc_events(params)
        changed = True
        created.append(output)
        return changed, created, None
    except Exception as e:
        return False, repr(e), None


def perform_task(module):
    params = module.params
    actions = {
        "created": create_svc_events
    }

    if not params['hmc_auth']:
        return False, "missing credential info", None
    try:
        return actions[params['state']](module, params)
    except Exception as error:
        return False, repr(error), None


def run_module():
    module_args = dict(
        hmc_host=dict(type='str', required=True),
        hmc_auth=dict(type='dict',
                      required=True,
                      no_log=True,
                      options=dict(
                          username=dict(required=True, type='str'),
                          password=dict(type='str', no_log=True),
                      )
                      ),
        state=dict(type='str', choices=['created']),
        system_name=dict(type='str', required=True),
        description=dict(type='str', required=True),
        types=dict(required=True, type='str', choices=['cloudconnector', 'sys', 'lpm', 'vios', 'hmc']),
        attributes=dict(type='dict', required=True,
                        options=dict(
                            title=dict(type='str', required=True,),
                            severity=dict(type='int', choices=[1, 2, 3, 4], required=True),
                            contact_name=dict(type='str', required=True),
                            contact_phone=dict(type='int', required=True),
                            contact_email=dict(type='str', required=True),
                            service_file=dict(type='list',
                                              choices=['pedbgq4', 'pedbgq8', 'vios', 'lpmffdc', 'rscdump', 'spdump'], required=True, elements='str'),
                            target_lpar_name=dict(type='str'),
                            target_mtms=dict(type='str'),
                            lpar_name=dict(type='str')
                        )
                        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
    )

    if module._verbosity >= 5:
        init_logger()

    if sys.version_info < (3, 0):
        py_ver = sys.version_info[0]
        module.fail_json(msg="Unsupported Python version {0}, supported python version is 3 and above".format(py_ver))

    changed, info, warning = perform_task(module)
    if isinstance(info, str):
        module.fail_json(msg=info)

    result = {}
    result['changed'] = changed
    result['info'] = info
    if warning:
        result['warning'] = warning

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
