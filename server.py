import json
import mimetypes
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from uuid import uuid4
import logging
import socket
import sys
import _thread
from players_connection_list import PlayerList


def addr_to_msg(addr):
    return '{}:{}'.format(addr[0], str(addr[1])).encode('utf-8')

def simple_udp_server():
    addresses = []
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind(("localhost", 8000))
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("connection from: %s", addr)
        addresses.append(addr)
        if len(addresses) >= 2:
            print("server - send client info to: %s", addresses[0])
            sock.sendto(addr_to_msg(addresses[1]), addresses[0])
            print("server - send client info to: %s", addresses[1])
            sock.sendto(addr_to_msg(addresses[0]), addresses[1])
            addresses.pop(1)
            addresses.pop(0)

if __name__ == '__main__':
    _thread.start_new_thread(simple_udp_server)
    while True:
        pass
