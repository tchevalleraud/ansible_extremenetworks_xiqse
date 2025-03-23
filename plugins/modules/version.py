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
  - tchevalleraud.extremenetworks_xiqse.provider
options:
  timeout:
    description:
      - Connection timeout in seconds.
    type: int
    default: 30
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
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.utils import get_auth_token, query_graphql

def run_module():
    module_args = dict(
        provider    = dict(type="dict", required=True, options=dict(
            protocol        = dict(type="str", required=False, default="https"),
            host            = dict(type="str", required=True),
            port            = dict(type="int", required=False, default=8443),
            client_id       = dict(type="str", required=True, no_log=True),
            client_secret   = dict(type="str", required=True, no_log=True),
            verify          = dict(type="bool", required=False, default=True),
        )),
        timeout     = dict(type="int", required=False, default=30)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    provider        = module.params["provider"]
    xiqse_protocol  = provider["protocol"]
    xiqse_host      = provider["host"]
    xiqse_port      = provider["port"]
    xiqse_client    = provider["client_id"]
    xiqse_secret    = provider["client_secret"]
    xiqse_verify    = provider["verify"]
    timeout         = module.params["timeout"]

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
        token = get_auth_token(xiqse_host, xiqse_client, xiqse_secret, xiqse_port, xiqse_protocol, xiqse_verify, timeout)
        result = query_graphql(xiqse_host, token, query, {}, xiqse_port, xiqse_protocol, xiqse_verify, timeout)

        version = result.get("data", {}).get("administration", {}).get("serverInfo", {}).get("version", "Unknown")
        module.exit_json(changed=False, version=version)
    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()