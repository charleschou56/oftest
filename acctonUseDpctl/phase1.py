import logging
import oftest.base_tests as base_tests
from oftest import config
from oftest.testutils import *
from util import *
from accton_util import convertIP4toStr as toIpV4Str
from accton_util import convertMACtoStr as toMacStr


class l3ucast_route(base_tests.SimpleDataPlane):
    """
    [L3 unicast route]
      Do unicast route and output to specified port

    Inject  eth 1/3 Tag2, SA000000112233, DA7072cf7cf3a3, SIP 192.168.3.2, DIP 192.168.2.2
    Output  eth 1/1 Tag3, SA 000004223355, DA 000004224466

    ./dpctl tcp:192.168.2.1:6633 flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10
    ./dpctl tcp:192.168.2.1:6633 flow-mod table=10,cmd=add,prio=101 in_port=1,vlan_vid=0x1002/0x1fff goto:20
    ./dpctl tcp:192.168.2.1:6633 flow-mod table=20,cmd=add,prio=201 in_port=1,vlan_vid=2/0xfff,eth_dst=70:72:cf:7c:f3:a3,eth_type=0x0800 goto:30
    ./dpctl tcp:192.168.2.1:6633 group-mod cmd=add,type=ind,group=0x30002 group=any,port=any,weight=0 output=2
    ./dpctl tcp:192.168.2.1:6633 group-mod cmd=add,type=ind,group=0x20000003 group=any,port=any,weight=0 set_field=eth_src=00:00:04:22:33:55,set_field=eth_dst=00:00:04:22:44:66,set_field=vlan_vid=3,group=0x30002
    ./dpctl tcp:192.168.2.1:6633 flow-mod table=30,cmd=add,prio=301 eth_type=0x0800,ip_dst=192.168.2.2/255.255.255.0 write:group=0x20000003 goto:60
    """
    def runTest(self):

        delete_all_flows(self.controller)
        delete_all_groups(self.controller)

        test_ports = sorted(config["port_map"].keys())

        input_port = test_ports[0]
        output_port = test_ports[1]

        apply_dpctl_mod(self, config, "meter-mod cmd=del,meter=0xffffffff")
        apply_dpctl_mod(self, config, "flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10")
        apply_dpctl_mod(self, config, "flow-mod table=10,cmd=add,prio=101 in_port="+str(input_port)+",vlan_vid=0x1002/0x1fff goto:20")
        apply_dpctl_mod(self, config, "flow-mod table=20,cmd=add,prio=201 in_port="+str(input_port)+",eth_dst=00:00:00:11:33:55,eth_type=0x0800,vlan_vid=2 goto:30")
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x3000"+str(output_port)+" group=any,port=any,weight=0 output="+str(output_port))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x20000003 group=any,port=any,weight=0 set_field=eth_src=00:00:04:22:33:55,set_field=eth_dst=00:00:04:22:44:66,set_field=vlan_vid=3,group=0x3000"+str(output_port))
        apply_dpctl_mod(self, config, "flow-mod table=30,cmd=add,prio=301 eth_type=0x0800,ip_dst=192.168.3.2/255.255.255.0 write:group=0x20000003 goto:60")

        input_pkt = simple_tcp_packet(pktlen=100,
                                       eth_dst='00:00:00:11:33:55',
                                       eth_src='00:00:00:11:22:33',
                                       ip_src='192.168.5.10',
                                       ip_dst='192.168.3.2',
                                       ip_ttl=64,
                                       vlan_vid=2,
                                       dl_vlan_enable=True)
        output_pkt = simple_tcp_packet(pktlen=100,
                                       eth_dst='00:00:04:22:44:66',
                                       eth_src='00:00:04:22:33:55',
                                       ip_src='192.168.5.10',
                                       ip_dst='192.168.3.2',
                                       ip_ttl=63,
                                       vlan_vid=3,
                                       dl_vlan_enable=True)

        self.dataplane.send(input_port, str(input_pkt))
        verify_packet(self, str(output_pkt), output_port)


class l3ucast_route6(base_tests.SimpleDataPlane):
    """
    [L3 IPv6 unicast route]
      Do unicast route and output to specified port

    Inject  eth 1/3 Tag2, SA000000112233, DA7072cf7cf3a3, SIP 2014::2, DIP 2014::1
    Output  eth 1/1 Tag2, SA 000004223355, DA 000004224466

    ./dpctl tcp:192.168.1.1:6633 flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=10,cmd=add,prio=101 in_port=3,vlan_vid=0x1002/0x1fff goto:20
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=20,cmd=add,prio=201 in_port=3,vlan_vid=2/0xfff,eth_dst=70:72:cf:7c:f3:a3,eth_type=0x86dd goto:30
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=ind,group=0x20001 group=any,port=any,weight=0 output=1
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=ind,group=0x20000001 group=any,port=any,weight=0 set_field=eth_src=00:00:04:22:33:55,set_field=eth_dst=00:00:04:22:44:66,set_field=vlan_vid=2,group=0x20001
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=30,cmd=add,prio=301 eth_type=0x86dd,ipv6_dst=2014::1/64 write:group=0x20000001 goto:60
    """
    def runTest(self):
        delete_all_flows(self.controller)
        delete_all_groups(self.controller)

        test_ports = sorted(config["port_map"].keys())

        input_port = test_ports[0]
        output_port = test_ports[1]

        apply_dpctl_mod(self, config, "meter-mod cmd=del,meter=0xffffffff")
        apply_dpctl_mod(self, config, "flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10")
        apply_dpctl_mod(self, config, "flow-mod table=10,cmd=add,prio=101 in_port="+str(input_port)+",vlan_vid=0x1002/0x1fff goto:20")
        apply_dpctl_mod(self, config, "flow-mod table=20,cmd=add,prio=201 in_port="+str(input_port)+",eth_dst=70:72:cf:7c:f3:a3,eth_type=0x86dd goto:30")
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x2000"+str(output_port)+" group=any,port=any,weight=0 output="+str(output_port))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x20000001 group=any,port=any,weight=0 set_field=eth_src=00:00:04:22:33:55,set_field=eth_dst=00:00:04:22:44:66,set_field=vlan_vid=2,group=0x2000"+str(output_port))
        apply_dpctl_mod(self, config, "flow-mod table=30,cmd=add,prio=301 eth_type=0x86dd,ipv6_dst=2014::1/64 write:group=0x20000001 goto:60")

        input_pkt = simple_packet(
                '70 72 cf 7c f3 a3 00 00 00 11 22 33 81 00 00 02 '
                '86 dd 60 00 00 00 00 08 11 7f 20 14 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 02 20 14 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 01 00 0d 00 07 00 08 '
                'bf 9f 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

        output_pkt = simple_packet(
                '00 00 04 22 44 66 00 00 04 22 33 55 81 00 00 02 '
                '86 dd 60 00 00 00 00 08 11 7e 20 14 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 02 20 14 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 01 00 0d 00 07 00 08 '
                'bf 9f 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

        self.dataplane.send(input_port, str(input_pkt))
        verify_packet(self, str(output_pkt), output_port)


class l3mcast_route(base_tests.SimpleDataPlane):
    """
    [L3 multicast route]
      Do multicast route and output to specified ports

    Inject  eth 1/1 Tag2, SA000000112233, DA01005E404477, SIP 192.168.3.100, DIP 224.0.2.2
    Output  eth 1/2 Tag2, SA000000112233, DA01005E404477, SIP 192.168.3.100, DIP 224.0.2.2
    Output  eth 1/3 Tag6, SA000000336699, DA01005E404477, SIP 192.168.3.100, DIP 224.0.2.2

    ./dpctl tcp:0.0.0.0:6633 flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10
    ./dpctl tcp:0.0.0.0:6633 flow-mod table=10,cmd=add,prio=101 in_port=3,vlan_vid=0x1002/0x1fff goto:20
    ./dpctl tcp:0.0.0.0:6633 flow-mod table=20,cmd=add,prio=201 eth_dst=01:00:5e:40:44:77/ff:ff:ff:80:00:00,eth_type=0x0800 goto:40
    ./dpctl tcp:0.0.0.0:6633 group-mod cmd=add,type=ind,group=0x20002 group=any,port=any,weight=0 output=2
    ./dpctl tcp:0.0.0.0:6633 group-mod cmd=add,type=ind,group=0x60003 group=any,port=any,weight=0 output=3
    ./dpctl tcp:0.0.0.0:6633 group-mod cmd=add,type=ind,group=0x50000002 group=any,port=any,weight=0 set_field=eth_src=00:00:00:33:66:99,set_field=vlan_vid=6,group=0x60003
    ./dpctl tcp:0.0.0.0:6633 group-mod cmd=add,type=all,group=0x60020001 group=any,port=any,weight=0 group=0x20002 group=any,port=any,weight=0 group=0x50000002
    ./dpctl tcp:0.0.0.0:6633 flow-mod table=40,cmd=add,prio=401 eth_type=0x0800,ip_src=192.168.3.100,ip_dst=224.0.2.2,vlan_vid=2 write:group=0x60020001 goto:60
    """
    def runTest(self):
        delete_all_flows(self.controller)
        delete_all_groups(self.controller)

        test_ports = sorted(config["port_map"].keys())

        input_port = test_ports[0]
        output_port1 = test_ports[1]
        output_port2 = test_ports[2]

        apply_dpctl_mod(self, config, "meter-mod cmd=del,meter=0xffffffff")
        apply_dpctl_mod(self, config, "flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10")
        apply_dpctl_mod(self, config, "flow-mod table=10,cmd=add,prio=101 in_port="+str(input_port)+",vlan_vid=0x1002/0x1fff goto:20")
        apply_dpctl_mod(self, config, "flow-mod table=20,cmd=add,prio=201 eth_dst=01:00:5e:40:44:77/ff:ff:ff:80:00:00,eth_type=0x0800 goto:40")
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x2000"+str(output_port1)+" group=any,port=any,weight=0 output="+str(output_port1))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x6000"+str(output_port2)+" group=any,port=any,weight=0 output="+str(output_port2))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x50000002 group=any,port=any,weight=0 set_field=eth_src=00:00:00:33:66:99,set_field=vlan_vid=6,group=0x6000"+str(output_port2))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=all,group=0x60020001 group=any,port=any,weight=0 group=0x2000"+str(output_port1)+" group=any,port=any,weight=0 group=0x50000002")
        apply_dpctl_mod(self, config, "flow-mod table=40,cmd=add,prio=401 eth_type=0x0800,ip_src=192.168.3.100,ip_dst=224.0.2.2,vlan_vid=2 write:group=0x60020001 goto:60")

        input_pkt = simple_tcp_packet(pktlen=100,
                                       eth_dst='01:00:5e:40:44:77',
                                       eth_src='00:00:00:11:22:33',
                                       ip_src='192.168.3.100',
                                       ip_dst='224.0.2.2',
                                       ip_ttl=64,
                                       vlan_vid=2,
                                       dl_vlan_enable=True)

        output_pkt1 = input_pkt

        output_pkt2 = simple_tcp_packet(pktlen=100,
                                       eth_dst='01:00:5e:40:44:77',
                                       eth_src='00:00:00:33:66:99',
                                       ip_src='192.168.3.100',
                                       ip_dst='224.0.2.2',
                                       ip_ttl=63,
                                       vlan_vid=6,
                                       dl_vlan_enable=True)

        self.dataplane.send(input_port, str(input_pkt))
        verify_packet(self, str(output_pkt1), output_port1)
        verify_packet(self, str(output_pkt2), output_port2)

class l3mcast_route2(base_tests.SimpleDataPlane):
    """
    [L3 multicast route]
      Do multicast route and output to specified ports

    Inject  eth 1/1 Tag2, SA000000112233, DA01005E404477, SIP 192.168.3.100, DIP 224.0.2.2
    Output  eth 1/2 Tag5, SA000000224466, DA01005E404477, SIP 192.168.3.100, DIP 224.0.2.2
    Output  eth 1/3 Tag6, SA000000336699, DA01005E404477, SIP 192.168.3.100, DIP 224.0.2.2

    ./dpctl tcp:0.0.0.0:6633 flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10
    ./dpctl tcp:0.0.0.0:6633 flow-mod table=10,cmd=add,prio=101 in_port=3,vlan_vid=0x1002/0x1fff goto:20
    ./dpctl tcp:0.0.0.0:6633 flow-mod table=20,cmd=add,prio=201 eth_dst=01:00:5e:40:44:77/ff:ff:ff:80:00:00,eth_type=0x0800 goto:40
    ./dpctl tcp:0.0.0.0:6633 group-mod cmd=add,type=ind,group=0x50003 group=any,port=any,weight=0 output=2
    ./dpctl tcp:0.0.0.0:6633 group-mod cmd=add,type=ind,group=0x60003 group=any,port=any,weight=0 output=3
    ./dpctl tcp:0.0.0.0:6633 group-mod cmd=add,type=ind,group=0x50000001 group=any,port=any,weight=0 set_field=eth_src=00:00:00:22:44:66,set_field=vlan_vid=5,group=0x50002
    ./dpctl tcp:0.0.0.0:6633 group-mod cmd=add,type=ind,group=0x50000002 group=any,port=any,weight=0 set_field=eth_src=00:00:00:33:66:99,set_field=vlan_vid=6,group=0x60003
    ./dpctl tcp:0.0.0.0:6633 group-mod cmd=add,type=all,group=0x60020001 group=any,port=any,weight=0 group=0x50000001 group=any,port=any,weight=0 group=0x50000002
    ./dpctl tcp:0.0.0.0:6633 flow-mod table=40,cmd=add,prio=401 eth_type=0x0800,ip_src=192.168.3.100,ip_dst=224.0.2.2,vlan_vid=2 write:group=0x60020001 goto:60
    """
    def runTest(self):
        delete_all_flows(self.controller)
        delete_all_groups(self.controller)

        test_ports = sorted(config["port_map"].keys())

        input_port = test_ports[0]
        output_port1 = test_ports[1]
        output_port2 = test_ports[2]

        apply_dpctl_mod(self, config, "meter-mod cmd=del,meter=0xffffffff")
        apply_dpctl_mod(self, config, "flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10")
        apply_dpctl_mod(self, config, "flow-mod table=10,cmd=add,prio=101 in_port="+str(input_port)+",vlan_vid=0x1002/0x1fff goto:20")
        apply_dpctl_mod(self, config, "flow-mod table=20,cmd=add,prio=201 eth_dst=01:00:5e:40:44:77/ff:ff:ff:80:00:00,eth_type=0x0800 goto:40")
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x5000"+str(output_port1)+" group=any,port=any,weight=0 output="+str(output_port1))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x6000"+str(output_port2)+" group=any,port=any,weight=0 output="+str(output_port2))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x50000001 group=any,port=any,weight=0 set_field=eth_src=00:00:00:22:44:66,set_field=vlan_vid=5,group=0x5000"+str(output_port1))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x50000002 group=any,port=any,weight=0 set_field=eth_src=00:00:00:33:66:99,set_field=vlan_vid=6,group=0x6000"+str(output_port2))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=all,group=0x60020001 group=any,port=any,weight=0 group=0x50000001 group=any,port=any,weight=0 group=0x50000002")
        apply_dpctl_mod(self, config, "flow-mod table=40,cmd=add,prio=401 eth_type=0x0800,ip_src=192.168.3.100,ip_dst=224.0.2.2,vlan_vid=2 write:group=0x60020001 goto:60")

        input_pkt = simple_tcp_packet(pktlen=100,
                                       eth_dst='01:00:5e:40:44:77',
                                       eth_src='00:00:00:11:22:33',
                                       ip_src='192.168.3.100',
                                       ip_dst='224.0.2.2',
                                       ip_ttl=64,
                                       vlan_vid=2,
                                       dl_vlan_enable=True)

        output_pkt1 = simple_tcp_packet(pktlen=100,
                                       eth_dst='01:00:5e:40:44:77',
                                       eth_src='00:00:00:22:44:66',
                                       ip_src='192.168.3.100',
                                       ip_dst='224.0.2.2',
                                       ip_ttl=63,
                                       vlan_vid=5,
                                       dl_vlan_enable=True)

        output_pkt2 = simple_tcp_packet(pktlen=100,
                                       eth_dst='01:00:5e:40:44:77',
                                       eth_src='00:00:00:33:66:99',
                                       ip_src='192.168.3.100',
                                       ip_dst='224.0.2.2',
                                       ip_ttl=63,
                                       vlan_vid=6,
                                       dl_vlan_enable=True)

        self.dataplane.send(input_port, str(input_pkt))
        verify_packet(self, str(output_pkt1), output_port1)
        verify_packet(self, str(output_pkt2), output_port2)


class l3mcast_route6(base_tests.SimpleDataPlane):
    """
    [L3 IPv6 multicast route]
      Do multicast route and output to specified ports

    Inject  eth 1/5 Tag2, SA000000112233, DA333300224477, SIP 2014::2, DIP ff01::2
    Output  eth 1/1 Tag2, original
    Output  eth 1/3 Tag3, SA000005336699, DA333300224477, SIP 2014::2, DIP ff01::2

    ./dpctl tcp:192.168.1.1:6633 flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=10,cmd=add,prio=101 in_port=5,vlan_vid=0x1002/0x1fff goto:20
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=20,cmd=add,prio=201 eth_dst=33:33:00:22:44:77/ff:ff:00:00:00:00,eth_type=0x86dd goto:40
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=ind,group=0x20001 group=any,port=any,weight=0 output=1
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=ind,group=0x30003 group=any,port=any,weight=0 output=3
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=ind,group=0x50000003 group=any,port=any,weight=0 set_field=eth_src=00:00:05:22:33:99,set_field=vlan_vid=3,group=0x30003
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=all,group=0x60020001 group=any,port=any,weight=0 group=0x20001 group=any,port=any,weight=0 group=0x50000003
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=40,cmd=add,prio=501 eth_type=0x86dd,ipv6_dst=ff01::2,vlan_vid=2 write:group=0x60020001 goto:60
    """
    def runTest(self):
        delete_all_flows(self.controller)
        delete_all_groups(self.controller)

        test_ports = sorted(config["port_map"].keys())

        input_port = test_ports[0]
        output_port = test_ports[1]
        output_port2 = test_ports[2]

        apply_dpctl_mod(self, config, "meter-mod cmd=del,meter=0xffffffff")
        apply_dpctl_mod(self, config, "flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10")
        apply_dpctl_mod(self, config, "flow-mod table=10,cmd=add,prio=101 in_port="+str(input_port)+",vlan_vid=0x1002/0x1fff goto:20")
        apply_dpctl_mod(self, config, "flow-mod table=20,cmd=add,prio=201 eth_dst=33:33:00:22:44:77/ff:ff:00:00:00:00,eth_type=0x86dd goto:40")
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x2000"+str(output_port)+" group=any,port=any,weight=0 output="+str(output_port))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x3000"+str(output_port2)+" group=any,port=any,weight=0 output="+str(output_port2))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x50000003 group=any,port=any,weight=0 set_field=eth_src=00:00:05:22:33:99,set_field=vlan_vid=3,group=0x3000"+str(output_port2))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=all,group=0x60020001 group=any,port=any,weight=0 group=0x2000"+str(output_port)+" group=any,port=any,weight=0 group=0x50000003")
        apply_dpctl_mod(self, config, "flow-mod table=40,cmd=add,prio=401 eth_type=0x86dd,ipv6_dst=ff01::2,vlan_vid=2 write:group=0x60020001 goto:60")

        input_pkt = simple_packet(
                '33 33 00 22 44 77 00 00 00 11 22 33 81 00 00 02 '
                '86 dd 60 00 00 00 00 26 3b 7f 20 14 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 01 ff 01 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

        output_pkt = simple_packet(
                '33 33 00 22 44 77 00 00 00 11 22 33 81 00 00 02 '
                '86 dd 60 00 00 00 00 26 3b 7f 20 14 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 01 ff 01 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

        output_pkt2 = simple_packet(
                '33 33 00 22 44 77 00 00 05 22 33 99 81 00 00 03 '
                '86 dd 60 00 00 00 00 26 3b 7e 20 14 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 01 ff 01 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

        self.dataplane.send(input_port, str(input_pkt))
        verify_packet(self, str(output_pkt), output_port)
        verify_packet(self, str(output_pkt2), output_port2)


class bridge_ucast(base_tests.SimpleDataPlane):
    """
    [Bridge unicast]
      Do unicast bridge

    Inject  eth 1/1 Tag2, SA000000112233, DA000000224477, SIP 192.168.2.1, DIP 192.168.2.2
    Output  eth 1/3 untag

    ./dpctl tcp:192.168.1.1:6633 flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=10,cmd=add,prio=101 in_port=1,vlan_vid=0x1002/0x1fff goto:20
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=ind,group=0x20003 group=any,port=any,weight=0 pop_vlan,output=3
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=50,cmd=add,prio=501 vlan_vid=2,eth_dst=00:00:00:22:44:77 write:group=0x20003 goto:60
    """
    def runTest(self):
        delete_all_flows(self.controller)
        delete_all_groups(self.controller)

        test_ports = sorted(config["port_map"].keys())

        input_port = test_ports[0]
        output_port = test_ports[1]

        apply_dpctl_mod(self, config, "meter-mod cmd=del,meter=0xffffffff")
        apply_dpctl_mod(self, config, "flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10")
        apply_dpctl_mod(self, config, "flow-mod table=10,cmd=add,prio=101 in_port="+str(input_port)+",vlan_vid=0x1002/0x1fff goto:20")
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x2000"+str(output_port)+" group=any,port=any,weight=0 pop_vlan,output="+str(output_port))
        apply_dpctl_mod(self, config, "flow-mod table=50,cmd=add,prio=501 vlan_vid=2,eth_dst=00:00:00:22:44:77 write:group=0x2000"+str(output_port)+" goto:60")

        input_pkt = simple_packet(
                '00 00 00 22 44 77 00 00 00 11 22 33 81 00 00 02 '
                '08 00 45 00 00 4e 04 d2 00 00 7f 00 b1 8a c0 a8 '
                '02 01 c0 a8 02 02 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

        output_pkt = simple_packet(
                '00 00 00 22 44 77 00 00 00 11 22 33 08 00 45 00 '
                '00 4e 04 d2 00 00 7f 00 b1 8a c0 a8 02 01 c0 a8 '
                '02 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00')

        self.dataplane.send(input_port, str(input_pkt))
        verify_packet(self, str(output_pkt), output_port)


class bridge_mcast(base_tests.SimpleDataPlane):
    """
    [Bridge multicast]
      Do multicast bridge

    Inject  eth 1/5 Tag2, SA000000112233, DA110000224477, SIP 192.168.2.1, DIP 192.168.2.2
    Output  eth 1/1 Tag2, SA000000112233, DA110000224477, SIP 192.168.2.1, DIP 192.168.2.2
    Output  eth 1/3 untag

    ./dpctl tcp:192.168.1.1:6633 flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=10,cmd=add,prio=101 in_port=5,vlan_vid=0x1002/0x1fff goto:20
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=ind,group=0x20001 group=any,port=any,weight=0 output=1
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=ind,group=0x20003 group=any,port=any,weight=0 pop_vlan,output=3
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=all,group=0x30020001 group=any,port=any,weight=0 group=0x20001 group=any,port=any,weight=0 group=0x20003
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=50,cmd=add,prio=601 vlan_vid=2,eth_dst=11:00:00:22:44:77 write:group=0x30020001 goto:60
    """
    def runTest(self):
        delete_all_flows(self.controller)
        delete_all_groups(self.controller)

        test_ports = sorted(config["port_map"].keys())

        input_port = test_ports[0]
        output_port = test_ports[1]
        output_port2 = test_ports[2]

        apply_dpctl_mod(self, config, "meter-mod cmd=del,meter=0xffffffff")
        apply_dpctl_mod(self, config, "flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10")
        apply_dpctl_mod(self, config, "flow-mod table=10,cmd=add,prio=101 in_port="+str(input_port)+",vlan_vid=0x1002/0x1fff goto:20")
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x2000"+str(output_port)+" group=any,port=any,weight=0 output="+str(output_port))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x2000"+str(output_port2)+" group=any,port=any,weight=0 pop_vlan,output="+str(output_port2))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=all,group=0x30020001 group=any,port=any,weight=0 group=0x2000"+str(output_port)+" group=any,port=any,weight=0 group=0x2000"+str(output_port2))
        apply_dpctl_mod(self, config, "flow-mod table=50,cmd=add,prio=501 vlan_vid=2,eth_dst=11:00:00:22:44:77 write:group=0x30020001 goto:60")

        input_pkt = simple_packet(
                '11 00 00 22 44 77 00 00 00 11 22 33 81 00 00 02 '
                '08 00 45 00 00 4e 04 d2 00 00 7f 00 b1 8a c0 a8 '
                '02 01 c0 a8 02 02 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

        output_pkt = simple_packet(
                '11 00 00 22 44 77 00 00 00 11 22 33 81 00 00 02 '
                '08 00 45 00 00 4e 04 d2 00 00 7f 00 b1 8a c0 a8 '
                '02 01 c0 a8 02 02 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

        output_pkt2 = simple_packet(
                '11 00 00 22 44 77 00 00 00 11 22 33 08 00 45 00 '
                '00 4e 04 d2 00 00 7f 00 b1 8a c0 a8 02 01 c0 a8 '
                '02 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00')

        self.dataplane.send(input_port, str(input_pkt))
        verify_packet(self, str(output_pkt), output_port)
        verify_packet(self, str(output_pkt2), output_port2)


class bridge_dlf(base_tests.SimpleDataPlane):
    """
    [Bridge DLF]
      Do DLF bridge

    Inject  eth 1/5 Tag2, SA000000112233, DA110000224466, SIP 192.168.2.1, DIP 192.168.2.2
    Output  eth 1/1 Tag2, SA000000112233, DA110000224477, SIP 192.168.2.1, DIP 192.168.2.2
    Output  eth 1/3 untag

    ./dpctl tcp:192.168.1.1:6633 flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=10,cmd=add,prio=101 in_port=5,vlan_vid=0x1002/0x1fff goto:20
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=ind,group=0x20001 group=any,port=any,weight=0 output=1
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=ind,group=0x20003 group=any,port=any,weight=0 pop_vlan,output=3
    ./dpctl tcp:192.168.1.1:6633 group-mod cmd=add,type=all,group=0x40020001 group=any,port=any,weight=0 group=0x20001 group=any,port=any,weight=0 group=0x20003
    ./dpctl tcp:192.168.1.1:6633 flow-mod table=50,cmd=add,prio=601 vlan_vid=2 write:group=0x40020001 goto:60
    """
    def runTest(self):
        delete_all_flows(self.controller)
        delete_all_groups(self.controller)

        test_ports = sorted(config["port_map"].keys())

        input_port = test_ports[0]
        output_port = test_ports[1]
        output_port2 = test_ports[2]

        apply_dpctl_mod(self, config, "meter-mod cmd=del,meter=0xffffffff")
        apply_dpctl_mod(self, config, "flow-mod table=0,cmd=add,prio=1 in_port=0/0xffff0000 goto:10")
        apply_dpctl_mod(self, config, "flow-mod table=10,cmd=add,prio=101 in_port="+str(input_port)+",vlan_vid=0x1002/0x1fff goto:20")
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x2000"+str(output_port)+" group=any,port=any,weight=0 output="+str(output_port))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=ind,group=0x2000"+str(output_port2)+" group=any,port=any,weight=0 pop_vlan,output="+str(output_port2))
        apply_dpctl_mod(self, config, "group-mod cmd=add,type=all,group=0x40020001 group=any,port=any,weight=0 group=0x2000"+str(output_port)+" group=any,port=any,weight=0 group=0x2000"+str(output_port2))
        apply_dpctl_mod(self, config, "flow-mod table=50,cmd=add,prio=601 vlan_vid=2 write:group=0x40020001 goto:60")

        input_pkt = simple_packet(
                '00 00 00 22 44 66 00 00 00 11 22 33 81 00 00 02 '
                '08 00 45 00 00 4e 04 d2 00 00 7f 00 b1 8a c0 a8 '
                '02 01 c0 a8 02 02 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

        output_pkt = simple_packet(
                '00 00 00 22 44 66 00 00 00 11 22 33 81 00 00 02 '
                '08 00 45 00 00 4e 04 d2 00 00 7f 00 b1 8a c0 a8 '
                '02 01 c0 a8 02 02 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

        output_pkt2 = simple_packet(
                '00 00 00 22 44 66 00 00 00 11 22 33 08 00 45 00 '
                '00 4e 04 d2 00 00 7f 00 b1 8a c0 a8 02 01 c0 a8 '
                '02 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
                '00 00 00 00 00 00 00 00 00 00 00 00')

        self.dataplane.send(input_port, str(input_pkt))
        verify_packet(self, str(output_pkt), output_port)
        verify_packet(self, str(output_pkt2), output_port2)

