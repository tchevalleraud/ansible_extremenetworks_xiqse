# Ansible Collection - Extreme Networks XIQ-SE

This collection provides Ansible modules and roles to manage ExtremeCloudIQ - Site Engine via a custom API client.

## Overview

This collection, currently in version 1.2.0, includes:

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
ansible-galaxy collection install tchevalleraud-extremenetworks_xiqse-1.2.0.tar.gz
```

## Usage Examples

### Modules

* [Get the version of XIQ-SE](https://github.com/tchevalleraud/ansible_extremenetworks_xiqse/blob/main/examples/get-xiqse-version.yml)

## Documentation

* Detailed information for each role is provided in its own `README` file within the role directory.

## License

[MIT](https://github.com/tchevalleraud/ansible_extremenetworks_xiqse/blob/main/LICENSE)