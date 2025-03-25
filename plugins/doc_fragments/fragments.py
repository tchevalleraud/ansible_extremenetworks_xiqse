# plugins/doc_fragments/fragments.py
# -*- coding: utf-8 -*-

class ModuleDocFragment:
    OPTIONS_IPADDRESS       = r"""
      options:
        ip_address:
          description:
            - Device IP Address
          type: str
          required: true
    """
    OPTIONS_MUTATION        = r"""
      options:
        mutation:
          description:
            - GraphQL mutation for XIQ-SE
          type: str
          required: true
    """
    OPTIONS_PROVIDER        = r"""
      options:
        provider:
          description:
            - Connection information for accessing the ExtremeCloud IQ - Site Engine (XIQ-SE) API.
          required: true
          type: dict
          suboptions:
            protocol:
              description:
                - Protocol to use for API communication.
              type: str
              default: https
              choices: [http, https]
            host:
              description:
                - IP address or FQDN of the XIQ-SE server.
              type: str
              required: true
            port:
              description:
                - Port to use for API communication.
              type: int
              default: 8443
            client_id:
              description:
                - OAuth2 client ID used for authentication.
              type: str
              required: true
              no_log: true
            client_secret:
              description:
                - OAuth2 secret associated with the client ID.
              type: str
              required: true
              no_log: true
            verify:
              description:
                - Whether to validate the SSL certificate.
              type: bool
              default: true
    """
    OPTIONS_QUERY           = r"""
      options:
        query:
          description:
            - GraphQL query for XIQ-SE
          type: str
          required: true
    """
    OPTIONS_SITE_PATH       = r"""
      options:
        site_path:
          description:
            - Full address of the rental you want.
          type: str
          required: true
    """
    OPTIONS_STATE           = r"""
      options:
        state:
          description:
            - Desired state of the item.
          type: str
          default: gathered
          choices:
            - present
            - absent
            - replaced
            - merged
            - deleted
            - gathered
    """
    OPTIONS_STATE_BOOL      = r"""
      options:
        state:
          description:
            - Desired state of the item.
          type: str
          default: gathered
          choices:
            - present
            - absent
            - gathered
    """
    OPTIONS_STATE_STATUS    = r"""
      options:
        state:
          description:
            - Desired state of the item.
          type: str
          default: gathered
          choices:
            - enabled
            - diabled
            - gathered
    """
    OPTIONS_TIMEOUT         = r"""
      options:
        timeout:
          description:
            - Connection timeout in seconds.
          type: int
          default: 30
    """