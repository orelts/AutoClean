# /usr/bin/python
import socket
import sys
import time
import select

"""!
@brief communication: using tcp-ip protocol for commuincating with ground_station.
we either send msg from tx2 or receive msg from ground station in purpose of different stuff such as direction or speed instructions.
"""
msg_length = 1024

## class for Communication with ground station server using TCP-P socket.
# we can receive msg and transmit msg to the ground station
class Communication:
    ##  Constructor, gets the ip of the server and the port the server listens on.
    # usage for example: trans = Transmission('192.168.16.101', 10001, '10')
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.header = '^'
        self.footer = '|'
        self.create()

    ##  creates the tcp-ip socket.
    # send pre msg. this method is called from the constructor.
    def create(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a TCP/IP socket
        print('connecting to {} port {}' .format(self.ip, self.port))
        self.sock.connect((self.ip, self.port))  # connect the socket to the port where the server is listening

        # pre-message
        message = self.header + 'N' + ','.join([ '-1', '-1', '-1']) + self.footer
        time.sleep(1)

    ##  transmit data to the server
    # sends msg in the format of "^<msg>|" where ^ is the header and | is the footer.
    # the msg is created by the composeMsg method.
    def transmit(self, data):  # if data = None, will send a default message
        # Send data
        if data != "":
            message = self.composeMsg(data)
        else:  # default msg
            print('default message')
            message = self.composeMsg()

        print('sending "{}"'.format(message))
        self.sock.sendall(message.encode())

    ##  composing the msg for transmission
    # @params sensors information
    # @returns msg
    def composeMsg(self, msg):
        return self.header + 'T' + msg + self.footer

    ##  receive msg from the server
    # @params -
    # @returns received msg
    def get_cmds(self):
        got_data = False
        ready = select.select([self.sock], [], [], 1)
        if ready[0]:
            data = self.sock.recv(4096)
            got_data = True
            if data:
                try:
                    self.handle_data(data)
                except Exception as e:
                    print("There was a problem", e, file= sys.stderr)
        if got_data:
            return data
        else:
            return None

    def handle_data(self, data):
        if data == "b'hey'":
            print("Handling data\n")
            self.transmit("hello")
        else:
            print("empty data\n")
            self.transmit("empty data")



    ##  closing the tcp-ip socket of the client-server
    def close(self):
        print(sys.stderr, 'closing socket')
        self.sock.close()