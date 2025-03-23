# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
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
      timeout:
        description:
          - Connection timeout in seconds.
        type: int
        default: 30
"""
