#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: version
short_description: Retrieves the XIQ-SE system version
description:
  - This module fetches the system version of XIQ-SE by querying the GraphQL  API.
  - It is compatible with ExtremeCloudIQ - Site Engine.
options:
  xiqse_protocol:
    description:
      - Protocol to use for API communication.
      - Defaults to `"https"`, but can be set to `"http"` if needed.
    required: false
    type: str
    default: "https"
    choices: ["http", "https"]
  xiqse_host:
    description:
      - IP address or hostname of XIQ-SE.
    required: true
    type: str
  xiqse_port:
    description:
      - Port used for API communication.
      - Defaults to `8443` for HTTPS.
    required: false
    type: int
    default: 8443
  xiqse_client:
    description:
      - Client ID for authentication.
    required: true
    type: str
  xiqse_secret:
    description:
      - Secret for authentication.
    required: true
    type: str
    no_log: true
  xiqse_verify:
    description:
      - Whether to verify the SSL certificate when using HTTPS.
      - Defaults to `true`, Set to `false` to disable verification (useful for self-signed certificates).
author:
  - Thibault Chevalleraud (@tchevalleraud)
"""

EXAMPLES = r"""
- name: Retrieve version via API
  version:
    xiqse_host: "192.168.1.1"
    xiqse_client: "RzNxMIxcj7"
    xiqse_secret: "6758749e-2bf3-4b6b-925f-ba599179b5fe"
  register: result

- name: Display the version
  debug:
    msg: "XIQ-SE version: {{ result.version }}"
"""

RETURN = r"""
version:
  description: Detected device version.
  returned: always
  type: str
  sample: "24.10.12.14"
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tchevalleraud.extremenetworks_xiqse.plugins.module_utils.utils import get_auth_token, query_graphql

def run_module():
    module_args = dict(
        xiqse_protocol  = dict(type="str", required=False, default="https"),
        xiqse_host      = dict(type="str", required=True),
        xiqse_port      = dict(type="int", required=False, default=8443),
        xiqse_client    = dict(type="str", required=True, no_log=True),
        xiqse_secret    = dict(type="str", required=True, no_log=True),
        xiqse_verify    = dict(type="bool", required=False, default=True),
        timeout         = dict(type="int", required=False, default=30)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    xiqse_protocol  = module.params["xiqse_protocol"]
    xiqse_host      = module.params["xiqse_host"]
    xiqse_port      = module.params["xiqse_port"]
    xiqse_client    = module.params["xiqse_client"]
    xiqse_secret    = module.params["xiqse_secret"]
    xiqse_verify    = module.params["xiqse_verify"]
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