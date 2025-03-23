# Ansible Collection - Extreme Networks XIQ-SE

This collection provides Ansible modules and roles to manage ExtremeCloudIQ - Site Engine via a custom API client.

## Overview

This collection, currently in version 1.0.22, includes:

- **Module** :
  - `mutation` : Executing a query type mutation
  - `query`: Executing a query type query
  - `version`: Get the version of XIQ-SE

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
ansible-galaxy collection install tchevalleraud-extremenetworks_xiqse-1.0.22.tar.gz
```

## Usage Examples

### Modules

* [Get the version of XIQ-SE](https://github.com/tchevalleraud/ansible_extremenetworks_xiqse/blob/main/examples/get-xiqse-version.yml)

## Documentation

* Detailed information for each role is provided in its own `README` file within the role directory.

## License

[MIT](https://github.com/tchevalleraud/ansible_extremenetworks_xiqse/blob/main/LICENSE)