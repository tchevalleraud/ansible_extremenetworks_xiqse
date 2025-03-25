#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: xiqse_site
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: Manage sites in XIQ-SE via GraphQL.
description:
  - This module allows you to manage sites in the XIQ-SE platform using GraphQL queries and mutations.
  - It supports retrieving, creating, and deleting sites within ExtremeCloudIQ - Site Engine.
  - It is compatible with ExtremeCloudIQ - Site Engine.
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_PROVIDER
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_SITE_PATH
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_STATE_BOOL
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""


EXAMPLES = r"""
- name: Check if a site exists
  tchevalleraud.extremenetworks_xiqse.xiqse_site:
    site_path: "/World/test"
    state: gathered
    provider:
      host: "{{ ansible_host }}"
      client_id: "{{ xiqse_client }}"
      client_secret: "{{ xiqse_secret }}"

- name: Create a new site
  tchevalleraud.extremenetworks_xiqse.xiqse_site:
    site_path: "/World/test"
    state: present
    provider:
      host: "{{ ansible_host }}"
      client_id: "{{ xiqse_client }}"
      client_secret: "{{ xiqse_secret }}"

- name: Delete an existing site
  tchevalleraud.extremenetworks_xiqse.xiqse_site:
    site_path: "/World/test"
    state: absent
    provider:
      host: "{{ ansible_host }}"
      client_id: "{{ xiqse_client }}"
      client_secret: "{{ xiqse_secret }}"
"""


RETURN = r"""
msg:
  description: Status message indicating the outcome of the operation.
  returned: always
  type: str
  sample: "Site /World/test created."

changed:
  description: Indicates whether a change has been made.
  returned: always
  type: bool
  sample: true

site:
  description: Information about the site when `state: gathered`.
  returned: when `state: gathered`
  type: dict
  sample:
    location: "/World/test"
    siteId: "1234"

error:
  description: Error message if the operation fails.
  returned: on failure
  type: str
  sample: "Error during site creation."
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
                module.exit_json(changed=False, msg="Site "+ site_path +" is exist.", site={
                    "location": site.get("location"),
                    "siteId": site.get("siteId")
                })
            else:
                module.exit_json(changed=False, msg="Site "+ site_path +"  does not exist.", site=None)

        elif state == "present":
            if not site:
                result  = xiqse.graphql(mutation_xiqse_create_site(), payload)
                status  = result.get("data", {}).get("network", {}).get("createSite", {}).get("status", "ERROR")

                if status == "SUCCESS":
                    module.exit_json(changed=True, msg="Site "+ site_path +"  created.", site={
                    "location": result.get("data", {}).get("network", {}).get("createSite", {}).get("siteLocation", None),
                    "siteId": result.get("data", {}).get("network", {}).get("createSite", {}).get("siteId", None)
                })
                else:
                    raise Exception("Error during site creation")
            else:
                module.exit_json(changed=False, msg="Site "+ site_path +"  already present.", site={
                    "location": site.get("location"),
                    "siteId": site.get("siteId")
                })

        elif state == "absent":
            if site:
                result  = xiqse.graphql(mutation_xiqse_delete_site(), payload)
                status  = result.get("data", {}).get("network", {}).get("deleteSite", {}).get("status", "ERROR")

                if status == "SUCCESS":
                    module.exit_json(changed=True, msg="Site "+ site_path +"  deleted.", site=None)
                else:
                    raise Exception("Error during site deleting")
            else:
                module.exit_json(changed=False, msg="Site "+ site_path +" not present.", site=None)

        else:
            raise Exception("This state is not supported.")

    except Exception as e:
        module.fail_json(msg=str(e))
def main():
    run_module()

if __name__ == '__main__':
    main()