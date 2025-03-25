import requests
import urllib3

class XIQSE:
    def __init__(self, host, client_id, client_secret, port=8443, protocol="https", validate_certs=True, timeout=30):
        self.host           = host
        self.client_id      = client_id
        self.client_secret  = client_secret
        self.port           = port
        self.protocol       = protocol
        self.validate_certs = validate_certs
        self.timeout        = timeout
        self.token          = None

        if not self.validate_certs:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def base_url(self):
        return f"{self.protocol}://{self.host}:{self.port}"

    def authenticate(self):
        token_url   = f"{self.base_url()}/oauth/token/access-token?grant_type=client_credentials"
        headers     = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = requests.post(
                token_url,
                auth=(self.client_id, self.client_secret),
                headers=headers,
                verify=self.validate_certs,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()

            if "access_token" in result:
                self.token = result["access_token"]
                return self.token
            else:
                raise Exception("Authentication failed: No access_token in response")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Auth request failed: {e}")

    def graphql(self, query, variables=None):
        if self.token is None:
            self.authenticate()

        if variables is None:
            variables = {}

        url = f"{self.base_url()}/nbi/graphql"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                url,
                json={"query": query, "variables": variables},
                headers=headers,
                timeout=self.timeout,
                verify=self.validate_certs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"GraphQL request failed: {e}")

def get_xiqse_provider_params():
    return dict(type="dict", required=True, options=dict(
        protocol        = dict(type="str", required=False, default="https"),
        host            = dict(type="str", required=True),
        port            = dict(type="int", required=False, default=8443),
        client_id       = dict(type="str", required=True, no_log=True),
        client_secret   = dict(type="str", required=True, no_log=True),
        verify          = dict(type="bool", required=False, default=True),
    ))

def get_xiqse_query_params():
    return dict(type="str", required=True)

def get_xiqse_site_path_params():
    return dict(type="str", required=True)

def get_xiqse_state_params():
    return dict(type="str", choices=["present", "absent", "replaced", "merged", "deleted", "gathered"], default="gathered")

def get_xiqse_state_bool_params():
    return dict(type="str", choices=["present", "absent", "gathered"], default="gathered")

def get_xiqse_state_status_params():
    return dict(type="str", choices=["enabled", "disabled", "gathered"], default="gathered")

def get_xiqse_timeout_params():
    return dict(type="int", required=False, default=30)

def mutation_xiqse_create_site():
    return """
        mutation Site($sitePath: String!) {
          network {
            createSite(input: {
              siteLocation: $sitePath
            }) {
              errorCode
              status
            }
          }
        }
    """

def mutation_xiqse_delete_site():
    return """
        mutation Site($sitePath: String!) {
          network {
            deleteSite(input: {
              siteLocation: $sitePath
            }) {
              errorCode
              status
            }
          }
        }
    """

def query_device_version():
    return """
        query DeviceFirmware($deviceIp: String!) {
          network {
            device(ip: $deviceIp){
              firmware
            }
          }
        }
    """

def query_xiqse_site():
    return """
        query Site($sitePath: String!) {
          network {
            siteByLocation(location: $sitePath){
                location
                siteId
                siteName
            }
          }
        }
    """

def query_xiqse_version():
    return """
        query {
          administration {
            serverInfo {
              version
            }
          }
        }
    """