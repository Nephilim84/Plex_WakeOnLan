#!/usr/bin/env python

#pip install getmac
#pip install wakeonlan
from getmac import get_mac_address
from wakeonlan import send_magic_packet
from time import sleep
import socket, sys, signal
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# this is just to make the output look nice
formatter = logging.Formatter(fmt="%(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")

# this logs to stdout and I think it is flushed immediately
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('test')

#from pymystrom.switch import MyStromSwitch
#import asyncio

import requests

MYSTROM_SWITCH_IP = '192.168.1.52'
RPI4_IP = "192.168.1.2"
WOL_IP = "192.168.1.101"
WOL_PORT = 9
PLEX_DISCOVER_PORT = 32412
DEBUG_FILE = "/home/dietpi/plex/Plex_WakeOnLan/debug.log"

#log = logging.getLogger('app')
#log.addHandler(JournalHandler())
#log.setLevel(logging.INFO)
#log.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
#logging.basicConfig(filename=DEBUG_FILE)

def log(message):
	print(message)

def sendWOLPacket():
    mac = get_mac_address(ip=WOL_IP)

    send_magic_packet(mac,ip_address=WOL_IP,port=WOL_PORT)
    logger.info('WOL Packet sent -> MAC:' + mac + ' | IP:' + WOL_IP + ' | Port:' + str(WOL_PORT))

def switchOnMyStrom():
    url='http://' + MYSTROM_SWITCH_IP + '/relay?state=1'
    headers = {}
    resp = requests.get(url,headers=headers)
    #curl --location -g --request GET url
    logger.info('Mystrom switch on request was sent to ' + MYSTROM_SWITCH_IP )


#async def switchOnMyStromAsync():
#    async with MyStromSwitch(MYSTROM_SWITCH_IP) as switch:
#
#        # Collect the data of the current state
#        await switch.get_state()
#
#        print("Power consumption:", switch.consumption)
#        print("Relay state:", switch.relay)
#        print("Temperature:", switch.temperature)
#        print("Firmware:", switch.firmware)
#        print("MAC address:", switch.mac)
#
#        print("Turn on the switch")
#        if not switch.relay:
#            await switch.turn_on()
#
#        # print("Toggle the switch")
#        # await switch.toggle()
#
#        # Switch relay off if it was off
#        if switch.relay:
#            await switch.turn_off()
#

def signal_handler(sig, frame):
    global server_socket
    server_socket.close()
    logger.warning('Force exit!')
    sys.exit(0)
	
#Sockets and interrupt handler
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
signal.signal(signal.SIGINT, signal_handler)


try:
    server_socket.bind(('', PLEX_DISCOVER_PORT))
except socket.error as e:
    logger.error('Error binding socket!')
    exit(1)

while True:
    message, (ip,port) = server_socket.recvfrom(1024)
    if (ip != WOL_IP and ip != RPI4_IP) :
        logger.info('Plex client open on: ' + str(ip))
        #log("Content: " + str(message))
        #if(message has content) in case false positive connections 
        #asyncio.run(switchOnMyStrom)
        switchOnMyStrom()
        sendWOLPacket()
        #print('\n')
        sleep(10)

socket.close()

