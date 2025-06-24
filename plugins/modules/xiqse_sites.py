#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: xiqse_sites
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: Get the list of sites from XIQ-SE.
description:
  - This module retrieves the list of sites from XIQ-SE.
  - It is compatible with ExtremeCloudIQ - Site Engine.
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_PROVIDER
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""

EXAMPLES = r"""
- name: Playbook for sync sites with XIQ-SE
  hosts: xiqse_api
  gather_facts: no
  tasks:
    - name: Retrieve existing sites from XIQ-SE
      tchevalleraud.extremenetworks_xiqse.xiqse_sites:
        provider:
          host: "{{ xiqse_host }}"
          client_id: "{{ xiqse_client }}"
          client_secret: "{{ xiqse_secret }}"
      register: result

    - name: Extract existing site paths
      set_fact:
        existing_site_paths: "{{ result.sites | map(attribute='location') | list }}"
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