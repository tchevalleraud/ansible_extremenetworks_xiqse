#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: xiqse_add_device
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: TODO
description:
  - This module performs synchronization between a device and XIQ-SE.
  - It is compatible with ExtremeCloudIQ - Site Engine.
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_PROVIDER
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""

EXAMPLES = r"""
- name: Add a device to XIQ-SE
"""

RETURN = r"""
failed:
  description: Indicates if the module failed.
  returned: failure
  type: bool
  sample: false

result:
  description: The result of the add device operation.
  returned: always
  type: dict
  sample: {}
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import XIQSE

def run_module():
    module_args = dict(
        ip_address  = XIQSE.params.get_ipAddress(),
        profile_name= XIQSE.params.get_profile_name(),
        provider    = XIQSE.params.get_provider(),
        site_path   = XIQSE.params.get_sitePath(),
        timeout     = XIQSE.params.get_timeout()
    )
    
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    ip_address      = module.params["ip_address"]
    profile_name    = module.params["profile_name"]
    provider        = module.params["provider"]
    site_path       = module.params["site_path"]
    timeout         = module.params["timeout"]

    query   = XIQSE.mutation.network_addDevice()
    payload = {"deviceIp": ip_address, "profileName": profile_name, "sitePath": site_path}

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
        result  = xiqse.graphql(query, payload)
        module.exit_json(changed=False, result=result)
    except Exception as e:
        module.fail_json(msg=str(e))
    
def main():
    run_module()

if __name__ == '__main__':
    main()