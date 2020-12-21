# Vulnerability reports for Cisco IOS, NX-OS and ACI 

This playbook collects the software version of all devices in the Ansible inventory, queries the [Cisco PSIRT OpenVuln API](https://developer.cisco.com/psirt/) and renders an infrastructure specific [markdown report](https://github.com/NWMichl/openvuln/blob/main/openvuln.md).  
  
  
[![openvuln.md Screenshot](/pictures/openvuln.md.png)](https://github.com/NWMichl/openvuln/blob/main/openvuln.md)
  
## Use Case Description

Are you tired of crawling the PSIRT newsletter to eventually hit relevant security advisories just to curate a spreadsheet document by hand? Well, in this installment of 'Automate the boring stuff' Ansible does the job for you!

## Installation

Of course this depends on your platform but provided that a Linux host is used, we just need Ansible and (optional) Git installed. So for a CENTOS machine we're talking

    $ sudo yum install ansible
    $ sudo yum install git
    $ git clone https://github.com/NWMichl/openvuln.git

to get started.

## Configuration

The playbook needs certain input data to do its job, not all of them are mandatory.

You need to generate a client_key and client_secret via the [Cisco API Console](https://apiconsole.cisco.com/) using your CCO Login under `My Apps & Keys`, `Register a new App`. Select OAuth2.0 Client Credentials and the Cisco PSIRT checkbox to receive the necessary API keys.

### 1. API Credentials

You need to generate a client_key and client_secret via the [Cisco API Console](https://apiconsole.cisco.com/) using your CCO Login under `My Apps & Keys`, `Register a new App`. Select OAuth2.0 Client Credentials and the Cisco PSIRT checkbox to receive the necessary API keys.

Now, under the vars section of the second play, or via external extra vars, we need to populate these key like this.

    client_key: <client_key provided by the API Console> 
    client_secret: <client_secret provided by the API Console>

### 2. (opt) A list of platform / software version combinations

Under the vars section of the second play, or via external extra vars.  
Useful for air-gapped environments or simple API testing.

    host_list:
          - { name: aci, version: 14.2(5k), tag: Test_ACI, host: node-101 }
          - { name: nxos, version: 7.0(3)I7(7), tag: Test_NXOS, host: N9K-1 }
          - ...

### 3. (opt) A list of Cisco ACI APICs & credentials

Under the vars section of the second play, or via external extra vars.  
In case you'd like to automagically include the software version of all leaf/spine switches of one or more ACI fabrics.   

    aci:
      - { apic: <APIC-Fabric1-URL/IP> , aci_user: <username1>, aci_pass: <password1> }
      - { apic: <APIC-Fabric2-URL/IP> , aci_user: <username2>, aci_pass: <password2> }

### 4. (opt) A list of known security advisories via the external file known_vuln.yml

This is just a flat dictionary with the advisoryId as the key and an optional comment as value, to document the status and/or countermeasures for each vulnerability in your infrastructure. Useful to keep track of security improving activities and to quickly spot when new advisories arive. The format of the file looks like:

    ---
    cisco-sa-20200226-fxos-nxos-cdp: CDP not in use / disabled
    cisco-another-advisoryId: We're in the process of updating to version ...
    ...

### 5. (opt) https-proxy for API access 

If you need to reach the OpenVuln API via an https-proxy, just uncomment the four config lines of the Cisco API tasks and enter the proxy parameters, like URL, Port and credentials.

### 6. (opt) Slack notification

In order to use slack as a notification receiver, you need to register a custom app and allow incoming webhooks. The API token can be extracted from the Webhook URL, it's basically everything behind ...services/ . This token has to be provided as an Ansible variable called slack_token and don't forget to uncomment the slack notification task.

## Usage

The playbook can be run 'as is' with the preconfigured test data in the host_list variable, just by adding the API client_key & client_secret.

`ansible-playbook openvuln.yml`

Options:  
`-k` Ansible uses the current user and queries for the password to log into the IOS/NS-OS devices.  
`-i <inventory_file>` If you'd like to provide a (dynamic?) inventory other than the default one living in /etc/ansible/hosts.

Visit the [Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) on how to build your inventory. An example from my little homelab looks like this.

```
[ios]
CSR-1 ansible_host=10.10.10.11 ansible_network_os=ios ansible_ssh_user=nwmichl ansible_ssh_pass=<pass>
CSR-2 ansible_host=10.10.10.12 ansible_network_os=ios ansible_ssh_user=nwmichl ansible_ssh_pass=<pass>

[nxos]
N9K-1 ansible_host=10.10.10.21 ansible_network_os=nxos ansible_ssh_user=nwmichl ansible_ssh_pass=<pass>

[eos]
vEOS-1 ansible_host=10.10.10.31 ansible_network_os=eos ansible_ssh_user=nwmichl ansible_ssh_pass=<pass>
```

### Output

The markdown result is sorted by platform/software version and provides additional info about the associated hostgroup (tag) as well as the number of affected devices. The tag is either provided by hand via the host_files variable or automagically added based on the Ansible inventory groups and ACI APIC URL/IP.  
Oh, and each advisoryId has an HTML reference to the Cisco Security Advisory website with all the bad details.

[![Cisco Security Advisory website](/pictures/sec_adv.png)](https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-nxosbgp-mvpn-dos-K8kbCrJp)  

The additional `openvuln.csv` file lists all hostnames, group/tag and software version to map advisories to affected device using your spreadsheet software of choice. 

## Backlog

- Implement scheduled pipeline for playbook execution
- Pipe the vuln metrics to InfluxDB/Grafana to visualize in a CVSS-based heatmap
- Alert ops about unknown advisories via slack message, Grafana alert or, meh, even mail / ticket
- ...


