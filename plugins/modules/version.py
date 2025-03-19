#!/usr/bin/python
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