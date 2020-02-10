"""
ref: http://docs.python-requests.org/zh_CN/latest/user/quickstart.html

Test SPAN Rest API.

Test environment

    +--------+     +--------+
    | spine0 |     | spine1 |
    +--------+     +--------+
   49 |  | 50      49 |  | 50
      |  +------------+  |
   49 |  | 50      49 |  | 50
    +--------+     +--------+
    |  leaf0 |     |  leaf1 |
    +--------+     +--------+
      |    |         |    |
      p0   p1        p2   p3
      |    |         |    |
    host0 host1    host2 host3

p0: port 46 of leaf0
p1: port 48 of leaf0
p2: port 46 of leaf1
p3: port 48 of leaf1

"""

import oftest.base_tests as base_tests
import config as cfg
import requests
import time
import utils
from oftest import config
from oftest.testutils import *
from utils import *

URL = cfg.API_BASE_URL
LOGIN = cfg.LOGIN
AUTH_TOKEN = 'BASIC ' + LOGIN
GET_HEADER = {'Authorization': AUTH_TOKEN}
POST_HEADER = {'Authorization': AUTH_TOKEN, 'Content-Type': 'application/json'}

class SPANTest(base_tests.SimpleDataPlane):
    def setUp(self):
        base_tests.SimpleDataPlane.setUp(self)

        setup_configuration()
        self.port_configuration()

    def tearDown(self):
        base_tests.SimpleDataPlane.tearDown(self)

    def port_configuration(self):
        cfg.leaf0['port46']  = (
            Port(cfg.leaf0['front_port'][0])
            .tagged(False)
            .nos(cfg.leaf0['nos'])
        )
        cfg.leaf0['port48'] = (
            Port(cfg.leaf0['front_port'][1])
            .tagged(False)
            .nos(cfg.leaf0['nos'])
        )
        cfg.leaf1['port46'] = (
            Port(cfg.leaf1['front_port'][0])
            .tagged(False)
            .nos(cfg.leaf1['nos'])
        )
        cfg.leaf1['port48'] = (
            Port(cfg.leaf1['front_port'][1])
            .tagged(False)
            .nos(cfg.leaf1['nos'])
        )

class SetAndGetTest(SPANTest):
    """
    Test set and get SPAN rest API
    """

    def runTest(self):
        session_id = 1
        source_port = 46
        target_port = 48
        direction = 'both'

        span = (
            SPAN(session_id)
            .source(cfg.leaf0['id'], source_port, direction)
            .target(cfg.leaf0['id'], target_port)
            .build()
        )

        actual_session = span.get_session(session_id)
        assert(span._source['device_id'] == actual_session['src']['device_id'])
        assert(span._source['port'] == actual_session['src']['port'])
        assert(span._source['direction'] == actual_session['src']['direction'])
        assert(span._target['device_id'] == actual_session['target']['device_id'])
        assert(span._target['port'] == actual_session['target']['port'])

        span.destroy()

class NoSPANConfigTest(SPANTest):
    """
    Test situation without SAPN config
    """

    def runTest(self):
        ports = sorted(config["port_map"].keys())

        cfg.host0['ip'] = '192.168.10.10'
        cfg.host1['ip'] = '192.168.10.20'

        pkt_from_src = simple_tcp_packet(
            pktlen=68,
            dl_vlan_enable=True,
            vlan_vid=20,
            eth_dst=cfg.host1['mac'],
            eth_src=cfg.host0['mac'],
            ip_dst=cfg.host1['ip'],
            ip_src=cfg.host0['ip']
        )

        # check monitor status from source to target
        self.dataplane.send(ports[0], str(pkt_from_src))
        verify_no_packet(self, str(pkt_from_src), ports[1])
        verify_no_packet(self, str(pkt_from_src), ports[2])
        verify_no_packet(self, str(pkt_from_src), ports[3])


class SameLeafDescendingDirectionTest(SPANTest):
    """
    Test SPAN descending direction in same leaf
    """

    def runTest(self):
        ports = sorted(config["port_map"].keys())

        session_id = 1
        source_port = 46
        target_port = 48

        for direction in ['rx', 'both']:
            span = (
                SPAN(session_id)
                .source(cfg.leaf0['id'], source_port, direction)
                .target(cfg.leaf0['id'], target_port)
                .build()
            )

            wait_for_system_process()

            cfg.host0['ip'] = '192.168.10.10'
            cfg.host1['ip'] = '192.168.10.20'

            pkt_from_src = simple_tcp_packet(
                pktlen=68,
                dl_vlan_enable=True,
                vlan_vid=20,
                eth_dst=cfg.host1['mac'],
                eth_src=cfg.host0['mac'],
                ip_dst=cfg.host1['ip'],
                ip_src=cfg.host0['ip']
            )

            # check monitor status from source to target
            self.dataplane.send(ports[0], str(pkt_from_src))
            verify_packet(self, str(pkt_from_src), ports[1])
            verify_no_packet(self, str(pkt_from_src), ports[2])

            # clear queue packet
            self.dataplane.flush()

            span.destroy()

            wait_for_system_process()

class SameLeafUplinkDirectionTest(SPANTest):
    """
    Test SPAN uplink direction in same leaf
    """

    def runTest(self):
        ports = sorted(config["port_map"].keys())

        s1_vlan_id = 10

        t1 = (
            Tenant('t1')
            .segment('s1', 'vlan', [], s1_vlan_id)
            .segment_member('s1', [cfg.leaf0['port48'].name], cfg.leaf0['id'])
            .segment_member('s1', [cfg.leaf1['port48'].name], cfg.leaf1['id'])
            .build()
        )

        session_id = 1
        source_port = 48
        target_port = 46

        for direction in ['tx', 'both']:
            span = (
                SPAN(session_id)
                .source(cfg.leaf0['id'], source_port, direction)
                .target(cfg.leaf0['id'], target_port)
                .build()
            )

            wait_for_system_stable()

            cfg.host1['ip'] = '192.168.10.10'
            cfg.host3['ip'] = '192.168.10.20'

            pkt_from_p3_to_p1 = simple_tcp_packet(
                pktlen=68,
                dl_vlan_enable=True,
                vlan_vid=s1_vlan_id,
                eth_dst=cfg.host1['mac'],
                eth_src=cfg.host3['mac'],
                ip_dst=cfg.host1['ip'],
                ip_src=cfg.host3['ip']
            )

            expected_pkt_from_p1 = simple_tcp_packet(
                pktlen=64,
                eth_dst=cfg.host1['mac'],
                eth_src=cfg.host3['mac'],
                ip_dst=cfg.host1['ip'],
                ip_src=cfg.host3['ip']
            )

            # check monitor status from source to target
            self.dataplane.send(ports[3], str(pkt_from_p3_to_p1))
            # monitor port shall receive the packet
            verify_packet(self, str(pkt_from_p3_to_p1), ports[0])
            verify_packet(self, str(expected_pkt_from_p1), ports[1])

            # clear queue packet
            self.dataplane.flush()

            span.destroy()

            wait_for_system_process()

        t1.destroy()

class DifferentDescendingDirectionLeafTest(SPANTest):
    """
    Test SPAN descending direction in different leaf
    """

    def runTest(self):
        ports = sorted(config["port_map"].keys())

        session_id = 1
        source_port = 46
        target_port = 46
        direction = 'rx'

        for direction in ['rx', 'both']:
            span = (
                SPAN(session_id)
                .source(cfg.leaf0['id'], source_port, direction)
                .target(cfg.leaf1['id'], target_port)
                .build()
            )

            wait_for_system_stable()

            cfg.host0['ip'] = '192.168.10.10'
            cfg.host1['ip'] = '192.168.10.20'

            pkt_from_src = simple_tcp_packet(
                pktlen=68,
                dl_vlan_enable=True,
                vlan_vid=20,
                eth_dst=cfg.host1['mac'],
                eth_src=cfg.host0['mac'],
                ip_dst=cfg.host1['ip'],
                ip_src=cfg.host0['ip']
            )

            # check monitor status from source to target
            self.dataplane.send(ports[0], str(pkt_from_src))
            verify_no_packet(self, str(pkt_from_src), ports[1])
            verify_packet(self, str(pkt_from_src), ports[2])

            # clear queue packet
            self.dataplane.flush()

            span.destroy()

            wait_for_system_process()


class DifferentLeafUplinkDirectionTest(SPANTest):
    """
    Test SPAN uplink direction in different leaf
    """

    def runTest(self):
        ports = sorted(config["port_map"].keys())

        s1_vlan_id = 10

        t1 = (
            Tenant('t1')
            .segment('s1', 'vlan', [], s1_vlan_id)
            .segment_member('s1', [cfg.leaf1['port46'].name, cfg.leaf1['port48'].name], cfg.leaf1['id'])
            .build()
        )

        session_id = 1
        source_port = 48
        target_port = 46

        for direction in ['tx', 'both']:
            span = (
                SPAN(session_id)
                .source(cfg.leaf1['id'], source_port, direction)
                .target(cfg.leaf0['id'], target_port)
                .build()
            )

            wait_for_system_stable()

            cfg.host2['ip'] = '192.168.10.10'
            cfg.host3['ip'] = '192.168.10.20'

            pkt_from_p2_to_p3 = simple_tcp_packet(
                pktlen=68,
                dl_vlan_enable=True,
                vlan_vid=s1_vlan_id,
                eth_dst=cfg.host3['mac'],
                eth_src=cfg.host2['mac'],
                ip_dst=cfg.host3['ip'],
                ip_src=cfg.host2['ip']
            )

            expected_pkt_from_p3 = simple_tcp_packet(
                pktlen=64,
                eth_dst=cfg.host3['mac'],
                eth_src=cfg.host2['mac'],
                ip_dst=cfg.host3['ip'],
                ip_src=cfg.host2['ip']
            )

            # check monitor status from source to target
            self.dataplane.send(ports[2], str(pkt_from_p2_to_p3))
            # monitor port shall receive the packet
            verify_packet(self, str(pkt_from_p2_to_p3), ports[0])
            verify_packet(self, str(expected_pkt_from_p3), ports[3])

            # clear queue packet
            self.dataplane.flush()

            span.destroy()

            wait_for_system_process()

        t1.destroy()