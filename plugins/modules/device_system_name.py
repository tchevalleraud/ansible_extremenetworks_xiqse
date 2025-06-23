#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: device_system_name
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: @TODO
description:
  - This module performs synchronization between a device and XIQ-SE.
  - It is compatible with ExtremeCloudIQ - Site Engine.
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_IPADDRESS
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_PROVIDER
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""

EXAMPLES = r"""
"""

RETURN = r"""
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

    query   = XIQSE.mutation.network_readDevices()
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