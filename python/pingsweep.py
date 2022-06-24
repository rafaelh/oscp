#! /usr/bin/env python3

import sys
from scapy.all import *

def ping(host):
    icmp = IP(dst=host)/ICMP()
    resp = sr1(icmp,timeout=10)
    if resp == None:
        print(host + " is down")
    else:
        print(host + " is up")

for i in range(1,255):
    ping('10.11.1.{}'.format(i))
