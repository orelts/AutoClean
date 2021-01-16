#!/usr/bin/env python

import socket
import select

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
MAX_TRIES = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, )
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)

while True:
    msg = input("Enter cmd input please\n")
    data_ok = False
    attempt = 0
    while attempt < MAX_TRIES:
        print("Sending msg try  {} \n ".format(attempt))
        conn.send(msg.encode())
        data = conn.recv(4096)
        data_ok = True
        break
    if data_ok:
        print("received data: ", data)
    else:
        print(" didnt received msg\n")

conn.close()
