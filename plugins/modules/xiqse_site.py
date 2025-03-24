#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: xiqse_site
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: TODO
description:
  - TODO
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_PROVIDER
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import XIQSE
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import get_xiqse_provider_params
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import query_xiqse_site

def run_module():
    module_args = dict(
        provider    = get_xiqse_provider_params(),
        state       = dict(type="str", choices=["query", "present", "absent"], default="query"),
        timeout     = dict(type="int", required=False, default=30)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    provider        = module.params["provider"]
    state           = module.params["state"]
    timeout         = module.params["timeout"]

    query   = query_xiqse_site()
    payload = {"sitePath": "/World/test"}

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

        if state == "present":
            module.exit_json(changed=False, msg="Present")
        elif state == "absent":
            module.exit_json(changed=False, msg="Absent")
        else:
            module.exit_json(changed=False, msg=result)

    except Exception as e:
        module.fail_json(msg=str(e))
def main():
    run_module()

if __name__ == '__main__':
    main()