"""
Config file for some constant value
"""

import base64
from oftest import config
import ConfigParser
import socket

API_BASE_URL = "http://" + config['controller_host'] + ":8181/mars/"

# admin username
ADMIN_USERNAME = 'karaf'
ADMIN_PASSWORD = 'karaf'

# admin login
LOGIN = base64.b64encode(bytes('{}:{}'.format(ADMIN_USERNAME, ADMIN_PASSWORD)))

# Read ini file
INI_FILE = "auto-test.ini"

if socket.gethostname() == 'AutoTestMars':
    INI_FILE = "auto-test.ini"
elif socket.gethostname() == 'Mars-charles':
    INI_FILE = "mars-charles-58.ini"
elif socket.gethostname() == 'ubuntu-mars':
    INI_FILE = "mars-mini-pc.ini"

print 'Test Host: ' + socket.gethostname()
print 'Test INI : ' + INI_FILE
print 'Test Topology : ' + config['test_topology']

conf = ConfigParser.ConfigParser()
conf.read('./mars/ini/' + INI_FILE)

# Remote Power id/pw
REMOTE_POWER_USERNAME = 'snmp'
REMOTE_POWER_PASSWORD = '1234'


def create_device(conf, device_name):
    device = {
        'id': conf.get(device_name, 'id'),
        'name': conf.get(device_name, 'name'),
        'type': conf.get(device_name, 'type'),
        'mgmtIpAddress': conf.get(device_name, 'mgmtIpAddress'),
        'mac': conf.get(device_name, 'mac'),
        'nos': conf.get(device_name, 'nos'),
        'mfr': conf.get(device_name, 'mfr'),
        'port': conf.get(device_name, 'port'),
        'protocol': conf.get(device_name, 'protocol'),
        'mgmtPort': conf.get(device_name, 'mgmtPort'),
        'front_port_A': int(conf.get(device_name, 'front_port_A')),
        'front_port_B': int(conf.get(device_name, 'front_port_B')),
        'front_port_C': int(conf.get(device_name, 'front_port_C')),
        'front_port_D': int(conf.get(device_name, 'front_port_D')),
    }

    return device


def create_remote_power(conf, rp_name):
    remote_power = {
        'username': REMOTE_POWER_USERNAME,
        'password': REMOTE_POWER_PASSWORD,
        'ip': conf.get(rp_name, 'remotePowerIp'),
        'plug_id': conf.get(rp_name, 'remotePowerPlugId'),
    }

    return remote_power

# devices under test
# spine0 = create_device(conf, 'spine0')
# spine1 = create_device(conf, 'spine1')
# leaf0 = create_device(conf, 'leaf0')
# leaf1 = create_device(conf, 'leaf1')

# remote power info
# spine0_power = create_remote_power(conf, 'spine0')
# spine1_power = create_remote_power(conf, 'spine1')
# leaf0_power = create_remote_power(conf, 'leaf0')
# leaf1_power = create_remote_power(conf, 'leaf1')


# dynamically create devices and remote power
for device in conf.sections():
    globals()[device] = create_device(conf, device)
    globals()[device + "_power"] = create_remote_power(conf, device)

host0 = {
    'id': 'host0',
    'mac': '00:00:01:00:00:01',
    'ip': '',
    'mgmt_ip': '192.168.40.117',
    'username': 'mars',
    'password': 'accton',
    'nic_name': 'enp1s0'
}

host1 = {
    'id': 'host1',
    'mac': '00:00:01:00:00:02',
    'ip': '',
    'mgmt_ip': '192.168.40.118',
    'username': 'mars',
    'password': 'accton',
    'nic_name': 'enp1s0'
}

host2 = {
    'id': 'host2',
    'mac': '00:00:01:00:00:03',
    'ip': '',
    'mgmt_ip': '192.168.40.63',
    'username': 'mars',
    'password': 'accton',
    'nic_name': 'enp1s0'
}

host3 = {
    'id': 'host3',
    'mac': '00:00:01:00:00:04',
    'ip': '',
    'mgmt_ip': '192.168.40.113',
    'username': 'mars',
    'password': 'accton',
    'nic_name': 'enp6s16'
}

external_router0 = {
    'id': 'external_router0',
    'mac': '00:00:02:00:00:01',
    'ip': ''
}

external_router1 = {
    'id': 'external_router1',
    'mac': '00:00:02:00:00:02',
    'ip': ''
}

dhcp_server = {
    'id': 'dhcp_server',
    'mac': '00:00:03:00:00:11',
    'ip': ''
}

total_dut = [spine0, spine1, leaf0, leaf1]

if config['test_topology'] == 'scatter':
    devices = [spine0, leaf0, leaf1]
    spines = [spine0]
else:
    devices = total_dut
    spines = [spine0, spine1]

leaves = [leaf0, leaf1]
