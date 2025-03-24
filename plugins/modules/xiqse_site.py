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
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_SITE_PATH
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_STATE_BOOL
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import XIQSE
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import get_xiqse_provider_params
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import get_xiqse_site_path_params
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import get_xiqse_state_bool_params
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import get_xiqse_timeout_params
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import mutation_xiqse_create_site
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import mutation_xiqse_delete_site
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import query_xiqse_site

def run_module():
    module_args = dict(
        provider    = get_xiqse_provider_params(),
        site_path   = get_xiqse_site_path_params(),
        state       = get_xiqse_state_bool_params(),
        timeout     = get_xiqse_timeout_params()
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    provider        = module.params["provider"]
    site_path       = module.params["site_path"]
    state           = module.params["state"]
    timeout         = module.params["timeout"]

    query   = query_xiqse_site()
    payload = {"sitePath": site_path}

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
        site    = result.get("data", {}).get("network", {}).get("siteByLocation", None)

        if state == "gathered":
            if site:
                module.exit_json(changed=False, msg="Site "+ site_path +" is exist.")
            else:
                module.exit_json(changed=False, msg="Site "+ site_path +"  does not exist.")

        elif state == "present":
            if not site:
                result  = xiqse.graphql(mutation_xiqse_create_site(), payload)
                status  = result.get("data", {}).get("network", {}).get("createSite", {}).get("status", "ERROR")

                if status == "SUCCESS":
                    module.exit_json(changed=True, msg="Site "+ site_path +"  created.")
                else:
                    raise Exception("Error during site creation")
            else:
                module.exit_json(changed=False, msg="Site "+ site_path +"  already present.")

        elif state == "absent":
            if site:
                result  = xiqse.graphql(mutation_xiqse_delete_site(), payload)
                status  = result.get("data", {}).get("network", {}).get("deleteSite", {}).get("status", "ERROR")

                if status == "SUCCESS":
                    module.exit_json(changed=True, msg="Site "+ site_path +"  deleted.")
                else:
                    raise Exception("Error during site deleting")
            else:
                module.exit_json(changed=False, msg="Site "+ site_path +"  not present.")

        else:
            raise Exception("This state is not supported.")

    except Exception as e:
        module.fail_json(msg=str(e))
def main():
    run_module()

if __name__ == '__main__':
    main()