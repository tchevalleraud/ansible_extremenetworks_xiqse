#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: xiqse_sites
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: @TODO
description:
  - This module performs synchronization between a device and XIQ-SE.
  - It is compatible with ExtremeCloudIQ - Site Engine.
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_PROVIDER
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""

EXAMPLES = r"""
- name: Playbook to display the version of XIQ-SE
"""

RETURN = r"""
failed:
  description: Indicates if the module failed.
  returned: failure
  type: bool
  sample: false

sites:
  description: The list of sites.
  returned: always
  type: list
  sample: []
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import XIQSE

def run_module():
    module_args = dict(
        provider    = XIQSE.params.get_provider(),
        timeout     = XIQSE.params.get_timeout()
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    provider        = module.params["provider"]
    timeout         = module.params["timeout"]

    query   = XIQSE.query.network.sites()

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
        result  = xiqse.graphql(query)
        sites   = result.get("data", {}).get("network", {}).get("sites", None)

        module.exit_json(changed=False, sites=sites)

    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()