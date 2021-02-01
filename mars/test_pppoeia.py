"""
ref: http://docs.python-requests.org/zh_CN/latest/user/quickstart.html

Test pppoeia Rest API.

Test environment

    +--------+
    | spine0 |
    +--------+
   47 |  | 48
      |  +------------+
   26 |            26 |
    +--------+     +--------+
    |  leaf0 |     |  leaf1 |
    +--------+     +--------+
      |    |         |    |
      p0   p1        p2   p3
      |    |         |    |
    host0 host1    host2 host3

p0: port A of leaf0
p1: port B of leaf0
p2: port A of leaf1
p3: port B of leaf1

"""

import oftest.base_tests as base_tests
import config as cfg
import requests
import time
import utils
from oftest import config
from oftest.testutils import *
from utils import *

class PppoeiaTest(base_tests.SimpleDataPlane):
    def setUp(self):
        base_tests.SimpleDataPlane.setUp(self)
        setup_configuration()
        port_configuration()

    def tearDown(self):
        base_tests.SimpleDataPlane.tearDown(self)


class Pppoeia_01_SetterAndGetter(PppoeiaTest):
    """
    Test get Pppoeia rest API
    """

    def runTest(self):
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = [cfg.leaf0['id']]
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.get_device()
        if oftest.config['test_topology'] == 'scatter':
            assert("delegateDevices" in actual_device), "Can not get pppoe ia rule of device"
            assert("devices" in actual_device), "Can not get pppoe ia rule of device"

class Pppoeia_02_Setter_GetAllPortStats(PppoeiaTest):
    """
    Test set and get pppoeia rest API
    """
    def runTest(self):
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = [cfg.leaf0['id']]
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.get_devicePortStats()

        assert("statistics" in actual_device), "cannot get pppoe ia statistics data"

class Pppoeia_03_Setter_GetDevicePortStatsById(PppoeiaTest):
    """
    Test get pppoeia rest API
    """
    def runTest(self):
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = [cfg.leaf0['id']]
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.get_devicePortStatsById(cfg.leaf0['id'])

        assert("statistics" in actual_device), "cannot get pppoe ia port statistics"
        assert(cfg.leaf0['id'] == actual_device["statistics"][0]["deviceId"]), "cannot get pppoe ia port statistics"

class Pppoeia_04_Setter_GetDevicePort(PppoeiaTest):
    """
    Test get pppoeia rest API
    """
    def runTest(self):
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = [cfg.leaf0['id']]
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.get_devicePort()

        assert("ports" in actual_device), "cannot get pppoe ia port"

class Pppoeia_05_Setter_GetDevicePortById(PppoeiaTest):
    """
    Test set and get pppoeia rest API
    """
    def runTest(self):
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = [cfg.leaf0['id']]
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.get_devicePortById(cfg.leaf0['id'])

        assert("ports" in actual_device), "cannot get pppoe ia port"

class Pppoeia_06_Setter_SetDelegate(PppoeiaTest):
    """
    Test set and get pppoeia rest API
    """
    def runTest(self):
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "rest:192.168.40.176:80/2"
            ]
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.build()
        actual_device = pppoeia.get_device()
        assert("delegateDevices" in actual_device), "Can not get pppoe ia rule of device"
        assert("devices" in actual_device), "Can not get pppoe ia rule of device"
        assert("rest:192.168.40.176:80/2" in actual_device["delegateDevices"]), "Can not set rest:192.168.40.176:80/2 of agent"
        
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "rest:192.168.40.177:80/2"
            ]
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.build()
        actual_device = pppoeia.get_device()
        assert("delegateDevices" in actual_device), "Can not get pppoe ia rule of device"
        assert("devices" in actual_device), "Can not get pppoe ia rule of device"
        assert("rest:192.168.40.176:80/2" in actual_device["delegateDevices"]), "Can not set rest:192.168.40.176:80/2 of agent"
        assert("rest:192.168.40.177:80/2" in actual_device["delegateDevices"]), "Can not set rest:192.168.40.177:80/2 of agent"

class Pppoeia_07_Setter_PutDelegate(PppoeiaTest):
    """
    Test set and get pppoeia rest API
    """
    def runTest(self):
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "rest:192.168.40.176:80/2"
            ]
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.build()
        actual_device = pppoeia.get_device()
        assert("delegateDevices" in actual_device), "Can not get pppoe ia rule of device"
        assert("devices" in actual_device), "Can not get pppoe ia rule of device"
        assert("rest:192.168.40.176:80/2" in actual_device["delegateDevices"]), "Can not set rest:192.168.40.176:80/2 of agent"
        
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "rest:192.168.40.176:80/3"
            ]
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_delegate()
        actual_device = pppoeia.get_device()
        assert("delegateDevices" in actual_device), "Can not get pppoe ia rule of device"
        assert("devices" in actual_device), "Can not get pppoe ia rule of device"
        assert("rest:192.168.40.176:80/3" in actual_device["delegateDevices"]), "Can not set rest:192.168.40.176:80/2 of agent"

class Pppoeia_08_Setter_PutPppoeiaStatusById(PppoeiaTest):
    """
    Test put and get pppoeia rest API
    """
    def runTest(self):
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "status": "true"
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])
        actual_device = pppoeia.get_device()
        assert("delegateDevices" in actual_device), "Can not get pppoe ia rule of device"
        assert("devices" in actual_device), "Can not get pppoe ia rule of device"
        testStatus = "false"
        for dictData in actual_device["devices"]:
            #print("debug pppoe status:", dictData)
            if dictData["deviceId"] == cfg.leaf0['id']:
                if dictData["status"] == True: testStatus = "true"
        assert("true" == testStatus), "Can not put status of {}".format(cfg.leaf0['id'])
        
        pppoeia_cfg['data'] = {
            "status": "false"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])
        actual_device = pppoeia.get_device()
        assert("delegateDevices" in actual_device), "Can not get pppoe ia rule of device"
        assert("devices" in actual_device), "Can not get pppoe ia rule of device"
        testStatus = "false"
        for dictData in actual_device["devices"]:
            #print("debug pppoe status:", dictData)
            if dictData["deviceId"] == cfg.leaf0['id']:
                if dictData["status"] == False: testStatus = "true"
        assert("true" == testStatus), "Can not put status of {}".format(cfg.leaf0['id'])

class Pppoeia_09_Setter_PutPppoeiaHostPort(PppoeiaTest):
    """
    Test put and get pppoeia rest API
    """
    def runTest(self):
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "true",
            "circuitId": "port1",
            "remoteId": ""
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        actual_device = pppoeia.get_devicePortById(cfg.leaf0['id'])
        assert(actual_device["ports"][0]["deviceId"] == cfg.leaf0['id']), "Can not get device id"
        assert(actual_device["ports"][0]["circuitId"] == "port1"), "pppoe circuitId value error1"

        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "true",
            "circuitId": "test_cir",
            "remoteId": "test_remote"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        actual_device = pppoeia.get_devicePortById(cfg.leaf0['id'])
        assert(actual_device["ports"][0]["deviceId"] == cfg.leaf0['id']), "Can not get device id"
        assert(actual_device["ports"][0]["circuitId"] == "test_cir"), "pppoe circuitId value error2"
        assert(actual_device["ports"][0]["remoteId"] == "test_remote"), "pppoe remoteId value error2"

        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "false",
            "circuitId": "test_cir",
            "remoteId": "test_remote"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        actual_device = pppoeia.get_devicePortById(cfg.leaf0['id'])
        assert(actual_device["ports"][0]["deviceId"] == cfg.leaf0['id']), "Can not get device id"
        assert(actual_device["ports"][0]["stripVendor"] == False), "pppoe stripVendor value error2"
        assert(actual_device["ports"][0]["hostPort"] == True), "pppoe hostPort value error2"

        pppoeia_cfg['data'] = {
            "hostPort": "false",
            "stripVendor": "true",
            "circuitId": "test_cir",
            "remoteId": "test_remote"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        actual_device = pppoeia.get_devicePortById(cfg.leaf0['id'])
        assert(actual_device["ports"][0]["deviceId"] == cfg.leaf0['id']), "Can not get device id"
        assert(actual_device["ports"][0]["stripVendor"] == True), "pppoe stripVendor value error2"
        assert(actual_device["ports"][0]["hostPort"] == False), "pppoe hostPort value error2"

class Pppoeia_10_Setter_DeletePppoeiaHostPort(PppoeiaTest):
    """
    Test get and put pppoeia rest API
    """
    def runTest(self):
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "rest:192.168.40.176:80/2"
            ]
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.build()
        actual_device = pppoeia.get_device()
        assert("delegateDevices" in actual_device), "Can not get pppoe ia rule of device"
        assert("devices" in actual_device), "Can not get pppoe ia rule of device"
        assert("rest:192.168.40.176:80/2" in actual_device["delegateDevices"]), "Can not set rest:192.168.40.176:80/2 of agent"
        
        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "rest:192.168.40.176:80/3"
            ]
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.build()
        actual_device = pppoeia.get_device()
        assert("delegateDevices" in actual_device), "Can not get pppoe ia rule of device"
        assert("devices" in actual_device), "Can not get pppoe ia rule of device"
        assert("rest:192.168.40.176:80/2" in actual_device["delegateDevices"]), "Can not set rest:192.168.40.176:80/2 of agent"
        assert("rest:192.168.40.176:80/3" in actual_device["delegateDevices"]), "Can not set rest:192.168.40.176:80/3 of agent"

        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 2)
        actual_device = pppoeia.get_device()
        assert("rest:192.168.40.176:80/2" not in actual_device["delegateDevices"]), "Can not delete rest:192.168.40.176:80/2"
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 3)
        actual_device = pppoeia.get_device()
        assert("rest:192.168.40.176:80/3" not in actual_device["delegateDevices"]), "Can not delete rest:192.168.40.176:80/3"


class Pppoeia_Run_1_Setter_OneDutPppoeiaDiscovery(PppoeiaTest):
    """
    Test Pppoeia Discovery Behavior
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.111",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.113",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        #reset delault
        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "false"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf1['id'])
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 2)
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 3)
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf1['id'], 2)
        pppoeia_cfg['data'] = {
            "hostPort": "false",
            "stripVendor": "false",
            "circuitId": "",
            "remoteId": ""
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf1['id'], 1)
        wait_for_seconds(4)

        pppoeia_cfg = {}
        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "status": "true"
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])

        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "{}/{}".format(cfg.leaf0['id'], 2)
            ]
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.build()

        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "true",
            "circuitId": "test_a",
            "remoteId": "test_b"
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        wait_for_seconds(4)

        from struct import pack
        pkt_from_p1_to_p2 = simple_pppoeia_packet(
            pktlen=60, 
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac'],
            pppoe_paylen=12,
            pppoe_payload=pack("12B",0x01,0x01,0,0,0x01,0x03,0,0x04,0x25,0x1d,0,0)
        )
        expected_pkt = simple_eth_packet(
            pktlen=14,
            eth_type=0x8863,
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac']
        )
        self.dataplane.send(ports[0], str(pkt_from_p1_to_p2))
        wait_for_seconds(0.1)
        verify_packet(self, str(expected_pkt), ports[1])

class Pppoeia_Run_2_Setter_OneDutPppoeiaSecondDutVerify(PppoeiaTest):
    """
    Test Pppoeia Discovery Behavior
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.111",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.113",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        #reset delault
        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "false"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf1['id'])
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 2)
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 3)
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf1['id'], 2)
        pppoeia_cfg['data'] = {
            "hostPort": "false",
            "stripVendor": "false",
            "circuitId": "",
            "remoteId": ""
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf1['id'], 1)
        wait_for_seconds(4)

        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "true"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])

        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "{}/{}".format(cfg.leaf0['id'], 2)
            ]
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.build()

        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "true",
            "circuitId": "test_a",
            "remoteId": "test_b"
        }

        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        wait_for_seconds(4)

        from struct import pack
        pkt_from_p1_to_p2 = simple_pppoeia_packet(
            pktlen=60, 
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac'],
            pppoe_paylen=12,
            pppoe_payload=pack("12B",0x01,0x01,0,0,0x01,0x03,0,0x04,0x25,0x1d,0,0)
        )
        expected_pkt = simple_eth_packet(
            pktlen=14,
            eth_type=0x8863,
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac']
        )
        self.dataplane.send(ports[0], str(pkt_from_p1_to_p2))
        wait_for_seconds(0.1)
        verify_packet(self, str(expected_pkt), ports[1])
        verify_no_packet(self, str(expected_pkt), ports[2])

class Pppoeia_Run_3_Setter_TwoDutPppoeiaDiscovery(PppoeiaTest):
    """
    Test Pppoeia Discovery Behavior
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.111",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.113",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        #reset delault
        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "false"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf1['id'])
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 2)
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 3)
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf1['id'], 2)
        pppoeia_cfg['data'] = {
            "hostPort": "false",
            "stripVendor": "false",
            "circuitId": "",
            "remoteId": ""
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf1['id'], 1)
        wait_for_seconds(4)

        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "true"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])

        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "{}/{}".format(cfg.leaf0['id'], 2)
            ]
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.build()
        # actual_device = pppoeia.get_device()
        # assert("{}/{}".format(cfg.leaf0['id'], 2) in actual_device["delegateDevices"]), \
        #     "Can not set {}/{} of agent".format(cfg.leaf0['id'],2)
        
        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "true",
            "circuitId": "test_a",
            "remoteId": "test_b"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)

        pppoeia_cfg['data'] = {
            "status": "true"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf1['id'])

        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "{}/{}".format(cfg.leaf1['id'], 2)
            ]
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.build()
        # actual_device = pppoeia.get_device()
        # assert("{}/{}".format(cfg.leaf1['id'], 2) in actual_device["delegateDevices"]), \
        #     "Can not set {}/{} of agent".format(cfg.leaf1['id'],2)
        wait_for_seconds(4)

        from struct import pack
        pkt_from_p1_to_p2 = simple_pppoeia_packet(
            pktlen=60, 
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac'],
            pppoe_paylen=12,
            pppoe_payload=pack("12B",0x01,0x01,0,0,0x01,0x03,0,0x04,0x25,0x1d,0,0)
        )
        expected_pkt = simple_eth_packet(
            pktlen=14,
            eth_type=0x8863,
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac']
        )
        self.dataplane.send(ports[0], str(pkt_from_p1_to_p2))
        wait_for_seconds(0.1)
        verify_packet(self, str(expected_pkt), ports[1])
        verify_packet(self, str(expected_pkt), ports[3])
        verify_no_packet(self, str(expected_pkt), ports[2])

class Pppoeia_Run_4_Setter_OneDutPppoeiaNoDelegates(PppoeiaTest):
    """
    Test Pppoeia Delegates Behavior
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.111",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        #reset delault
        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "false"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf1['id'])
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 2)
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 3)
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf1['id'], 2)
        pppoeia_cfg['data'] = {
            "hostPort": "false",
            "stripVendor": "false",
            "circuitId": "",
            "remoteId": ""
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf1['id'], 1)

        #leaf0
        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "true"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])

        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "true",
            "circuitId": "test_a",
            "remoteId": "test_b"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        wait_for_seconds(2)

        from struct import pack
        pkt_from_p1_to_p2 = simple_pppoeia_packet(
            pktlen=60, 
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac'],
            pppoe_paylen=12,
            pppoe_payload=pack("12B",0x01,0x01,0,0,0x01,0x03,0,0x04,0x25,0x1d,0,0)
        )
        expected_pkt = simple_eth_packet(
            pktlen=14,
            eth_type=0x8863,
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac']
        )
        self.dataplane.send(ports[0], str(pkt_from_p1_to_p2))
        wait_for_seconds(0.1)
        verify_no_packet(self, str(expected_pkt), ports[1])

class Pppoeia_Run_5_Setter_TwoDutPppoeiaOneNoDelegates(PppoeiaTest):
    """
    Test Pppoeia Delegates Behavior
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.111",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.113",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        #reset delault
        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "false"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf1['id'])
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 2)
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf0['id'], 3)
        actual_device = pppoeia.delete_deviceDelegatesById(cfg.leaf1['id'], 2)
        pppoeia_cfg['data'] = {
            "hostPort": "false",
            "stripVendor": "false",
            "circuitId": "",
            "remoteId": ""
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf1['id'], 1)

        #leaf0
        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "true"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])

        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "true",
            "circuitId": "test_a",
            "remoteId": "test_b"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)
        
        #leaf1
        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "true"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf1['id'])

        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "true",
            "circuitId": "test_a",
            "remoteId": "test_b"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf1['id'], 1)
        wait_for_seconds(2)

        from struct import pack
        pkt_from_p1_to_p2 = simple_pppoeia_packet(
            pktlen=60, 
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac'],
            pppoe_paylen=12,
            pppoe_payload=pack("12B",0x01,0x01,0,0,0x01,0x03,0,0x04,0x25,0x1d,0,0)
        )
        expected_pkt = simple_eth_packet(
            pktlen=14,
            eth_type=0x8863,
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac']
        )
        self.dataplane.send(ports[2], str(pkt_from_p1_to_p2))
        wait_for_seconds(0.1)
        verify_no_packet(self, str(expected_pkt), ports[3])

class Pppoeia_Run_6_Setter_TwoDutReboot(PppoeiaTest):
    """
    Test Pppoeia status after reboot
    """
    def runTest(self):

        pppoeia_cfg = {}
        pppoeia_cfg['data'] = {
            "status": "true"
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaById(cfg.leaf0['id'])

        pppoeia_cfg['data'] = {
            "delegateDevices": [
                "{}/{}".format(cfg.leaf0['id'], 2)
            ]
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.build()

        pppoeia_cfg['device-id'] = cfg.leaf0['id']
        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "true",
            "circuitId": "port1_1",
            "remoteId": ""
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf0['id'], 1)

        pppoeia_cfg['device-id'] = cfg.leaf1['id']
        pppoeia_cfg['data'] = {
            "hostPort": "true",
            "stripVendor": "false",
            "circuitId": "port1_2",
            "remoteId": ""
        }
        pppoeia = PPPoEIA(pppoeia_cfg)
        actual_device = pppoeia.put_pppoeiaByIdAndPort(cfg.leaf1['id'], 1)
        wait_for_seconds(4)

        rebootTest = RebootSwitch(cfg.leaf0['id'])
        rebootTest.reboot()

        rebootTest = RebootSwitch(cfg.leaf1['id'])
        rebootTest.reboot()
        time.sleep(180)

        actual_device = pppoeia.get_device()
        testStatus = "false"
        for dictData in actual_device["devices"]:
            #print("debug pppoe status:", dictData)
            if dictData["deviceId"] == cfg.leaf0['id']:
                if dictData["status"] == True: testStatus = "true"
        assert("true" == testStatus), "Can not put status of {}".format(cfg.leaf0['id'])
        
        assert("{}/{}".format(cfg.leaf0['id'], 2) in actual_device["delegateDevices"]), \
            "Can not set {}/{} of agent".format(cfg.leaf0['id'],2)

        actual_device = pppoeia.get_devicePortById(cfg.leaf0['id'])
        #print("debug pppoe status:", actual_device)
        assert(actual_device["ports"][0]["deviceId"] == cfg.leaf0['id']), "Can not get device id"
        assert(actual_device["ports"][0]["hostPort"] == True), "pppoe hostPort value error1"
        assert(actual_device["ports"][0]["stripVendor"] == True), "pppoe stripVendor value error1"
        assert(actual_device["ports"][0]["circuitId"] == "port1_1"), "pppoe circuitId value error1"
        assert(actual_device["ports"][0]["remoteId"] == ""), "pppoe remoteId value error1"

        actual_device = pppoeia.get_devicePortById(cfg.leaf1['id'])
        assert(actual_device["ports"][0]["deviceId"] == cfg.leaf1['id']), "Can not get device id"
        assert(actual_device["ports"][0]["hostPort"] == True), "pppoe hostPort value error1"
        assert(actual_device["ports"][0]["stripVendor"] == False), "pppoe stripVendor value error1"
        assert(actual_device["ports"][0]["circuitId"] == "port1_2"), "pppoe circuitId value error2"
        assert(actual_device["ports"][0]["remoteId"] == ""), "pppoe remoteId value error2"
