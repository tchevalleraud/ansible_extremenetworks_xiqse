#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: device_version
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: TODO
description:
  - TODO
options:
  ip_address:
    description:
      - Device IP Address
    type: str
    required: true
  timeout:
    description:
      - Connection timeout in seconds.
    type: int
    default: 30
"""

EXAMPLES = r"""
- name: Retrieve device version via API
  tchevalleraud.extremenetworks_xiase.device_version:
    ip_address: "10.0.0.1"
    provider:
      host: "192.168.1.1"
      client_id: "RzNxMIxcj7"
      client_secret: "6758749e-2bf3-4b6b-925f-ba599179b5fe"
  register: result

- name: Display the version
  ansible.builtin.debug:
    msg: "Device version: {{ result.version }}"
"""

RETURN = r"""
version:
  description: Detected device version.
  returned: always
  type: str
  sample: "9.1.1.0_B008"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import XIQSE
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import get_xiqse_provider_params

def run_module():
    module_args = dict(
        ip_address  = dict(type="str", required=True),
        provider    = get_xiqse_provider_params(),
        timeout     = dict(type="int", required=False, default=30)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    device_ip       = module.params["ip_address"]
    provider        = module.params["provider"]
    timeout         = module.params["timeout"]

    query = """
        query DeviceFirmware($deviceIp: String!) {
          network {
            device(ip: $deviceIp){
              firmware
            }
          }
        }
    """
    payload = {"deviceIp": device_ip}

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