#!/usr/bin/env python

#pip install getmac
#pip install wakeonlan
from getmac import get_mac_address
from wakeonlan import send_magic_packet
from time import sleep
import socket, sys, signal

WOL_IP = "192.168.1.69"
WOL_PORT = 9
PLEX_DISCOVER_PORT = 32412
DEBUG_FILE = "/usr/bin/plex_wol/debug.log"



def log(message):
	print(message)

def sendWOLPacket():
    mac = get_mac_address(ip=WOL_IP)
    send_magic_packet(mac,ip_address=IP,port=WOL_PORT)
    log('\nWOL Packet sent -> MAC:' + mac + ' | IP:' + WOL_IP + '| Port:' + str(WOL_PORT))


def signal_handler(sig, frame):
    global server_socket
    server_socket.close()
    log('Force exit!')
    sys.exit(0)
	
#Sockets and interrupt handler
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
signal.signal(signal.SIGINT, signal_handler)

#error mesages
log_file = open(DEBUG_FILE,"w")
sys.stdout = log_file

try:
    server_socket.bind(('', PLEX_DISCOVER_PORT))
except socket.error as e:
    log("Error binding socket!")
    exit(1)

while True:
    message, (ip,port) = server_socket.recvfrom(1024)
    if ip != WOL_IP:
        log("Plex client open on: " + str(ip))
        #log("Content: " + str(message))
        #if(message has content) in case false positive connections 
        sendWOLPacket()
        #print('\n')
        sleep(5)

socket.close()

