#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: version
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: Retrieves the XIQ-SE system version
description:
  - This module fetches the system version of XIQ-SE by querying the GraphQL  API.
  - It is compatible with ExtremeCloudIQ - Site Engine.
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.options_provider
  - tchevalleraud.extremenetworks_xiqse.fragments.options_timeout
"""

EXAMPLES = r"""
- name: Retrieve version via API
  tchevalleraud.extremenetworks_xiqse.version:
    provider:
      host: "192.168.1.1"
      client_id: "RzNxMIxcj7"
      client_secret: "6758749e-2bf3-4b6b-925f-ba599179b5fe"
  register: result

- name: Display the version
  debug:
    msg: "XIQ-SE version: {{ result.version }}"
"""

RETURN = r"""
version:
  description: Detected xiqse version.
  returned: always
  type: str
  sample: "24.10.12.14"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import XIQSE
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import get_xiqse_provider_params

def run_module():
    module_args = dict(
        provider    = get_xiqse_provider_params(),
        timeout     = dict(type="int", required=False, default=30)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    provider    = module.params["provider"]
    timeout     = module.params["timeout"]
    query = """
        query {
          administration {
            serverInfo {
              version
            }
          }
        }
    """

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