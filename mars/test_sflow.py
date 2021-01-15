"""
ref: http://docs.python-requests.org/zh_CN/latest/user/quickstart.html

Test Sflow Rest API.

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

HOST0_MAC = "00:90:9e:9d:b4:77"
HOST1_MAC = "00:90:9e:9d:b4:7b"
HOST2_MAC = "00:90:9e:9d:b4:85"
HOST3_MAC = "00:90:9e:9d:b4:96"

class SflowTest(base_tests.SimpleDataPlane):
    def setUp(self):
        base_tests.SimpleDataPlane.setUp(self)
        setup_configuration()
        port_configuration()

    def tearDown(self):
        base_tests.SimpleDataPlane.tearDown(self)


class Sflow_01_SetterAndGetter(SflowTest):
    """
    Test set and get Sflow rest API
    """

    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = [cfg.leaf0['id']]
        sflow = SFLOW(sflow_cfg)
        actual_device = sflow.get_device()
        if oftest.config['test_topology'] == 'scatter':
            assert("sflows" in actual_device), "Can not get device sflow rule"

class Sflow_02_Setter_GetRuleByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [3],
            "duration": 10000000
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert("192.168.2.20" == actual_device["controllerIp"]), "collector_ip setup fail"
        assert(1500 == actual_device["maxPayloadLength"]), "'maxPayloadLength setup fail"
        assert(10000000 == actual_device["duration"]), "duration setup fail"
        assert(10000000 == actual_device["pollingInterval"]), "pollingInterval setup fail"
        assert(16777215 == actual_device["samplingRate"]), "samplingRate setup fail"
        assert(256 == actual_device["maxHeaderLength"]), "maxHeaderLength setup fail"

class Sflow_03_Setter_SetMinPollingByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 1,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert("192.168.2.20" == actual_device["controllerIp"]), "collector_ip setup fail"
        assert(1 == actual_device["pollingInterval"]), "pollingInterval setup fail"

        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 1000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.buildNotSuccess()

        #print("Debug: Build sflow rule not success ==> pass")
        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(1 == actual_device["pollingInterval"]), "pollingInterval setup fail"

class Sflow_04_Setter_SetMaxPollingByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])


        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(10000000 == actual_device["pollingInterval"]), "pollingInterval setup fail(c1)"

        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 1,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.buildNotSuccess()

        #print("Debug: Build sflow rule not success ==> pass")
        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(10000000 == actual_device["pollingInterval"]), "pollingInterval setup fail(c2)"

class Sflow_05_Setter_SetMinHeaderByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 64,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert("192.168.2.20" == actual_device["controllerIp"]), "collector_ip setup fail"
        assert(64 == actual_device["maxHeaderLength"]), "maxHeaderLength setup fail"

        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.buildNotSuccess()

        #print("Debug: Build sflow rule not success ==> pass")
        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(64 == actual_device["maxHeaderLength"]), "maxHeaderLength setup fail"

class Sflow_06_Setter_SetMaxHeaderByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(256 == actual_device["maxHeaderLength"]), "maxHeaderLength setup fail(c1)"

        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 64,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.buildNotSuccess()

        #print("Debug: Build sflow rule not success ==> pass")
        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(256 == actual_device["maxHeaderLength"]), "maxHeaderLength setup fail(c2)"

class Sflow_07_Setter_SetMinPayLoadByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 200,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])


        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(200 == actual_device["maxPayloadLength"]), "maxPayloadLength setup fail"

        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.buildNotSuccess()

        #print("Debug: Build sflow rule not success ==> pass")
        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(200 == actual_device["maxPayloadLength"]), "maxPayloadLength setup fail"

class Sflow_08_Setter_SetMaxPayLoadByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(1500 == actual_device["maxPayloadLength"]), "maxPayloadLength setup fail(c1)"

        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 200,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.buildNotSuccess()

        #print("Debug: Build sflow rule not success ==> pass")
        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(1500 == actual_device["maxPayloadLength"]), "maxPayloadLength setup fail(c2)"

class Sflow_09_Setter_SetMinSampleRateByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 200,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 256,
            "port": [1],
            "duration": 10000000
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])


        #print("debug sflow device status1:", actual_device)
        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(256 == actual_device["samplingRate"]), "samplingRate setup fail"

        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.buildNotSuccess()

        #print("Debug: Build sflow rule not success ==> pass")
        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(256 == actual_device["samplingRate"]), "samplingRate setup fail"

class Sflow_10_Setter_SetMaxSampleRateByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])


        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(16777215 == actual_device["samplingRate"]), "samplingRate setup fail(c1)"

        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 200,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 256,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.buildNotSuccess()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(16777215 == actual_device["samplingRate"]), "samplingRate setup fail(c2)"

class Sflow_11_Setter_SetMinDurationByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 200,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 256,
            "port": [1],
            "duration": 30
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])


        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(30 == actual_device["duration"]), "duration setup fail"

        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.buildNotSuccess()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(30 == actual_device["duration"]), "duration setup fail"

class Sflow_12_Setter_SetMaxDurationByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(10000000 == actual_device["duration"]), "duration setup fail(c1)"

        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 200,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 256,
            "port": [1],
            "duration": 30
        }
        actual_device = sflow.buildNotSuccess()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(10000000 == actual_device["duration"]), "duration setup fail(c2)"

class Sflow_13_Setter_DelRuleByDeviceId(SflowTest):
    """
    Test set and get Sflow rest API
    """
    def runTest(self):
        sflow_cfg = {}
        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.10",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.build()

        sflow_cfg['device-id'] = cfg.leaf1['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.20",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.build()

        sflow_cfg['device-id'] = cfg.spine0['id']
        sflow_cfg['data'] = {
            "collector_ip": "192.168.2.30",
            "max_payload_length": 1500,
            "max_header_length": 256,
            "polling_interval": 10000000,
            "sample_rate": 16777215,
            "port": [1],
            "duration": 10000000
        }
        actual_device = sflow.build()

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert("192.168.2.10" == actual_device["controllerIp"]), "1:collector_ip setup fail"
        
        actual_device = sflow.get_deviceById(cfg.leaf1['id'])
        assert("192.168.2.20" == actual_device["controllerIp"]), "2:collector_ip setup fail"
        
        actual_device = sflow.get_deviceById(cfg.spine0['id'])
        assert("192.168.2.30" == actual_device["controllerIp"]), "3:collector_ip setup fail"

        actual_device = sflow.delete_deviceById(cfg.leaf0['id'])

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert({} == actual_device), "delete leaf0 fail"

        actual_device = sflow.delete_deviceById(cfg.leaf1['id'])

        actual_device = sflow.get_deviceById(cfg.leaf1['id'])
        assert({} == actual_device), "delete leaf1 fail"

        actual_device = sflow.delete_deviceById(cfg.spine0['id'])

        actual_device = sflow.get_deviceById(cfg.spine0['id'])
        assert({} == actual_device), "delete spine fail"

class Sflow_Run_1_Setter_DuringTime(SflowTest):
    """
    Test sflow during time
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg_sw1 = {}
        vlan_cfg_sw1['device-id'] = cfg.leaf0['id']
        sflow_cfg = {}
        sflow_cfg['device-id'] = [cfg.leaf0['id']]

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.113",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        # vlan_cfg = {}
        # vlan_cfg['device-id'] = cfg.leaf0['id']
        # vlan_cfg['ports'] = [
        #     {
        #         "port": 1,
        #         "native": 10,
        #         "mode": "hybrid",
        #         "vlans": [
        #             "100/untag"
        #         ]
        #     }
        # ]
        # vlan = StaticVLAN(vlan_cfg).build()

        sflow_cfg['device-id'] = cfg.leaf1['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.13",
            "max_payload_length": 200,
            "max_header_length": 64,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 30
        }
        actual_device = sflow.build()
        time.sleep(35)

        #actual_device = sflow.delete_deviceById(cfg.leaf1['id'])
        #time.sleep(2)
        actual_device = sflow.get_deviceById(cfg.leaf1['id'])
        assert({} == actual_device), "delete leaf1 fail"
        
        #part 2
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.111",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.13",
            "max_payload_length": 200,
            "max_header_length": 64,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 30
        }
        actual_device = sflow.build()
        time.sleep(35)

        #actual_device = sflow.delete_deviceById(cfg.leaf0['id'])
        #time.sleep(2)
        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert({} == actual_device), "delete leaf0 fail"

class Sflow_Run_2_Setter_TwoDutDuringTime(SflowTest):
    """
    Test sflow during time
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg_sw1 = {}
        vlan_cfg_sw1['device-id'] = cfg.leaf0['id']
        sflow_cfg = {}
        sflow_cfg['device-id'] = [cfg.leaf0['id']]

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.113",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        sflow_cfg['device-id'] = cfg.leaf1['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.13",
            "max_payload_length": 200,
            "max_header_length": 64,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 30
        }
        actual_device = sflow.build()

        #part 2
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.111",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.13",
            "max_payload_length": 200,
            "max_header_length": 64,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 30
        }
        actual_device = sflow.build()
        time.sleep(35)
        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan = StaticVLAN(vlan_cfg)
        vlan.delete_DevieIdNoVerify({'device-id': cfg.leaf0['id']})
        vlan.delete_DevieIdNoVerify({'device-id': cfg.leaf1['id']})

        #actual_device = sflow.delete_deviceById(cfg.leaf0['id'])
        #time.sleep(2)
        #actual_device = sflow.delete_deviceById(cfg.leaf1['id'])
        #time.sleep(2)
        actual_device = sflow.get_deviceById(cfg.leaf1['id'])
        assert({} == actual_device), "delete leaf1 fail"

        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert({} == actual_device), "delete leaf0 fail"

class Sflow_Run_3_Setter_OneDutCapture(SflowTest):
    """
    Test capture sflow packet
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg_sw1 = {}
        vlan_cfg_sw1['device-id'] = cfg.leaf0['id']
        sflow_cfg = {}
        sflow_cfg['device-id'] = [cfg.leaf0['id']]

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan = StaticVLAN(vlan_cfg)
        vlan.delete_DevieIdNoVerify({'device-id': cfg.leaf0['id']})
        vlan.delete_DevieIdNoVerify({'device-id': cfg.leaf1['id']})

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.113",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['ports'] = [
            {
                "port": 1,
                "native": 10,
                "mode": "access",
                "vlans": [
                    "10/untag"
                ]
            }
        ]
        vlan = StaticVLAN(vlan_cfg).build()

        sflow_cfg['device-id'] = cfg.leaf1['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.14",
            "max_payload_length": 200,
            "max_header_length": 64,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 1000
        }
        actual_device = sflow.build()

        pkt_from_p2_to_p2 = simple_eth_packet(
            pktlen=120, 
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac']
        )
        expected_pkt = simple_eth_packet(
            pktlen=12,
            eth_type=0x0800,
            eth_dst=HOST3_MAC,
            eth_src=cfg.leaf1['mac']
        )
        #print("debug expected_pkt: ",expected_pkt)
        for i in range(1000):
            self.dataplane.send(ports[2], str(pkt_from_p2_to_p2))
            wait_for_seconds(0.1)
        verify_packet(self, str(expected_pkt), ports[3])

class Sflow_Run_4_Setter_TwoDutCapture(SflowTest):
    """
    Test capture sflow packet
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg_sw1 = {}
        vlan_cfg_sw1['device-id'] = cfg.leaf0['id']
        sflow_cfg = {}
        sflow_cfg['device-id'] = [cfg.leaf0['id']]

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan = StaticVLAN(vlan_cfg)
        vlan.delete_DevieIdNoVerify({'device-id': cfg.leaf0['id']})
        vlan.delete_DevieIdNoVerify({'device-id': cfg.leaf1['id']})

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.113",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.111",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['ports'] = [
            {
                "port": 1,
                "native": 10,
                "mode": "access",
                "vlans": [
                    "10/untag"
                ]
            }
        ]
        vlan = StaticVLAN(vlan_cfg).build()

        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['ports'] = [
            {
                "port": 1,
                "native": 20,
                "mode": "access",
                "vlans": [
                    "20/untag"
                ]
            }
        ]
        vlan = StaticVLAN(vlan_cfg).build()

        sflow_cfg['device-id'] = cfg.leaf1['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.14",
            "max_payload_length": 200,
            "max_header_length": 64,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 1000
        }
        actual_device = sflow.build()


        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.14",
            "max_payload_length": 200,
            "max_header_length": 64,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 1000
        }
        actual_device = sflow.build()


        pkt_from_p2_to_p2 = simple_eth_packet(
            pktlen=120, 
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac']
        )
        expected_pkt = simple_eth_packet(
            pktlen=12,
            eth_type=0x0800,
            eth_dst=HOST3_MAC,
            eth_src=cfg.leaf1['mac']
        )
        #print("debug expected_pkt: ",expected_pkt)
        for i in range(500):
            self.dataplane.send(ports[2], str(pkt_from_p2_to_p2))
            wait_for_seconds(0.1)
        verify_packet(self, str(expected_pkt), ports[3])

        pkt_from_p0_to_p0 = simple_eth_packet(
            pktlen=120, 
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac']
        )
        expected_pkt = simple_eth_packet(
            pktlen=12,
            eth_type=0x0800,
            eth_dst=HOST3_MAC,
            eth_src=cfg.leaf0['mac']
        )
        #print("debug expected_pkt: ",expected_pkt)
        for i in range(500):
            self.dataplane.send(ports[0], str(pkt_from_p0_to_p0))
            wait_for_seconds(0.1)
        verify_packet(self, str(expected_pkt), ports[3])

class Sflow_Run_5_Setter_TwoDutCaptureByPacketLength(SflowTest):
    """
    Test capture sflow packet
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg_sw1 = {}
        vlan_cfg_sw1['device-id'] = cfg.leaf0['id']
        sflow_cfg = {}
        sflow_cfg['device-id'] = [cfg.leaf0['id']]

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan = StaticVLAN(vlan_cfg)
        vlan.delete_DevieIdNoVerify({'device-id': cfg.leaf0['id']})
        vlan.delete_DevieIdNoVerify({'device-id': cfg.leaf1['id']})

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.113",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.111",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['ports'] = [
            {
                "port": 1,
                "native": 10,
                "mode": "access",
                "vlans": [
                    "10/untag"
                ]
            }
        ]
        vlan = StaticVLAN(vlan_cfg).build()

        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['ports'] = [
            {
                "port": 1,
                "native": 20,
                "mode": "access",
                "vlans": [
                    "20/untag"
                ]
            }
        ]
        vlan = StaticVLAN(vlan_cfg).build()

        sflow_cfg['device-id'] = cfg.leaf1['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.14",
            "max_payload_length": 200,
            "max_header_length": 100,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 1000
        }
        actual_device = sflow.build()

        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.14",
            "max_payload_length": 300,
            "max_header_length": 200,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 1000
        }
        actual_device = sflow.build()


        pkt_from_p2_to_p2 = simple_eth_packet(
            pktlen=64, 
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host2['mac']
        )
        expected_pkt = simple_eth_packet(
            pktlen=12,
            eth_type=0x0800,
            eth_dst=HOST3_MAC,
            eth_src=cfg.leaf1['mac']
        )
        #print("debug expected_pkt: ",expected_pkt)
        for i in range(500):
            self.dataplane.send(ports[2], str(pkt_from_p2_to_p2))
            wait_for_seconds(0.1)
        verify_packet(self, str(expected_pkt), ports[3])
        verify_no_packet(self, str(expected_pkt), ports[1])

        pkt_from_p0_to_p0 = simple_eth_packet(
            pktlen=250, 
            eth_dst='ff:ff:ff:ff:ff:ff',
            eth_src=cfg.host0['mac']
        )
        expected_pkt = simple_eth_packet(
            pktlen=12,
            eth_type=0x0800,
            eth_dst=HOST3_MAC,
            eth_src=cfg.leaf0['mac']
        )
        #print("debug expected_pkt: ",expected_pkt)
        for i in range(500):
            self.dataplane.send(ports[0], str(pkt_from_p0_to_p0))
            wait_for_seconds(0.1)
        verify_packet(self, str(expected_pkt), ports[3])
        verify_no_packet(self, str(expected_pkt), ports[1])

class Sflow_Run_6_Setter_TwoDutReboot(SflowTest):
    """
    Test capture sflow packet
    """
    def runTest(self):
        ports = sorted(config["port_map"].keys())
        vlan_cfg = {}
        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg_sw1 = {}
        vlan_cfg_sw1['device-id'] = cfg.leaf0['id']
        sflow_cfg = {}
        sflow_cfg['device-id'] = [cfg.leaf0['id']]

        sflow = SFLOW(sflow_cfg)
        sflow.delete_deviceByIdNotVerify(cfg.leaf0['id'])
        sflow.delete_deviceByIdNotVerify(cfg.leaf1['id'])
        sflow.delete_deviceByIdNotVerify(cfg.spine0['id'])


        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan = StaticVLAN(vlan_cfg)
        vlan.delete_DevieIdNoVerify({'device-id': cfg.leaf0['id']})
        vlan.delete_DevieIdNoVerify({'device-id': cfg.leaf1['id']})

        vlan_cfg['device-id'] = cfg.leaf1['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.113",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        vlan_cfg['device-id'] = cfg.leaf0['id']
        vlan_cfg['vlans'] = [
            {
                "vlan": 1,
                "ip": "10.0.10.111",
                "mask": "255.255.255.0"
            }
        ]
        vlan = VLAN(vlan_cfg).build()

        sflow_cfg['device-id'] = cfg.leaf1['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.14",
            "max_payload_length": 200,
            "max_header_length": 100,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 10000
        }
        actual_device = sflow.build()

        sflow_cfg['device-id'] = cfg.leaf0['id']
        sflow_cfg['data'] = {
            "collector_ip": "10.0.10.14",
            "max_payload_length": 300,
            "max_header_length": 200,
            "polling_interval": 3,
            "sample_rate": 256,
            "port": [1],
            "duration": 10000
        }
        actual_device = sflow.build()

        rebootTest = RebootSwitch(cfg.leaf0['id'])
        rebootTest.reboot()

        rebootTest = RebootSwitch(cfg.leaf1['id'])
        rebootTest.reboot()

        time.sleep(180)
        actual_device = sflow.get_deviceById(cfg.leaf0['id'])
        assert(3 == actual_device["pollingInterval"]), "Verify pollingInterval fail by reboot(leaf0)"
        actual_device = sflow.get_deviceById(cfg.leaf1['id'])
        assert(3 == actual_device["pollingInterval"]), "Verify pollingInterval fail by reboot(leaf1)"