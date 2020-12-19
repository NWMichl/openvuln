# Vulnerability reports for Cisco IOS, NX-OS and ACI 

This Ansible playbook collects the software version of all devices in the inventory, queries the [Cisco PSIRT OpenVuln API](https://developer.cisco.com/psirt/) and renders a [markdown report](https://github.com/NWMichl/openvuln/blob/main/openvuln.md).  
  
  
![openvuln.md Screenshot](/openvuln.md.png)
  
  
## API Keys

You need to generate a client_key and client_secret via the [Cisco API Console](https://apiconsole.cisco.com/) using your CCO Login under `My Apps & Keys`, `Register a new App`.
Select OAuth2.0 Client Credentials and the Cisco PSIRT checkbox to receive the necessary API keys.

## Input Data

The playbook needs certain input data to do its job, not all of them are mandatory.

### 1. API Credentials

Under the vars section of the second play, or via external extra vars:

    client_key: <client_key provided by the API Console> 
    client_secret: <client_secret provided by the API Console>

### 2. (opt) A list of platform / software version combinations

Under the vars section of the second play, or via external extra vars.  
Useful for air-gapped environments or simple API testing.

    host_list:
          - { name: aci, version: 14.2(5k), tag: Test_ACI }
          - { name: nxos, version: 7.0(3)I7(7), tag: Test_NXOS }
          - ...

### 3. (opt) A list of Cisco ACI APICs & credentials

Under the vars section of the second play, or via external extra vars.  
In case you'd like to automagically include the software version of all leaf/spine switches of one or more ACI fabrics.   

    aci:
      - { apic: <APIC-Fabric1-URL/IP> , aci_user: <username1>, aci_pass: <password1> }
      - { apic: <APIC-Fabric2-URL/IP> , aci_user: <username2>, aci_pass: <password2> }

### 4. (opt) A list of known security advisories via the external file known_vuln.yml

This is just a flat dictionary with the advisoryId as the key and an optional comment as value, to document the status and/or countermeasures for each vulnerability in your infrastructure. This is useful to keep track of security improving activities and to quickly spot when new/unseen advisories arive. The format of the file looks like:

    ---
    cisco-sa-20200226-fxos-nxos-cdp: CDP not in use / disabled
    cisco-another-advisoryId: We're in the process of updating to version ...
    ...

### 5. (opt) https-proxy for API access 

If you need to reach the OpenVuln API via an https-proxy, just uncomment the four config lines of the Cisco API tasks and enter the proxy parameters, like URL, Port and credentials.

## Playbook run 

The playbook can be run 'as is' with the preconfigured test data in the host_list variable.

`ansible-playbook openvuln.yml`

Options:  
`-k` Ansible uses the current user and queries for the password to log into the IOS/NS-OS devices.  
`-i <inventory_file>` If you'd like to provide a (dynamic?) inventory other than the default one living in /etc/ansible/hosts.  

## Output

The markdown result is sorted by platform/software version and provides additional info about the associated hostgroup (tag). The tag is either provided by hand via the host_files variable or automagically added based on the Ansible inventory groups and ACI APIC URL/IP.  
Oh, and each advisoryId has an HTML reference to the Cisco Security Advisory website.

## Backlog

- Implement scheduled pipeline for playbook execution
- Pipe the vuln metrics to InfluxDB/Grafana to visualize in a CVSS-based heatmap
- Alert ops about unknown advisories via slack message, Grafana alert or, meh, even mail / ticket
- ...


