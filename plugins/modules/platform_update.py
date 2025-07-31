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
short_description: Performs consolidated system firmware, VIOS, SR-IOV, and I/O adapter updates, including partition migration.
notes:
  - The current version supports IBM Fix Central website as the update source .
  - Support for additional update sources will be added in future releases.
description:
    - This module allows updating System Firmware, VIOS, SR-IOV adapters, and I/O adapters either individually or through a single consolidated update flow.
    - This operations can be configured using I(platform_config) parameter.
    - It supports both 'DriverOnly' and 'Adapter' update strategies for SR-IOV adapters and allows updates from IBM Fix Central website when specified.
    - Supports defining the order in which updates are applied across components.
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
    platform_config:
        description:
            - Defines the configuration for the operation to be performed, such as system firmware updates
              (including SR-IOV adapter updates) or VIOS updates (including I/O adapter updates).
            - Also supports performing partition migrations.
            - This option applies changes to the HMC.
        required: false
        type: dict
        suboptions:
            system_firmware_update:
                description:
                    - System firmware update configuration.
                type: dict
                suboptions:
                    update_type:
                        description:
                            - Type of firmware update operation.
                            - 'C(NoUpdate): System firmware update is skipped, but SR-IOV adapter updates are still allowed'
                            - 'C(Update): Performs an update.'
                            - 'C(Upgrade): Performs an upgrade.'
                            - When set to C(Update) or C(Upgrade), the C(sriov_adapter_update) will be implicit.
                            - When set to C(NoUpdate), C(resource_type), and C(level) are not required.
                        type: str
                        choices: ['NoUpdate', 'Update', 'Upgrade']
                    update_order:
                        description:
                            - Optional order in which the update should be applied.
                        type: int
                    resource_type:
                        description:
                            - Specifies the source repository for the update image.
                            - currently only supports C(IBMWebsite).
                        type: str
                        choices: ['IBMWebsite']
                        default: 'IBMWebsite'
                    level:
                        description:
                            - Specifies the firmware version level to apply.
                            - If not provided, the latest available version will be used by default.
                        type: str
                        default: 'latest'
                    sriov_adapter_update:
                        description:
                            - List of SR-IOV adapter update configurations.
                            - This option must not be provided if C(update_type) is set to C(Update) or C(Upgrade)
                        type: list
                        elements: dict
                        suboptions:
                            all:
                                description:
                                    - Indicates whether the update should be applied to all adapters.
                                    - If set to C(true), the C(adapter_id) field is not required.
                                type: bool
                            adapter_id:
                                description:
                                    - ID of the specific adapter to be updated.
                                    - Required only when C(all) is not specified.
                                type: str
                            subtype:
                                description:
                                    - Specifies the level of update to apply.
                                    - C(DriverOnly) applies only the driver update.
                                    - C(Adapter) applies both the adapter firmware and driver updates.
                                type: str
                                choices: ['DriverOnly', 'Adapter']
            partition_migration:
                description:
                    - Configuration for migrating logical partitions.
                type: list
                elements: dict
                suboptions:
                    is_quick_evac:
                        description: Whether to enable quick evacuation.
                        type: bool
                    destination_managed_system:
                        description: Target managed system name.
                        type: str
                    leave_partition_in_target:
                        description: Whether to keep the partition in the target after platform update.
                        type: bool
            vios_update:
                description:
                    - Configuration for updating Virtual I/O Servers.
                type: list
                elements: dict
                suboptions:
                    update_type:
                        description:
                            - Specifies the type of VIOS update to be performed.
                            - 'C(NoUpdate): No update will be applied to VIOS, but I/O adapter updates are still allowed'
                            - 'C(Update): Triggers a VIOS update using the provided configuration.'
                            - When set to C(NoUpdate), the fields C(resource_type) and C(level) are not required.
                        type: str
                        choices: ['NoUpdate', 'Update']
                    vios_name:
                        description: Name of the VIOS partition.
                        type: str
                    update_order:
                        description: Priority/order of update among multiple VIOS.
                        type: int
                    resource_type:
                        description:
                            - Specifies the source repository for the update image.
                            - Currentlt only supports C(IBMWebsite).
                        type: str
                        choices: ['IBMWebsite']
                        default: 'IBMWebsite'
                    level:
                        description:
                            - Specifies the VIOS version level to apply.
                            - If not provided, the latest available version will be used by default.
                        type: str
                        default: 'latest'
                    io_adapter_update:
                        description: List of I/O adapters to update during VIOS update.
                        type: list
                        elements: dict
                        suboptions:
                            all:
                                description:
                                    - Indicates whether all I/O adapters should be updated.
                                    - If set to C(true), the C(device) field is not required
                                type: bool
                            device:
                                description:
                                    - List of I/O adapter device names to be updated.
                                    - Specify one or more device names as a list (e.g., C(['ent0', 'fcs0'])).
                                    - Required only when C(all) is not specified.
                                type: list
                                elements: str
                            repository:
                                description:
                                    - Specifies the source repository for the update image.
                                    - Currentlt only supports C(IBMWebsite).
                                type: str
                                choices: ['IBMWebsite']
                                default: 'IBMWebsite'
    state:
        description:
            - It gathers and returns information about available SR-IOV adapters, Virtual I/O Servers (VIOS), and I/O adapters without making any changes.
        type: str
        choices: ['facts']
'''

EXAMPLES = '''
- name: Update a SR-IOV adapters (DriverOnly) using IBM Fix Central
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    platform_config:
      system_firmware_update:
        update_type: NoUpdate
        update_order: 1
        sriov_adapter_update:
          - adapter_id: "ent0"
            subtype: DriverOnly

- name: Update all SR-IOV adapters (Adapter) using IBM Fix Central (No Firware Update)
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    platform_config:
      system_firmware_update:
        update_type: NoUpdate
        update_order: 1
        sriov_adapter_update:
          - all: true
            subtype: Adapter

- name: Perform a System Firmware update using default level
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    platform_config:
      system_firmware_update:
        update_type: Update
        update_order: 1

- name: Perform a System Firmware update using specified level (level 12)
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    platform_config:
      system_firmware_update:
        update_type: Update
        update_order: 1
        level: 12

- name: Migrate a partition to a different managed system
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    platform_config:
      system_firmware_update:
        update_type: Update
        update_order: 1
        resource_type: IBMWebsite
      partition_migration:
        - is_quick_evac: true
          destination_managed_system: "p920_system"
          leave_partition_in_target: false

- name: Update VIOS to latest available level from IBM Fix Central
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    platform_config:
      vios_update:
        - update_type: Update
          vios_name: "vios1"
          update_order: 1
          resource_type: IBMWebsite

- name: Update selected I/O adapters only (no VIOS update)
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    platform_config:
      vios_update:
        - update_type: NoUpdate
          vios_name: "vios1"
          update_order: 1
          resource_type: IBMWebsite
          io_adapter_update:
            - device:
                - "device 1"
                - "device 2"
              repository: IBMWebsite

- name: Update VIOS to specific level and all I/O adapters from IBM Fix Central
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    platform_config:
      vios_update:
        - update_type: NoUpdate
          vios_name: "vios1"
          update_order: 1
          resource_type: IBMWebsite
          level: 13
          io_adapter_update:
            - all: true
              repository: IBMWebsite

- name: Update multiple VIOS instances to the latest available level from IBM Fix Central
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    platform_config:
      vios_update:
        - update_type: Update
          vios_name: "vios1"
          update_order: 1
          resource_type: IBMWebsite
        - update_type: Update
          vios_name: "vios2"
          update_order: 2
          resource_type: IBMWebsite

- name: Facts
  platform_update:
    hmc_host: "10.0.0.10"
    hmc_auth:
      username: "hscroot"
      password: "hmcpass"
    system_name: "p910_system"
    state: facts
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
LOG_FILENAME = "/tmp/ansible_power_hmc.log"
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
import json


before_update_level = {}
after_update_level = {}


def init_logger():
    logging.basicConfig(
        filename=LOG_FILENAME,
        format='[%(asctime)s] %(levelname)s: [%(funcName)s] %(message)s',
        level=logging.DEBUG)


def validate_sub_params(params, value):
    mandatoryList = []
    unsupportedList = []
    if value == 'sriov_adapter_update':
        mandatoryList += ['subtype']
        unsupportedList += ['is_quick_evac', 'destination_managed_system', 'leave_partition_in_target', 'vios_name', 'resource_type',
                            'io_adapter_update', 'device', 'repository', 'hmc_host', 'hmc_auth', 'update_type',
                            'system_name', 'vios_update']

        if params.get('all') and params.get('adapter_id'):
            raise ParameterError("Parameter all and adapter_id are mutually exculsive")

        if not (params.get('all') or params.get('adapter_id')):
            raise ParameterError("either all or adapter_id parameter is required")

    if value == 'io_adapter_update':
        unsupportedList += ['is_quick_evac', 'destination_managed_system', 'leave_partition_in_target', 'vios_name', 'resource_type',
                            'io_adapter_update', 'hmc_host', 'hmc_auth', 'update_type', 'system_name', 'vios_update']

        if params.get('all'):
            if params.get('device'):
                raise ParameterError("'all' is mutually exclusive with 'device'.")
        else:
            mandatoryList += ['device']
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
    def check_params(param_dict, mandatory, unsupported, context=''):
        missing = [key for key in mandatory if not param_dict.get(key)]
        if missing:
            raise ParameterError(
                f"mandatory parameter{'s' if len(missing) > 1 else ''} "
                f"{'[' + ', '.join(missing) + ']'} {'are' if len(missing) > 1 else 'is'} missing"
                + (f" for {context}" if context else '')
            )

        invalid = [key for key in unsupported if param_dict.get(key)]
        if invalid:
            raise ParameterError(
                f"unsupported parameter{'s' if len(invalid) > 1 else ''} "
                f"{'[' + ', '.join(invalid) + ']'}"
                + (f" for {context}" if context else '')
            )

    def validate_sfw_update(sfw_update):
        mandatory = ['update_type', 'update_order']
        unsupported = [
            'is_quick_evac', 'destination_managed_system', 'leave_partition_in_target', 'vios_name',
            'io_adapter_update', 'id', 'device', 'repository', 'hmc_host', 'hmc_auth', 'adapter_id',
            'subtype', 'system_name', 'vios_update'
        ]
        update_type = sfw_update.get('update_type', '').lower()
        sriov_updates = sfw_update.get('sriov_adapter_update', [])
        resource_type = sfw_update.get('resource_type')

        if update_type == 'noupdate':
            if not sriov_updates:
                raise ParameterError("Missing parameter sriov_adapter_update for system_firmware_update")
            if resource_type:
                sfw_update['resource_type'] = None
            if sfw_update.get('level') != 'latest':
                raise ParameterError("Parameter 'level' is not supported for system_firmware_update when update_type = 'noupdate'")
            sfw_update['level'] = None
        elif update_type in ['update', 'upgrade']:
            if sriov_updates:
                raise ParameterError(f"Invalid combination: sriov_adapter_update is not allowed with update_type = '{update_type}'")

        if sriov_updates:
            for adapter in sriov_updates:
                validate_sub_params(adapter, 'sriov_adapter_update')

        check_params(sfw_update, mandatory, unsupported, 'system_firmware_update')

    def validate_vios_update(vios_updates):
        for vios in vios_updates:
            mandatory = ['update_type', 'vios_name', 'update_order']
            unsupported = [
                'is_quick_evac', 'destination_managed_system', 'leave_partition_in_target', 'device',
                'repository', 'sriov_adapter_update', 'hmc_host', 'hmc_auth', 'adapter_id', 'subtype',
                'system_name'
            ]
            if vios.get('update_type', '').lower() != 'noupdate':
                mandatory.append('resource_type')
            else:
                if vios.get('resource_type'):
                    vios['resource_type'] = None
                if vios.get('level') != 'latest':
                    raise ParameterError("Parameter 'level' is not supported for vios_update when update_type = 'noupdate'")
                vios['level'] = None

            io_adapters = vios.get('io_adapter_update', [])
            if io_adapters:
                for adapter in io_adapters:
                    validate_sub_params(adapter, 'io_adapter_update')

            check_params(vios, mandatory, unsupported, 'vios_update')

    def validate_partition_migration(partition_migs):
        mandatory = ['is_quick_evac', 'destination_managed_system']
        unsupported = [
            'update_type', 'update_order', 'vios_name', 'resource_type', 'io_adapter_update',
            'device', 'repository', 'sriov_adapter_update', 'hmc_host', 'hmc_auth', 'adapter_id',
            'subtype', 'system_name', 'level', 'vios_update'
        ]
        for mig in partition_migs:
            check_params(mig, mandatory, unsupported, 'partition_migration')

    if params.get('state') and params.get('platform_config'):
        raise ParameterError("Invalid parameter combination: 'state' and 'platform_config' cannot be used together. Please provide only one of them.")
    elif not (params.get('state') or params.get('platform_config')):
        raise ParameterError("Missing required parameter: Please provide either 'state' or 'platform_config'.")
    if params.get('state'):
        mandatory = ['hmc_host', 'hmc_auth', 'system_name']
        unsupported = [
            'is_quick_evac', 'destination_managed_system', 'leave_partition_in_target', 'vios_name',
            'resource_type', 'io_adapter_update', 'id', 'device', 'repository', 'adapter_id',
            'subtype', 'update_type', 'all', 'platform_config', 'vios_update',
        ]
        check_params(params, mandatory, unsupported)
    else:
        mandatory = ['hmc_host', 'hmc_auth', 'system_name', 'platform_config']
        unsupported = [
            'is_quick_evac', 'destination_managed_system', 'leave_partition_in_target', 'vios_name',
            'resource_type', 'io_adapter_update', 'id', 'device', 'repository', 'adapter_id',
            'subtype', 'update_type', 'all', 'vios_update'
        ]
        check_params(params, mandatory, unsupported)

        platform_config = params.get('platform_config', {})
        if not platform_config:
            raise ParameterError("Missing parameter 'platform_config'")

        sfw_update = platform_config.get('system_firmware_update')
        if sfw_update:
            validate_sfw_update(sfw_update)

        vios_updates = platform_config.get('vios_update', [])
        if vios_updates:
            validate_vios_update(vios_updates)

        partition_migs = platform_config.get('partition_migration', [])
        if partition_migs:
            if not (sfw_update or vios_updates):
                raise ParameterError("Invalid usage: 'partition_migration' must be specified along with either 'vios_update' or 'system_firmware_update'")
            validate_partition_migration(partition_migs)


def cleanup_entries(data, sriov=None, io=None):
    Adapter_subtype_map = {
        'DriverOnly': 'adapterdriver',
        'Adapter': 'adapterdriver,adapter'
    }
    if sriov:
        sriov_adapters = data["system_firmware_update"].get("sriov_adapter_update", [])
        if sriov_adapters:
            subtype = sriov_adapters[0].get("subtype", "adapterdriver")
            data['system_firmware_update']['sriov_adapter_update'] = [
                {
                    "AdapterID": str(adapter_id),
                    "SubType": subtype
                } for adapter_id in sriov
            ]
    if io:
        viosUpdates = data['vios_update']
        if viosUpdates:
            for vios in viosUpdates:
                ioAdapters = vios.get("io_adapter_update")
                if ioAdapters and ioAdapters[0].get('all'):
                    repo = ioAdapters[0].get("repository", "")
                    vios["io_adapter_update"] = [
                        {
                            "Id": adapter_id,
                            "Device": ",".join(devices),
                            "Repository": repo
                        }
                        for adapter_id, devices in io['IOAdapterUpdate'].items()
                    ]
                elif ioAdapters:
                    vios["io_adapter_update"] = [
                        {
                            "Id": adapter.get("Id", ""),
                            "Device": ",".join(adapter.get("device", [])),
                            "Repository": adapter.get("repository")
                        }
                        for adapter in ioAdapters
                    ]

    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            if value is not None:
                cleaned_value = cleanup_entries(value)

                if key in ["subtype", "SubType"] and isinstance(cleaned_value, str):
                    cleaned_value = Adapter_subtype_map.get(cleaned_value, cleaned_value)

                cleaned[key] = cleaned_value
        return cleaned

    elif isinstance(data, list):
        return [cleanup_entries(item) for item in data]

    else:
        return data


def map_entries(data):
    config_map = {
        "vios_update": "VIOSUpdate",
        "io_adapter_update": "IOAdapterUpdate",
        "device": "Device",
        "repository": "Repository",
        "update_order": "UpdateOrder",
        "vios_name": "VIOSName",
        "update_type": "UpdateType",
        "system_firmware_update": "SystemFirmwareUpdate",
        "sriov_adapter_update": "SRIOVAdapterUpdate",
        "adapter_id": "AdapterID",
        "subtype": "SubType",
        "partition_migration": "PartitionMigration",
        "is_quick_evac": "IsQuickEvac",
        "destination_managed_system": "DestinationManagedSystem",
        "leave_partition_in_target": "LeavePartitionInTarget",
        "resource_type": "ResourceType",
        "name": "Name",
        "level": "Level",
        "all": "ALL"
    }

    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            new_key = config_map.get(k, k)
            new_dict[new_key] = map_entries(v)
        return new_dict
    elif isinstance(data, list):
        return [map_entries(item) for item in data]
    else:
        return data


def check_current_level(hmc_conn, hmc, data, system):
    result = {
        "firmware_level": None,
        "sriov_levels": [],
        "io_adapter_levels": [],
        "vios_versions": []
    }
    try:
        sysfw = data.get("SystemFirmwareUpdate")
        if sysfw:
            update_type = sysfw.get("UpdateType")
            if update_type and update_type not in ("NoUpdate", ""):
                try:
                    result["firmware_level"] = hmc.get_firmware_level(system)
                except Exception as e:
                    logger.error("Failed to get firmware level for %s: %s", system, e)

            sriov_updates = sysfw.get("SRIOVAdapterUpdate")
            if sriov_updates and isinstance(sriov_updates, list):
                for sriov in sriov_updates:
                    adapter_id = sriov.get("AdapterID")
                    if adapter_id:
                        try:
                            sriov_cmd = f"lslic -t sriov -m {system} -F adapter_id,active_adapter_driver_level,active_adapter_level"
                            sriov_raw = hmc_conn.execute(sriov_cmd)
                            for line in sriov_raw.strip().splitlines():
                                if line.startswith(f"{adapter_id},"):
                                    parts = line.split(",")
                                    if len(parts) == 3:
                                        result["sriov_levels"].append({
                                            "adapter_id": parts[0],
                                            "driver_level": parts[1],
                                            "adapter_level": parts[2]
                                        })
                        except Exception as e:
                            logger.error("Failed to get SRIOV adapter level for %s: %s", adapter_id, e)

    except Exception as e:
        logger.error("Error in SystemFirmwareUpdate parsing: %s", e)

    try:
        vios_updates = data.get("VIOSUpdate")
        if vios_updates and isinstance(vios_updates, list):
            for vios in vios_updates:
                try:
                    update_type = vios.get("UpdateType")
                    vios_name = vios.get("VIOSName")

                    if update_type and update_type not in ("NoUpdate", "") and vios_name:
                        try:
                            lpar_cmd = f"lssyscfg -r lpar -m {system} -F name,os_version"
                            lpar_raw = hmc_conn.execute(lpar_cmd)
                            for line in lpar_raw.strip().splitlines():
                                if line.startswith(f"{vios_name},"):
                                    name, os_version = line.split(",", 1)
                                    result["vios_versions"].append({
                                        "vios_name": name,
                                        "os_version": os_version
                                    })
                        except Exception as e:
                            logger.error("Failed to get OS version for VIOS %s: %s", vios_name, e)

                    io_updates = vios.get("IOAdapterUpdate")
                    if io_updates and isinstance(io_updates, list):
                        for io in io_updates:
                            try:
                                adapter_id = io.get("Id")
                                if adapter_id:
                                    io_cmd = f"lslic -t io -m {system} -F device,current_level"
                                    io_raw = hmc_conn.execute(io_cmd)
                                    for line in io_raw.strip().splitlines():
                                        if line.startswith(f"{adapter_id},"):
                                            device, current_level = line.split(",", 1)
                                            result["io_adapter_levels"].append({
                                                "device": device,
                                                "current_level": current_level
                                            })
                            except Exception as e:
                                logger.error("Failed to get IO adapter level for %s: %s", adapter_id, e)
                except Exception as e:
                    logger.error("Error while processing individual VIOS update entry: %s", e)
    except Exception as e:
        logger.error("Error in VIOSUpdate parsing: %s", e)

    return result


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
    attributes = params.get('platform_config')
    changed = False
    vios_updates = copy.deepcopy(attributes.get('vios_update'))
    all_io_updates = []
    available_adapter_id = []
    available_io_updates = {"IOAdapterUpdate": {}}
    global before_update_level, after_update_level
    if vios_updates:
        for entry in vios_updates:
            vios_name = entry.get("vios_name")
            io_adapters = entry.get("io_adapter_update")

            if isinstance(io_adapters, list):
                for adapter in entry["io_adapter_update"]:
                    adapter["vios_name"] = vios_name
                    all_io_updates.append(adapter)

    hmc_conn = HmcCliConnection(module, hmc_host, hmc_user, password)
    hmc = Hmc(hmc_conn)

    sys_list = (
        hmc.list_all_managed_system_details(config_F="name") + hmc.list_all_managed_system_details(config_F="type_model*serial_num")
    )
    if not sys_list:
        module.fail_json(msg="No managed systems found in HMC")
    elif system_name not in [v for d in sys_list for v in d.values()]:
        module.fail_json(msg="The managed system is not available in HMC")
    else:
        vios_list = list(hmc_conn.execute("lssyscfg -r lpar -m {0} -F name,state,lpar_id,rmc_state".format(system_name)).splitlines())
        if vios_updates:
            vios_names = [entry["vios_name"] for entry in attributes.get("vios_update", [])]
            for vios in vios_names:
                vios_details = next((entry.split(',') for entry in vios_list if entry.split(',')[0] == vios), None)
                if vios_details:
                    if vios_details[3] == 'inactive':
                        module.fail_json(msg=f"The VIOS {vios} does not have an active RMC connection and cannot be updated at this time")
                    for io_update in all_io_updates:
                        if io_update.get("vios_name") == vios:
                            io_update["vios_id"] = vios_details[2].zfill(3)
                    if attributes.get('vios_update'):
                        for entry in attributes.get('vios_update'):
                            io_adapters = entry.get("io_adapter_update")
                            if io_adapters:
                                for adapter in io_adapters:
                                    adapter["Id"] = vios_details[2].zfill(3)
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
            module.fail_json(msg="Given system is not present")

        # System Readiness Check
        sysfirm_update = attributes.get("system_firmware_update", {})
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
                module.fail_json(msg=error_msg)

        # SRIOV Adapters Avaiability check
        sysfirm_update = attributes.get("system_firmware_update", {})
        if sysfirm_update:
            output = rest_conn.LicQueryLevel(system_uuid, system_name, type='sriov')
            if output.get('ParameterName'):
                error_msg = output.get('ParameterValue')
                module.fail_json(msg=error_msg)
            sriov_update = sysfirm_update.get('sriov_adapter_update')
            if sriov_update:
                if 'No results' in output.get("SRIOVAdapterUpdate", {}).get("AdapterID"):
                    error_msg = f'No SRIOV Adapters are available for {system_name}'
                    module.fail_json(msg=error_msg)

                for adapter in sriov_update:
                    if adapter.get('all'):
                        available_adapter_id = output.get("SRIOVAdapterUpdate", {}).get("AdapterID")
                    else:
                        adapter_id = adapter.get("adapter_id")
                        if int(adapter_id) not in output.get("SRIOVAdapterUpdate", {}).get("AdapterID"):
                            error_msg = f"SRIOVAdapter with ID {adapter_id} is not present for system {system_name}"
                            module.fail_json(msg=error_msg)

        # IO Adapter Avaiabillty check
        if all_io_updates:
            output = rest_conn.LicQueryLevel(system_uuid, system_name, type='io')
            if output.get('ParameterName'):
                error_msg = output.get('ParameterValue')
                module.fail_json(msg=error_msg)

            for io_update in all_io_updates:
                if 'No results' in output.get("IOAdapterUpdate"):
                    error_msg = f"No IO Adapters are available for VIOS '{io_update.get('vios_name')}'"
                    module.fail_json(msg=error_msg)
                if io_update.get('all'):
                    vios_id = io_update.get('vios_id')
                    if output.get('IOAdapterUpdate', {}).get(vios_id, []):
                        available_io_updates = {'IOAdapterUpdate': {vios_id: output.get('IOAdapterUpdate', {}).get(vios_id, [])}}
                    else:
                        error_msg = f"No available I/O adapters found for VIOS {output.get('vios_name')}"
                        module.fail_json(msg=error_msg)
                else:
                    io_id = str(io_update.get('vios_id')).zfill(3)
                    devices = io_update.get('device')
                    valid_devices = output.get('IOAdapterUpdate', {}).get(io_id, [])
                    if valid_devices:
                        for device in devices:
                            if device not in valid_devices:
                                error_msg = (
                                    f"Device '{device}' is not found under IO Adapter with ID '{io_update.get('vios_id')}' "
                                    f"for VIOS '{io_update.get('vios_name')}'."
                                )
                                module.fail_json(msg=error_msg)
                    else:
                        error_msg = f"VIOS '{io_update.get('vios_name')}' does not contain IO Adapter with ID '{io_update.get('vios_id')}'."
                        module.fail_json(msg=error_msg)

        # Vios Update Check
        needs_update = None
        if vios_updates:
            needs_update = any('update' == vios.get('update_type', '').lower() for vios in attributes.get("vios_update", []))
        if needs_update:
            console_uuid = rest_conn.getManagementConsole()
            for vios_info in attributes.get("vios_update", []):
                updateType = vios_info['update_type'].lower()
                if updateType in 'update':
                    vios_name = vios_info['vios_name']
                    source_file = vios_info['resource_type']
                    vios_level = vios_info['level']
                    output = rest_conn.listViosUpdates(console_uuid, system_name, vios_name, source_file)
                    if output.strip() in ("[]", "", "None"):
                        error_msg = f"Update file for {vios_name} not found at the specified source location: {source_file}."
                        module.fail_json(msg=error_msg)
                    elif vios_level != 'latest' and vios_level not in output:
                        error_msg = (
                            f"Update file {vios_level} for vios {vios_name} "
                            f"is not found at the specified source location: {source_file}."
                        )
                        module.fail_json(msg=error_msg)

        # System Firmware Update Check
        sysfirm_update = attributes.get('system_firmware_update')
        if sysfirm_update:
            updateType = sysfirm_update.get('update_type').lower()
            if updateType in ['update', 'upgrade']:
                firm_level = sysfirm_update.get('level')
                source_file = sysfirm_update.get('resource_type').lower()
                output = rest_conn.LICQueryRepository(system_uuid, system_name, source_file,
                                                      type="sys", level=updateType)
                if "No results" in output.get('ParameterValue'):
                    error_msg = f"No {updateType.upper()} file found at the specified source: {source_file} for the resource: {system_name}."
                    module.fail_json(msg=error_msg)
                if output.get('ParameterName') == 'JOBRESULT_KEY_ERRORMSG':
                    error_msg = (
                        f"No {updateType.upper()} file found at the specified source: {source_file} "
                        f"for the resource: {system_name} reason: {output.get('ParameterValue')}"
                    )
                    module.fail_json(msg=error_msg)
                elif firm_level != 'latest' and firm_level not in output:
                    error_msg = (
                        f"Update file {firm_level} for the resource {system_name} "
                        f"is not found at the specified source location: {source_file}."
                    )
                    module.fail_json(msg=error_msg)
                else:
                    if output.get('ParameterValue'):
                        output = output.get('ParameterValue')
                        lines = output.split("\n")
                        for line in lines:
                            parts = line.split(",")
                            if firm_level != 'latest' and firm_level == parts[2]:
                                sysfirm_update['IsDestruptive'] = True
                                break

        # IO Adapter Update check
        if all_io_updates:
            for io_update in all_io_updates:
                source_file = io_update.get('repository').lower()
                vios_id = io_update.get('vios_id')
                output = rest_conn.LICQueryRepository(system_uuid, system_name, source_file)
                if available_io_updates:
                    adp_ids = vios_id
                else:
                    adp_ids = {io_update.get('id')}
                if output.get('ParameterName') == 'JOBRESULT_KEY_ERRORMSG':
                    error_msg = f"Import operation failed for IO Adapter ID '{adp_ids}' on VIOS '{io_update.get('vios_name')}': {output.get('ParameterValue')}"
                    module.fail_json(msg=error_msg)

        cleaned_data = cleanup_entries(attributes, sriov=available_adapter_id, io=available_io_updates)
        mapped_data = map_entries(cleaned_data)
        before_update_level = check_current_level(hmc_conn, hmc, mapped_data, system_name)
        final_output = rest_conn.PlatformUpdate(system_uuid, mapped_data)
        after_update_level = check_current_level(hmc_conn, hmc, mapped_data, system_name)
    except (Exception, HmcError) as error:
        error_msg = parse_error_response(error)
        logger.debug("Line number: %d exception: %s", sys.exc_info()[2].tb_lineno, repr(error))
        module.fail_json(msg=error_msg)

    finally:
        try:
            rest_conn.logoff()
        except Exception as logoff_error:
            error_msg = parse_error_response(logoff_error)
            module.warn(msg=error_msg)

    return True, final_output, None


def facts(module):
    params = module.params

    try:
        validate_parameters(params)
    except Exception as e:
        module.fail_json(msg=str(e))

    hmc_host = params['hmc_host']
    hmc_user = params['hmc_auth']['username']
    password = params['hmc_auth']['password']
    system_name = params['system_name']
    changed = False
    hmc_conn = None

    hmc_conn = HmcCliConnection(module, hmc_host, hmc_user, password)
    hmc = Hmc(hmc_conn)
    sys_list = (
        hmc.list_all_managed_system_details(config_F="name") + hmc.list_all_managed_system_details(config_F="type_model*serial_num")
    )
    if not sys_list:
        module.fail_json(msg="No managed systems found in HMC")
    elif system_name not in [v for d in sys_list for v in d.values()]:
        module.fail_json(msg="The managed system is not available in HMC")
    else:
        cmd = f"lssyscfg -r lpar -m {system_name} -F name,rmc_state,lpar_id,lpar_env | grep vioserver | grep -w active"
        output = hmc_conn.execute(cmd).splitlines()
        vios_list = [(line.split(',')[0], line.split(',')[2]) for line in output if line.strip()]
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
                module.fail_json(msg="Given system is not present")
        except (Exception, HmcError) as error:
            error_msg = parse_error_response(error)
            logger.debug("Line number: %d exception: %s", sys.exc_info()[2].tb_lineno, repr(error))
            module.fail_json(msg=error_msg)

        def extract_adapters(response, key):
            if response.get('ParameterName'):
                return None
            value = response.get(key)
            if not value or 'No results' in value:
                return None
            return value

        sriov_output = rest_conn.LicQueryLevel(system_uuid, system_name, type='sriov')
        sriov_adapters = extract_adapters(sriov_output, 'SRIOVAdapterUpdate')

        io_output = rest_conn.LicQueryLevel(system_uuid, system_name, type='io')
        io_adapters = extract_adapters(io_output, 'IOAdapterUpdate')

        vios_info = []

        for vios_name, vios_id in vios_list:
            padded_id = vios_id.zfill(3)
            adapter_info = io_adapters.get(padded_id)
            vios_info.append({
                'vios_name': vios_name,
                'vios_id': vios_id,
                'io_devices': adapter_info if adapter_info else 'No adapters available'
            })

        adapter_info = {
            system_name: {
                'sriov_adapters': sriov_adapters if sriov_adapters else 'No sriov_adapters available',
                'vios_info': vios_info
            }
        }

    return changed, adapter_info, None


def compare_levels(before, after):
    if before is not None and after is not None:
        return json.dumps(before, sort_keys=True) == json.dumps(after, sort_keys=True)
    return False


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
        platform_config=dict(
            type='dict',
            options=dict(
                system_firmware_update=dict(
                    type='dict',
                    options=dict(
                        update_type=dict(type='str', choices=['NoUpdate', 'Update', 'Upgrade']),
                        update_order=dict(type='int'),
                        resource_type=dict(type='str', choices=['IBMWebsite'], default='IBMWebsite'),
                        level=dict(type='str', default="latest"),
                        sriov_adapter_update=dict(
                            type='list',
                            elements='dict',
                            options=dict(
                                all=dict(type="bool"),
                                adapter_id=dict(type='str'),
                                subtype=dict(type='str', choices=['DriverOnly', 'Adapter'])
                            )
                        )
                    )
                ),
                partition_migration=dict(
                    type='list',
                    elements='dict',
                    options=dict(
                        is_quick_evac=dict(type='bool'),
                        destination_managed_system=dict(type='str'),
                        leave_partition_in_target=dict(type='bool')
                    )
                ),
                vios_update=dict(
                    type='list',
                    elements='dict',
                    options=dict(
                        update_type=dict(type='str', choices=['NoUpdate', 'Update']),
                        vios_name=dict(type='str'),
                        update_order=dict(type='int'),
                        resource_type=dict(type='str', choices=['IBMWebsite'], default='IBMWebsite'),
                        level=dict(type='str', default="latest"),
                        io_adapter_update=dict(
                            type='list',
                            elements='dict',
                            options=dict(
                                all=dict(type='bool'),
                                device=dict(type='list', elements='str'),
                                repository=dict(type='str', choices=['IBMWebsite'], default='IBMWebsite')
                            )
                        )
                    )
                )
            )
        ),
        state=dict(type='str', choices=['facts'])
    )

    module = AnsibleModule(
        argument_spec=module_args,
    )

    if module._verbosity >= 5:
        init_logger()

    if sys.version_info < (3, 0):
        py_ver = sys.version_info[0]
        raise ParameterError("Unsupported Python version {0}, supported python version is 3 and above".format(py_ver))

    if module.params.get('state'):
        changed, info, warning = facts(module)
    else:
        changed, info, warning = platform_update(module)
        if info:
            if all(data.get('CurrentStatus') == 'COMPLETED_WITH_ERROR' for data in info):
                changed = False
        if compare_levels(before_update_level, after_update_level):
            changed = False

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
