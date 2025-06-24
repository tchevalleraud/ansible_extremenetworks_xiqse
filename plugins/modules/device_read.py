#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: device_read
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: Performs synchronization between the equipment and XIQ-SE.
description:
  - This module performs synchronization between a device and XIQ-SE.
  - It is compatible with ExtremeCloudIQ - Site Engine.
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_IPADDRESS
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_PROVIDER
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""

EXAMPLES = r"""
- name: Synchronize device configuration with XIQ-SE
  tchevalleraud.extremenetworks_xiqse.device_read:
    ip_address: "{{ ansible_host }}"
    provider:
      host: "{{ xiqse_host }}"
      client_id: "{{ xiqse_client }}"
      client_secret: "{{ xiqse_secret }}"

- name: Allow time for XIQ-SE to finish synchronizing
  ansible.builtin.wait_for:
    timeout: 10
"""

RETURN = r"""
msg:
  description: The status message indicating whether the synchronization was successful or failed.
  returned: always
  type: str
  sample: "Synchronization in progress for x.x.x.x."

changed:
  description: Indicates if the synchronization request has been successfully sent.
  returned: always
  type: bool
  sample: true

error:
  description: Error message if the synchronization request fails.
  returned: when an error occurs
  type: str
  sample: "Unable to sync device x.x.x.x."
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

    query   = XIQSE.mutation.network.readDevices()
    payload = {"ipAddress": ip_address}

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
        status = result.get("data", {}).get("network", {}).get("readDevices", {}).get("status", "ERROR")

        if status == "SUCCESS":
            module.exit_json(changed=True, msg="Synchronization in progress for "+ip_address+".")
        else:
            raise Exception("Unable to sync device "+ip_address+".")
    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()