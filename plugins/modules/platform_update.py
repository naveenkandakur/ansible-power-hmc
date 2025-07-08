# !/usr/bin/python

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
module: platform_update
author:
    - Chiranthan M V (@chiranthanmv)
short_description: Performs consolidated system firmware, VIOS, SR-IOV, and I/O adapter updates with migration and LPM readiness validation.
description:
    - This module allows updating System Firmware, VIOS, SR-IOV adapters, and I/O adapters either individually or through a single consolidated update flow.
    - The operations can be defined using the I(ParameterValue) structure.
    - It supports both minimal and full update strategies for SR-IOV adapters and allows updates from IBM Fix Central website when specified.
    - Supports defining the order in which updates are applied across components.
    - Includes validation for Live Partition Mobility (LPM) readiness and VIOS redundancy.
    - Compatible with update source like IBM Fix Central website (recommended for end-to-end automation)
version_added: 1.0.0
requirements:
- Python >= 3
options:
    hmc_host:
        description:
            - IP address or hostname of the target Hardware Management Console (HMC).
        required: true
        type: str
    hmc_auth:
        description:
            - Authentication credentials to connect to the HMC.
        required: true
        type: dict
        suboptions:
            username:
                description:
                    - Username for logging into the HMC.
                required: true
                type: str
            password:
                description:
                    - Password for the HMC user.
                required: false
                type: str
    system_name:
        description:
            - The name or mtms (machine type model serial) of the managed system on which the operations are to be performed.
        required: true
        type: str
    ParameterValue:
        description:
            - Specifies the operation details, including firmware update, partition migration, or VIOS update.
        required: false
        type: dict
        suboptions:
            SystemFirmwareUpdate:
                description:
                    - System firmware update configuration.
                type: dict
                suboptions:
                    UpdateType:
                        description:
                            - Type of firmware update operation.
                        type: str
                        choices: ['NoUpdate', 'Update', 'Upgrade']
                    UpdateOrder:
                        description:
                            - Optional order in which the update should be applied.
                        type: int
                    IsDestruptive:
                        description:
                            - Whether the update is disruptive (causes reboots/downtime).
                        type: bool
                    ResourceType:
                        description:
                            - Source type for firmware image (e.g., from IBM Fix Central).
                        type: str
                        choices: ['IBMWebsite']
                    Level:
                        description:
                            - Specifies the firmware version level to apply.
                            - If not provided, the latest available version will be used by default.
                        type: str
                        default: 'latest'
                    SRIOVAdapterUpdate:
                        description:
                            - List of SR-IOV adapter update configurations.
                        type: list
                        elements: dict
                        suboptions:
                            ALL:
                                description: Whether to apply the update to all adapters.
                                type: bool
                            AdapterID:
                                description: ID of the adapter to be updated.
                                type: str
                            SubType:
                                description: Level of update to apply.
                                type: str
                                choices: ['Minimal', 'Full']
            PartitionMigration:
                description:
                    - Configuration for migrating logical partitions.
                type: list
                elements: dict
                suboptions:
                    IsQuickEvac:
                        description: Whether to enable quick evacuation.
                        type: bool
                    DestinationManagedSystem:
                        description: Target managed system name.
                        type: str
                    LeavePartitionInTarget:
                        description: Whether to keep the partition in the target system post-migration.
                        type: bool
            VIOSUpdate:
                description:
                    - Configuration for updating Virtual I/O Servers.
                type: list
                elements: dict
                suboptions:
                    UpdateType:
                        description: Type of VIOS update.
                        type: str
                        choices: ['NoUpdate', 'Update']
                    VIOSName:
                        description: Name of the VIOS partition.
                        type: str
                    UpdateOrder:
                        description: Priority/order of update among multiple VIOS.
                        type: int
                    ResourceType:
                        description: Source type for the update.
                        type: str
                        choices: ['IBMWebsite']
                    Level:
                        description:
                            - Specifies the VIOS version level to apply.
                            - If not provided, the latest available version will be used by default.
                        type: str
                        default: 'latest'
                    IOAdapterUpdate:
                        description: List of I/O adapters to update during VIOS update.
                        type: list
                        elements: dict
                        suboptions:
                            ALL:
                                description: Whether to update all I/O adapters.
                                type: bool
                            Id:
                                description: Partition ID to update.
                                type: str
                            Device:
                                description: Device name of the adapter.
                                type: str
                            Repository:
                                description: Source repository for update image.
                                type: str
                                choices: ['IBMWebsite']
'''

EXAMPLES = '''
- name: Perform a minimal system firmware update using IBM Fix Central
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    ParameterValue:
      SystemFirmwareUpdate:
        UpdateType: NoUpdate
        UpdateOrder: 1
        SRIOVAdapterUpdate:
          - AdapterID: "ent0"
            SubType: Minimal

- name: Migrate a partition to a different managed system
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    ParameterValue:
      SystemFirmwareUpdate:
        UpdateType: Update
        UpdateOrder: 1
        ResourceType: IBMWebsite
      PartitionMigration:
        - IsQuickEvac: true
          DestinationManagedSystem: "p920_system"
          LeavePartitionInTarget: false

- name: Update VIOS using IBM Fix Central
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    ParameterValue:
      VIOSUpdate:
        - UpdateType: Update
          VIOSName: "vios1"
          UpdateOrder: 1
          ResourceType: IBMWebsite
          IOAdapterUpdate:
            - Id: "ent1"
              Device: "fcs0"
              Repository: IBMWebsite
'''

RETURN = '''
result:
    description: The result dictionary containing the status and details of the operation.
    type: dict
    returned: always
    sample: {
        "changed": true,
        "msg": "System firmware updated successfully"
    }
'''


import logging
LOG_FILENAME = "/Users/chiranthanmv/platform_up/ansible.log"
logger = logging.getLogger(__name__)
import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_cli_client import HmcCliConnection
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import HmcError
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_resource import Hmc
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_constants import HmcConstants
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_rest_client import parse_error_response
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_rest_client import HmcRestClient
import sys
import copy


def init_logger():
    logging.basicConfig(
        filename=LOG_FILENAME,
        format='[%(asctime)s] %(levelname)s: [%(funcName)s] %(message)s',
        level=logging.DEBUG)


def validate_sub_params(params, value):
    mandatoryList = []
    unsupportedList = []
    if value == 'SRIOVAdapterUpdate':
        mandatoryList += ['SubType']
        unsupportedList += ['IsQuickEvac', 'DestinationManagedSystem', 'LeavePartitionInTarget', 'VIOSName', 'ResourceType',
                            'IOAdapterUpdate', 'Id', 'Device', 'Repository', 'hmc_host', 'hmc_auth', 'UpdateType',
                            'system_name', 'IsDestruptive']

        if params.get('ALL') and params.get('AdapterID'):
            raise ParameterError("Parameter ALL and AdapterID are mutually exculsive")

        if not (params.get('ALL') or params.get('AdapterID')):
            raise ParameterError("either ALL or AdapterID parameter is required")

    if value == 'IOAdapterUpdate':
        mandatoryList += ['Repository']
        unsupportedList += ['IsQuickEvac', 'DestinationManagedSystem', 'LeavePartitionInTarget', 'VIOSName', 'ResourceType',
                            'IOAdapterUpdate', 'hmc_host', 'hmc_auth', 'UpdateType', 'system_name', 'IsDestruptive']

        if params.get('ALL'):
            if params.get('Id') or params.get('Device'):
                raise ParameterError("'ALL' is mutually exclusive with 'Id' and 'Device'.")
        else:
            mandatoryList += ['Id', 'Device']
    collate = []
    for eachUnsupported in unsupportedList:
        if params.get(eachUnsupported):
            collate.append(eachUnsupported)

    if collate:
        if len(collate) == 1:
            raise ParameterError(f"unsupported parameter for {value}: {(collate[0])}")
        else:
            raise ParameterError(f"unsupported parameters for {value}: {(','.join(collate))}")

    collate = []
    for eachMandatory in mandatoryList:
        if not params.get(eachMandatory):
            collate.append(eachMandatory)

    if collate:
        if len(collate) == 1:
            raise ParameterError(f"mandatory parameter {(collate[0])} is missing for {value}")
        else:
            raise ParameterError(f"mandatory parameters {(','.join(collate))} are missing for {value}")


def validate_parameters(params):

    mandatoryList = ['hmc_host', 'hmc_auth', 'system_name', 'ParameterValue']
    unsupportedList = ['IsQuickEvac', 'DestinationManagedSystem', 'LeavePartitionInTarget', 'VIOSName', 'ResourceType',
                       'IOAdapterUpdate', 'Id', 'Device', 'Repository', 'AdapterID', 'SubType', 'UpdateType', 'ALL',
                       'IsDestruptive']

    collate = []
    for eachUnsupported in unsupportedList:
        if params.get(eachUnsupported):
            collate.append(eachUnsupported)

    if collate:
        if len(collate) == 1:
            raise ParameterError("unsupported parameter: %s" % (collate[0]))
        else:
            raise ParameterError("unsupported parameters: %s" % (','.join(collate)))

    collate = []
    for eachMandatory in mandatoryList:
        if not params.get(eachMandatory):
            collate.append(eachMandatory)
    if collate:
        if len(collate) == 1:
            raise ParameterError("mandatory parameter '%s' is missing" % (collate[0]))
        else:
            raise ParameterError("mandatory parameters '%s' are missing" % (','.join(collate)))

    param_val = params.get('ParameterValue', {})

    if not param_val:
        raise ParameterError('Missing parameter ParameterValue')

    sfw_update = param_val.get('SystemFirmwareUpdate', {})
    if sfw_update:
        mandatoryList = ['UpdateType', 'UpdateOrder']
        unsupportedList = ['IsQuickEvac', 'DestinationManagedSystem', 'LeavePartitionInTarget', 'VIOSName',
                           'IOAdapterUpdate', 'Id', 'Device', 'Repository', 'hmc_host', 'hmc_auth', 'AdapterID',
                           'SubType', 'system_name']
        UpdateType = sfw_update.get('UpdateType', {})
        sriov_updates = sfw_update.get('SRIOVAdapterUpdate', {})
        resourceType = sfw_update.get('ResourceType', {})

        if UpdateType:
            if UpdateType.lower() == 'noupdate' and not sriov_updates:
                raise ParameterError("Missing Parameter SRIOVAdapterUpdate for SystemFirmwareUpdate")
            elif UpdateType.lower() in ['update', 'upgrade'] and sriov_updates:
                raise ParameterError(f"Invalid combination: SRIOVAdapterUpdate is not allowed with UpdateType = '{UpdateType}")

            if UpdateType.lower() in ['update', 'upgrade'] and not resourceType:
                raise ParameterError(f"Required Parameter ResourceType for updateType = {UpdateType}")
            elif UpdateType.lower() == 'noupdate':
                if resourceType:
                    raise ParameterError(f"Unsupported Parameter ResourceType for for SystemFirmwareUpdate when updateType = {UpdateType}")
                if sfw_update.get('Level') != 'latest':
                    raise ParameterError(f"Parameter 'Level' is not supported for SystemFirmwareUpdate when UpdateType = {UpdateType}")
                if sfw_update.get('Level') == 'latest':
                    sfw_update['Level'] = None
        if sriov_updates:
            for adapter in sriov_updates:
                validate_sub_params(adapter, 'SRIOVAdapterUpdate')

        collate = []
        for eachMandatory in mandatoryList:
            if not sfw_update.get(eachMandatory):
                collate.append(eachMandatory)
        if collate:
            if len(collate) == 1:
                raise ParameterError(f"mandatory parameter {(collate[0])} is missing for SystemFirmwareUpdate")
            else:
                raise ParameterError(f"mandatory parameters {(','.join(collate))} are missing for SystemFirmwareUpdate")

        collate = []
        for eachUnsupported in unsupportedList:
            if sfw_update.get(eachUnsupported):
                collate.append(eachUnsupported)

            if collate:
                if len(collate) == 1:
                    raise ParameterError("unsupported parameter for SystemFirmwareUpdate: %s" % (collate[0]))
                else:
                    raise ParameterError("unsupported parameters for SystemFirmwareUpdate: %s" % (','.join(collate)))

    vios_updates = param_val.get('VIOSUpdate', [])
    if vios_updates:
        mandatoryList = ['UpdateType', 'VIOSName', 'UpdateOrder']
        unsupportedList = ['IsQuickEvac', 'DestinationManagedSystem', 'LeavePartitionInTarget', 'Id', 'Device', 'Repository',
                           'SRIOVAdapterUpdate', 'hmc_host', 'hmc_auth', 'AdapterID', 'SubType', 'system_name', 'IsDestruptive']
        for vios in vios_updates:
            collate = []
            for eachUnsupported in unsupportedList:
                if vios.get(eachUnsupported):
                    collate.append(eachUnsupported)

            if vios.get('UpdateType').lower() == 'noupdate':
                if vios.get('ResourceType'):
                    raise ParameterError("Parameter 'ResourceType' is not supported for ViosUpdate when UpdateType is 'NoUpdate'")
                if vios.get('Level') != 'latest':
                    raise ParameterError("Parameter 'Level' is not supported for ViosUpdate when UpdateType is 'NoUpdate'")
                if vios.get('Level') == 'latest':
                    vios['Level'] = None
            else:
                mandatoryList += ['ResourceType']

            io_adapters = vios.get('IOAdapterUpdate', [])
            if io_adapters:
                for io in io_adapters:
                    validate_sub_params(io, 'IOAdapterUpdate')

            if collate:
                if len(collate) == 1:
                    raise ParameterError("unsupported parameter for VIOSUpdate: %s" % (collate[0]))
                else:
                    raise ParameterError("unsupported parameters for VIOSUpdate: %s" % (','.join(collate)))

            collate = []
            for eachMandatory in mandatoryList:
                if not vios.get(eachMandatory):
                    collate.append(eachMandatory)
            if collate:
                if len(collate) == 1:
                    raise ParameterError("mandatory parameter '%s' is missing for VIOSUpdate" % (collate[0]))
                else:
                    raise ParameterError("mandatory parameters '%s' are missing for VIOSUpdate" % (','.join(collate)))

    partition_migs = param_val.get('PartitionMigration', [])
    if partition_migs:
        if not (sfw_update or vios_updates):
            raise ParameterError("Invalid usage: 'PartitionMigration' must be specified along with either 'VIOSUpdate' or 'SystemFirmwareUpdate'")
        mandatoryList = ['IsQuickEvac', 'DestinationManagedSystem']
        unsupportedList = ['UpdateType', 'UpdateOrder', 'VIOSName', 'ResourceType', 'IOAdapterUpdate', 'Id', 'Device', 'Repository',
                           'SRIOVAdapterUpdate', 'hmc_host', 'hmc_auth', 'AdapterID', 'SubType', 'system_name', 'IsDestruptive', 'Level']
        for migs in partition_migs:
            collate = []
            for eachUnsupported in unsupportedList:
                if migs.get(eachUnsupported):
                    collate.append(eachUnsupported)
            if collate:
                if len(collate) == 1:
                    raise ParameterError("unsupported parameter for PartitionMigration : %s" % (collate[0]))
                else:
                    raise ParameterError("unsupported parameters for PartitionMigration: %s" % (','.join(collate)))

            collate = []
            for eachMandatory in mandatoryList:
                if not migs.get(eachMandatory):
                    collate.append(eachMandatory)
            if collate:
                if len(collate) == 1:
                    raise ParameterError("mandatory parameter '%s' is missing for PartitionMigration" % (collate[0]))
                else:
                    raise ParameterError("mandatory parameters '%s' are missing for PartitionMigration" % (','.join(collate)))


def fail_with_logoff(module, rest_conn, msg):
    try:
        rest_conn.logoff()
    except Exception as logoff_error:
        error_msg = parse_error_response(logoff_error)
        module.warn(msg=error_msg)
    module.fail_json(msg=msg)


def cleanup_entries(data, sriov=None, io=None):
    Adapter_subtype_map = {
        'Minimal': 'adapterdriver',
        'Full': 'adapterdriver,adapter'
    }
    if sriov:
        sriov_adapters = data["SystemFirmwareUpdate"].get("SRIOVAdapterUpdate", [])
        if sriov_adapters:
            subtype = sriov_adapters[0].get("SubType", "adapterdriver")
            data['SystemFirmwareUpdate']['SRIOVAdapterUpdate'] = [
                {
                    "AdapterID": str(adapter_id),
                    "SubType": subtype
                } for adapter_id in sriov
            ]
    if io:
        viosUpdates = data['VIOSUpdate']
        for vios in viosUpdates:
            ioAdapters = vios.get("IOAdapterUpdate")
            if ioAdapters and ioAdapters[0].get('ALL'):
                repo = ioAdapters[0].get("Repository", "")
                vios["IOAdapterUpdate"] = [
                    {
                        "Id": adapter_id,
                        "Device": ",".join(devices),
                        "Repository": repo
                    }
                    for adapter_id, devices in io['IOAdapterUpdate'].items()
                ]

    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            if value is not None:
                # Recursively clean value
                cleaned_value = cleanup_entries(value)

                # If this is the SubType key, normalize it
                if key == "SubType" and isinstance(cleaned_value, str):
                    cleaned_value = Adapter_subtype_map.get(cleaned_value, cleaned_value)

                cleaned[key] = cleaned_value
        return cleaned

    elif isinstance(data, list):
        return [cleanup_entries(item) for item in data]

    else:
        return data


def platform_update(module):
    params = module.params
    try:
        validate_parameters(params)
    except Exception as e:
        module.fail_json(msg=str(e))
    hmc_host = params['hmc_host']
    hmc_user = params['hmc_auth']['username']
    password = params['hmc_auth']['password']
    system_name = params['system_name']
    attributes = params.get('ParameterValue')
    changed = False
    vios_updates = copy.deepcopy(attributes.get('VIOSUpdate'))
    all_io_updates = []
    available_adapter_id = []
    available_io_updates = {}
    if vios_updates:
        for entry in vios_updates:
            vios_name = entry.get("VIOSName")
            io_adapters = entry.get("IOAdapterUpdate")

            if isinstance(io_adapters, list):
                for adapter in entry["IOAdapterUpdate"]:
                    adapter["VIOSName"] = vios_name
                    all_io_updates.append(adapter)

    hmc_conn = HmcCliConnection(module, hmc_host, hmc_user, password)
    hmc = Hmc(hmc_conn)

    sys_list = (
        hmc_conn.execute("lssyscfg -r sys -F name").splitlines() + hmc_conn.execute("lssyscfg -r sys -F type_model*serial_num").splitlines()
    )
    if system_name not in sys_list:
        module.fail_json(msg="The managed system is not available in HMC")
    else:
        vios_list = list(hmc_conn.execute("lssyscfg -r lpar -m {0} -F name,state,lpar_id,rmc_state".format(system_name)).splitlines())
        if vios_updates:
            vios_names = [entry["VIOSName"] for entry in attributes.get("VIOSUpdate", [])]
            for vios in vios_names:
                vios_details = next((entry.split(',') for entry in vios_list if entry.split(',')[0] == vios), None)
                if vios_details:
                    if vios_details[3] == 'inactive':
                        module.fail_json(msg=f"The VIOS {vios} does not have an active RMC connection and cannot be updated at this time")
                    for io_update in all_io_updates:
                        if io_update.get("VIOSName") == vios:
                            io_update["vios_id"] = vios_details[2].zfill(3)
                else:
                    module.fail_json(msg=f"The VIOS {vios} is not available in HMC")

    if re.match(HmcConstants.MTMS_pattern, system_name):
        try:
            system_name = hmc.getSystemNameFromMTMS(system_name)
        except HmcError as on_system_error:
            return changed, repr(on_system_error), None

    try:
        rest_conn = HmcRestClient(hmc_host, hmc_user, password)
    except Exception as error:
        error_msg = parse_error_response(error)
        module.fail_json(msg=error_msg)

    try:
        system_uuid, _unused = rest_conn.getManagedSystem(system_name)
        if not system_uuid:
            fail_with_logoff(module, rest_conn, "Given system is not present")
    except (Exception, HmcError) as error:
        error_msg = parse_error_response(error)
        logger.debug("Line number: %d exception: %s", sys.exc_info()[2].tb_lineno, repr(error))
        fail_with_logoff(module, rest_conn, error_msg)

    try:
        sysfirm_update = attributes.get("SystemFirmwareUpdate", {})
        if sysfirm_update:
            status, result = rest_conn.LicReadinessCheck(system_uuid, system_name)
            if status == 'COMPLETED_OK':
                logger.info("System readiness check Passed")
            else:
                msg = "No message error provided"
                for param in result:
                    if param.get("ParameterName") == 'JOBRESULT_KEY_ERRORMSG':
                        msg = param.get('ParameterValue')
                        break
                error_msg = f'system {system_name} is not in ready state, therefore the system firmware cannot be updated, Msg: {msg}'
                fail_with_logoff(module, rest_conn, error_msg)
    except (Exception, HmcError) as error:
        error_msg = parse_error_response(error)
        logger.debug("Line number: %d exception: %s", sys.exc_info()[2].tb_lineno, repr(error))
        fail_with_logoff(module, rest_conn, error_msg)

    try:
        sysfirm_update = attributes.get("SystemFirmwareUpdate", {})
        if sysfirm_update:
            output = rest_conn.LicQueryLevel(system_uuid, system_name, type='sriov')
            if output.get('ParameterName'):
                error_msg = output.get('ParameterValue')
                fail_with_logoff(module, rest_conn, error_msg)
            sriov_update = sysfirm_update.get('SRIOVAdapterUpdate')
            if sriov_update:
                if 'No results' in output.get("SRIOVAdapterUpdate", {}).get("AdapterID"):
                    error_msg = f'No SRIOV Adapters are available for {system_name}'
                    fail_with_logoff(module, rest_conn, error_msg)

                for adapter in sriov_update:
                    if adapter.get('ALL'):
                        available_adapter_id = output.get("SRIOVAdapterUpdate", {}).get("AdapterID")
                    else:
                        adapter_id = adapter.get("AdapterID")
                        if int(adapter_id) not in output.get("SRIOVAdapterUpdate", {}).get("AdapterID"):
                            error_msg = f"SRIOVAdapter with ID {adapter_id} is not present for system {system_name}"
                            fail_with_logoff(module, rest_conn, error_msg)

        if all_io_updates:
            output = rest_conn.LicQueryLevel(system_uuid, system_name, type='io')
            if output.get('ParameterName'):
                error_msg = output.get('ParameterValue')
                fail_with_logoff(module, rest_conn, error_msg)

            for io_update in all_io_updates:
                if 'No results' in output.get("IOAdapterUpdate"):
                    error_msg = f"No IO Adapters are available for VIOS '{io_update.get('VIOSName')}'"
                    fail_with_logoff(module, rest_conn, error_msg)
                if io_update.get('ALL'):
                    vios_id = io_update.get('vios_id')
                    if output.get('IOAdapterUpdate', {}).get(vios_id, []):
                        available_io_updates = {'IOAdapterUpdate': {vios_id: output.get('IOAdapterUpdate', {}).get(vios_id, [])}}
                    else:
                        error_msg = f"No available I/O adapters found for VIOS {output.get('VIOSName')}"
                        fail_with_logoff(module, rest_conn, error_msg)
                else:
                    io_id = str(io_update.get('Id')).zfill(3)
                    if io_id != io_update.get('vios_id'):
                        error_msg = (
                            f"Adapter ID mismatch: VIOS {io_update.get('VIOSName')} has ID {io_update.get('vios_id')}, "
                            f"but Adapter ID is {io_id}."
                        )
                        fail_with_logoff(module, rest_conn, error_msg)
                    device = io_update.get('Device')
                    valid_devices = output.get('IOAdapterUpdate', {}).get(io_id, [])
                    if valid_devices:
                        if device not in valid_devices:
                            error_msg = (
                                f"Device '{device}' is not found under IO Adapter with ID '{io_update.get('Id')}' "
                                f"for VIOS '{io_update.get('VIOSName')}'."
                            )
                            fail_with_logoff(module, rest_conn, error_msg)
                    else:
                        error_msg = f"VIOS '{io_update.get('VIOSName')}' does not contain IO Adapter with ID '{io_update.get('Id')}'."
                        fail_with_logoff(module, rest_conn, error_msg)
    except (Exception, HmcError) as error:
        error_msg = parse_error_response(error)
        logger.debug("Line number: %d exception: %s", sys.exc_info()[2].tb_lineno, repr(error))
        fail_with_logoff(module, rest_conn, error_msg)

    try:
        needs_update = None
        if vios_updates:
            needs_update = any('update' == vios.get('UpdateType', '').lower() for vios in attributes.get("VIOSUpdate", []))
        if needs_update:
            console_uuid = rest_conn.getManagementConsole()
            for vios_info in attributes.get("VIOSUpdate", []):
                updateType = vios_info['UpdateType'].lower()
                if updateType in 'update':
                    vios_name = vios_info['VIOSName']
                    source_file = vios_info['ResourceType']
                    vios_level = vios_info['Level']
                    output = rest_conn.listViosUpdates(console_uuid, system_name, vios_name, source_file)
                    if output.strip() in ("[]", "", "None"):
                        error_msg = f"Update file for {vios_name} not found at the specified source location: {source_file}."
                        fail_with_logoff(module, rest_conn, error_msg)
                    elif vios_level != 'latest' and vios_level not in output:
                        error_msg = (
                            f"Update file {vios_level} for vios {vios_name} "
                            f"is not found at the specified source location: {source_file}."
                        )
                        fail_with_logoff(module, rest_conn, error_msg)
    except (Exception, HmcError) as error:
        error_msg = parse_error_response(error)
        logger.debug("Line number: %d exception: %s", sys.exc_info()[2].tb_lineno, repr(error))
        fail_with_logoff(module, rest_conn, error_msg)

    try:
        sysfirm_update = attributes.get('SystemFirmwareUpdate')
        if sysfirm_update:
            updateType = sysfirm_update.get('UpdateType').lower()
            if updateType in ['update', 'upgrade']:
                firm_level = sysfirm_update.get('Level')
                source_file = sysfirm_update.get('ResourceType').lower()
                output = rest_conn.LICQueryRepository(system_uuid, system_name, source_file,
                                                      type="sys", level=updateType)
                if "No results" in output.get('ParameterValue'):
                    error_msg = f"No {updateType.upper()} file found at the specified source: {source_file} for the resource: {system_name}."
                    fail_with_logoff(module, rest_conn, error_msg)
                if output.get('ParameterName') == 'JOBRESULT_KEY_ERRORMSG':
                    error_msg = (
                        f"No {updateType.upper()} file found at the specified source: {source_file} "
                        f"for the resource: {system_name} reason: {output.get('ParameterValue')}"
                    )
                elif firm_level != 'latest' and firm_level not in output:
                    error_msg = (
                        f"Update file {firm_level} for the resource {system_name} "
                        f"is not found at the specified source location: {source_file}."
                    )
                    fail_with_logoff(module, rest_conn, error_msg)
    except (Exception, HmcError) as error:
        error_msg = parse_error_response(error)
        logger.debug("Line number: %d exception: %s", sys.exc_info()[2].tb_lineno, repr(error))
        fail_with_logoff(module, rest_conn, error_msg)

    try:
        if all_io_updates:
            for io_update in all_io_updates:
                source_file = io_update.get('Repository').lower()
                vios_id = io_update.get('vios_id')
                output = rest_conn.LICQueryRepository(system_uuid, system_name, source_file)
                if available_io_updates:
                    adp_ids = vios_id
                else:
                    adp_ids = {io_update.get('Id')}
                if output.get('ParameterName') == 'JOBRESULT_KEY_ERRORMSG':
                    error_msg = f"Import operation failed for IO Adapter ID '{adp_ids}' on VIOS '{io_update.get('VIOSName')}': {output.get('ParameterValue')}"
                    fail_with_logoff(module, rest_conn, error_msg)
    except (Exception, HmcError) as error:
        error_msg = parse_error_response(error)
        logger.debug("Line number: %d exception: %s", sys.exc_info()[2].tb_lineno, repr(error))
        fail_with_logoff(module, rest_conn, error_msg)

    try:
        cleaned_data = cleanup_entries(attributes, sriov=available_adapter_id, io=available_io_updates)
        final_output = rest_conn.PlatformUpdate(system_uuid, cleaned_data)
    except (Exception, HmcError) as error:
        error_msg = parse_error_response(error)
        logger.debug("Line number: %d exception: %s", sys.exc_info()[2].tb_lineno, repr(error))
        fail_with_logoff(module, rest_conn, error_msg)

    finally:
        try:
            rest_conn.logoff()
        except Exception as logoff_error:
            error_msg = parse_error_response(logoff_error)
            module.warn(msg=error_msg)

    return True, final_output, None


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
        system_name=dict(type='str', required=True),
        ParameterValue=dict(
            type='dict',
            options=dict(
                SystemFirmwareUpdate=dict(
                    type='dict',
                    options=dict(
                        UpdateType=dict(type='str', choices=['NoUpdate', 'Update', 'Upgrade']),
                        UpdateOrder=dict(type='int'),
                        IsDestruptive=dict(type='bool'),
                        ResourceType=dict(type='str', choices=['IBMWebsite']),
                        Level=dict(type='str', default="latest"),
                        SRIOVAdapterUpdate=dict(
                            type='list',
                            elements='dict',
                            options=dict(
                                ALL=dict(type="bool"),
                                AdapterID=dict(type='str'),
                                SubType=dict(type='str', choices=['Minimal', 'Full'])
                            )
                        )
                    )
                ),
                PartitionMigration=dict(
                    type='list',
                    elements='dict',
                    options=dict(
                        IsQuickEvac=dict(type='bool'),
                        DestinationManagedSystem=dict(type='str'),
                        LeavePartitionInTarget=dict(type='bool')
                    )
                ),
                VIOSUpdate=dict(
                    type='list',
                    elements='dict',
                    options=dict(
                        UpdateType=dict(type='str', choices=['NoUpdate', 'Update']),
                        VIOSName=dict(type='str'),
                        UpdateOrder=dict(type='int'),
                        ResourceType=dict(type='str', choices=['IBMWebsite']),
                        Level=dict(type='str', default="latest"),
                        IOAdapterUpdate=dict(
                            type='list',
                            elements='dict',
                            options=dict(
                                ALL=dict(type='bool'),
                                Id=dict(type='str'),
                                Device=dict(type='str'),
                                Repository=dict(type='str', choices=['IBMWebsite'])
                            )
                        )
                    )
                )
            )
        )
    )

    module = AnsibleModule(
        argument_spec=module_args,
    )

    if module._verbosity >= 5:
        init_logger()

    if sys.version_info < (3, 0):
        py_ver = sys.version_info[0]
        raise ParameterError("Unsupported Python version {0}, supported python version is 3 and above".format(py_ver))

    changed, info, warning = platform_update(module)

    result = {}
    result['changed'] = changed
    if info:
        result['command_output'] = info

    if warning:
        result['warning'] = warning

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
