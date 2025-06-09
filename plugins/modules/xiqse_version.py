#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: xiqse_version
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: Retrieves the XIQ-SE system version
description:
  - This module fetches the system version of XIQ-SE by querying the GraphQL  API.
  - It is compatible with ExtremeCloudIQ - Site Engine.
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_PROVIDER
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""

EXAMPLES = r"""
- name: Playbook to display the version of XIQ-SE
  hosts: xiqse_api
  gather_facts: no
  tasks:
    - name: Execute a GraphQL query to get the version
      tchevalleraud.extremenetworks_xiqse.xiqse_version:
        provider:
          host: "10.0.0.254"
          client_id: "xxxxxxxxxx"
          client_secret: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxxx"
      register: result

    - name: Displaying the XIQ-SE version
      ansible.builtin.debug:
        msg: "XIQ-SE version: {{ result.version }}"
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
  description: Detected xiqse version.
  returned: always
  type: str
  sample: "24.10.12.14"
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

    provider    = module.params["provider"]
    timeout     = module.params["timeout"]
    query       = XIQSE.query.administration_serverInfo_version()

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
        result = xiqse.graphql(query)

        version = result.get("data", {}).get("administration", {}).get("serverInfo", {}).get("version", "Unknown")
        module.exit_json(changed=False, version=version)
    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()