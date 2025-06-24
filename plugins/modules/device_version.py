#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: device_version
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: Retrieves version information of a device via XIQ-SE.
description:
  - This module allows the collection of equipment versions via the XIQ-SE GraphQL API.
  - It is compatible with ExtremeCloudIQ - Site Engine.
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_IPADDRESS
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_PROVIDER
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""

EXAMPLES = r"""
- name: Playbook to display the version of inventory device
  hosts: voss_devices
  gather_facts: no
  tasks:
    - name: Execute a GraphQL query to get the version
      tchevalleraud.extremenetworks_xiqse.device_version:
        ip_address: "{{ ansible_host }}"
        provider:
          host: "10.0.0.254"
          client_id: "xxxxxxxxxx"
          client_secret: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxxx"
      delegate_to: localhost
      register: result

    - name: Displaying the Device version
      ansible.builtin.debug:
        msg: "{{ result.version }}"

- name: Playbook to display the version of a specific device
  hosts: xiqse_api
  gather_facts: no
  tasks:
    - name: Execute a GraphQL query to get the version
      tchevalleraud.extremenetworks_xiqse.device_version:
        ip_address: "10.0.0.11"
        provider:
          host: "10.0.0.254"
          client_id: "xxxxxxxxxx"
          client_secret: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxxx"
      register: result

    - name: Displaying the Device version
      ansible.builtin.debug:
        msg: "{{ result.version }}"
"""

RETURN = r"""
changed:
  description: Indicates if the module caused a change. Always `false` since this is a read-only operation.
  returned: always
  type: bool
  sample: false

failed:
  description: Indicates if the module failed.
  returned: failure
  type: bool
  sample: false

version:
  description: The firmware version of the device.
  returned: always
  type: str
  sample: "9.1.1.0_B008"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import XIQSE

def run_module():
    module_args = dict(
        ip_address  = XIQSE.params.get_ipAddress(),
        provider    = XIQSE.params.get_provider(),
        timeout     = XIQSE.params.get_timeout()
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    ip_address      = module.params["ip_address"]
    provider        = module.params["provider"]
    timeout         = module.params["timeout"]

    query   = XIQSE.query.network.device.getFirmware()
    payload = {"deviceIp": ip_address}

    try:
        xiqse   = XIQSE(
            host=provider["host"],
            client_id=provider["client_id"],
            client_secret=provider["client_secret"],
            port=provider["port"],
            protocol=provider["protocol"],
            validate_certs=provider["verify"],
            timeout=timeout
        )
        result = xiqse.graphql(query, payload)

        version = result.get("data", {}).get("network", {}).get("device", {}).get("firmware", "Unknown")
        module.exit_json(changed=False, version=version)
    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()