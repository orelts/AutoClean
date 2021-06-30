#!/usr/bin/env python
import socket


def command_input():
    inp = input("Enter cmd input please\n")
    if inp[:4] == "info":
        return inp
    else:
        return None

## local IP of grounds station. if empty '' will listen to all incoming connections
TCP_IP = '192.168.1.22'
## port that was pre opened in grounds station's internet router
TCP_PORT = 10000 #6800

MAX_TRIES = 5

## create socket object which allows the connection and input the precise IP and PORT to listen to
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
## listen to up to 1 connection at a time. if exceeds, ignore the message that is incoming
s.listen(1)

## receive a message
conn, addr = s.accept()
print('Connection address:', addr)

while True:

    ## only when message is 'info' send it to the robot
    msg = command_input()
    if msg is None:
        continue

    # flushing the recv buffer before sending command and receiving usefull feedback
    conn.recv(4096)

    data_ok = False
    attempt = 0
    while attempt < MAX_TRIES:
        print("Sending msg try {} ".format(attempt))
        conn.send(msg.encode()) # send the message
        data = conn.recv(4096) # receive data from robot
        data_ok = True
        break
    if data_ok:
        print("received data: ", data)
    else:
        print(" didnt received msg\n")

conn.close()
