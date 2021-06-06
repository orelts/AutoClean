#!/usr/bin/env python
import socket
from tcp_ip import Op
from tcp_ip import Instructions
from tcp_ip import Info


def command_input():
    inp = input("Enter cmd input please\n")
    xml_msg = None

    if inp == "dir":
        xml_data = Instructions(Op.drive, "left", "10.4.2.1")
        xml_msg = xml_data.create_xml()
    elif inp == "inf":
        xml_data = Info(Op.info, "location")
        xml_msg = xml_data.create_xml()
    return xml_msg


TCP_IP = '192.114.105.254'
TCP_PORT = 5005
MAX_TRIES = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)

while True:

    xml_msg = command_input()
    if xml_msg is None:
        continue

    # flushing the recv buffer before sending command and receiving usefull feedback
    conn.recv(4096)

    data_ok = False
    attempt = 0
    while attempt < MAX_TRIES:
        print("Sending msg try {} ".format(attempt))
        conn.send(xml_msg.encode())
        data = conn.recv(4096)
        data_ok = True
        break
    if data_ok:
        print("received data: ", data)
    else:
        print(" didnt received msg\n")

conn.close()
