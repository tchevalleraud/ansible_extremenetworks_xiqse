#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: xiqse_query
author:
  - Thibault Chevalleraud (@tchevalleraud)
short_description: Ansible module that allows you to run a GraphQL query in XIQ-SE
description:
  - This module allows you to execute the query provided by the user in the GraphQL API of XIQ-SE.
  - It is compatible with ExtremeCloudIQ - Site Engine.
extends_documentation_fragment:
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_PROVIDER
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_QUERY
  - tchevalleraud.extremenetworks_xiqse.fragments.OPTIONS_TIMEOUT
"""

EXAMPLES = r"""
- name: Execute a GraphQL query in XIQ-SE
  tchevalleraud.extremenetworks_xiqse.xiqse_query:
    query: |
      query {
        administration {
          serverInfo {
            upTime
            version
          }
        }
      }
    provider:
      host: "{{ ansible_host }}"
      client_id: "{{ xiqse_client }}"
      client_secret: "{{ xiqse_secret }}"
  register: result

- name: Display the result
  ansible.builtin.debug:
    var: result
"""

RETURN = r"""
result:
  description: The full response returned by the GraphQL API of XIQ-SE.
  returned: always
  type: dict
  sample:
    data:
      administration:
        serverInfo:
          upTime: "10234"
          version: "22.5.1.3"

changed:
  description: Indicates if the query caused any changes. Always `false` since this is a read-only operation.
  returned: always
  type: bool
  sample: false

msg:
  description: Message detailing any errors encountered.
  returned: on failure
  type: str
  sample: "GraphQL query failed: Invalid request syntax."
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.xiqse import XIQSE

def run_module():
    module_args = dict(
        provider    = XIQSE.params.get_provider(),
        query       = XIQSE.params.get_query(),
        timeout     = XIQSE.params.get_timeout()
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    provider    = module.params["provider"]
    timeout     = module.params["timeout"]
    query       = module.params["query"]

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
        module.exit_json(changed=False, result=result)
    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()