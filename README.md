# Ansible Collection - Extreme Networks XIQ-SE

This collection provides Ansible modules and roles to manage ExtremeCloudIQ - Site Engine via a custom API client

## Overview

This collection, currently in version 1.2.19, includes:

- **Module** :
  - `device_version`: Get the version of device via XIQ-SE API 
  - `xiqse_mutation` : Executing a query type mutation
  - `xiqse_query`: Executing a query type query
  - `xiqse_site`: Allows site management within XIQ-SE
  - `xiqse_version`: Get the version of XIQ-SE

## Getting Started

### Prerequisites

- **Ansible:** Version 2.9 or later.
- **Python:** The control node requires Python 3.x.

### Installation

Install the collection via Ansible Galaxy:

```bash
ansible-galaxy collection install tchevalleraud.extremenetworks_xiqse
```

You can also build it locally:

```bash
git clone https://github.com/tchevalleraud/ansible_extremenetworks_xiqse
ansible-galaxy collection build
ansible-galaxy collection install tchevalleraud-extremenetworks_xiqse-1.2.19.tar.gz
```

## Usage Examples

Find all our examples here with the environment configuration :

* [Environment configuration](https://github.com/tchevalleraud/ansible_extremenetworks_xiqse/blob/main/examples/README.md)


* **Device Module** :
  * [Show device version](https://github.com/tchevalleraud/ansible_extremenetworks_xiqse/blob/main/examples/pb.device-version.yaml)
* **XIQ-SE Module** :
  * [Show XIQ-SE version](https://github.com/tchevalleraud/ansible_extremenetworks_xiqse/blob/main/examples/pb.xiqse-version.yaml)

## Documentation

* Detailed information for each role is provided in its own `README` file within the role directory.

## License

[MIT](https://github.com/tchevalleraud/ansible_extremenetworks_xiqse/blob/main/LICENSE)
