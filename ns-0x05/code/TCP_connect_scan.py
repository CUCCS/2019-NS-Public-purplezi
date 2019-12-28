#!/usr/bin/python
# from scapy.all import *
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP,TCP,sr1,RandShort,send,ICMP,UDP,Raw

dst_ip = "172.16.111.139"
src_port = RandShort()
dst_port = 80

tcp_connect_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=10)
if(str(type(tcp_connect_scan_resp))=="<type 'NoneType'>"):
    print("Filtered")
elif(tcp_connect_scan_resp.haslayer(TCP)):
    if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
        send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="AR"),timeout=10)
        print("Open")
    elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
        print("Closed")