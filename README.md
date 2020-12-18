# Autogenerate vulnerability reports for Cisco IOS, NX-OS and ACI 

This Ansible playbook collects the software version of all devices in the inventory, queries the [Cisco PSIRT OpenVuln API](https://developer.cisco.com/psirt/) and generates a markdown report.

## API Keys

You need to generate a client_key/id and client_secret via the [Cisco API Console](https://apiconsole.cisco.com/) using your CCO Login under `My Apps & Keys`, `Register a new App`.
Select OAuth2.0 Client Credentials and the Cisco PSIRT checkbox to receive the necessary API keys.

## Input Data

The playbook needs certain input data to do it's job, not all of them are mandatory.

1. 
