import requests
import urllib3

def get_auth_token(host, client_id, client_secret, port=8443, protocol="https", validate_certs=False, timeout=5):
    token_url = f"{protocol}://{host}:{port}/oauth/token/access-token?grant_type=client_credentials"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    if not validate_certs:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        response = requests.post(
            token_url,
            auth=(client_id, client_secret),
            headers=headers,
            verify=validate_certs,
            timeout=timeout
        )
        response.raise_for_status()
        result = response.json()

        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception("Authentication failed: No access_token in response")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")

def query_graphql(host, token, query, variables = {}, port=8443, protocol="https", validate_certs=False, timeout=5):
    url = f"{protocol}://{host}:{port}/nbi/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    if not validate_certs:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        response = requests.post(
            url,
            json={'query': query, 'variables': variables},
            headers=headers,
            timeout=timeout,
            verify=validate_certs
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"GraphQL request failed: {e}")