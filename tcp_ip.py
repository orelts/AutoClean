# /usr/bin/python
import socket
import sys
import time
import select
import enum
import xml.etree.ElementTree as ET

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
            message = self.composeMsg()

        print('sending "{}"'.format(message))
        self.sock.sendall(message.encode())
        time.sleep(1)

    ##  composing the msg for transmission
    # @params sensors information
    # @returns msg
    def composeMsg(self, msg = ""):
        return msg


    ##  receive msg from the server
    # @params -
    # @returns received msg
    def get_cmds(self):
        ready = select.select([self.sock], [], [], 1)
        if ready[0]:
            data = self.sock.recv(4096)
            return data
        else:
            return None

    def handle_data(self, data):
       try:
            if data:
                root = ET.fromstring(data)
                inst = root.find('cmd').get('type')
                if inst == "instruction":
                    for elem in root.findall('cmd'):
                        direction = elem.find('dir').text
                        coordinates = elem.find('coordinates').text
                        print(direction, coordinates)
                elif inst == "info":
                    for elem in root.findall('cmd'):
                        info = elem.find('info').text
                        print(info)
                for child in root:
                    print(child.tag, child.attrib)

                self.transmit("handled data")
            else:
                pass
       except Exception as e:
        self.transmit(str(e))



    ##  closing the tcp-ip socket of the client-server
    def close(self):
        print(sys.stderr, 'closing socket')
        self.sock.close()



class Op(enum.Enum):
    drive = 1
    info = 2


class Data:
    def __init__(self, op):
        self.operation = op


class Instructions(Data):
    def __init__(self, op, dir, coordinates):
        Data.__init__(self,op)
        self.coordinates = coordinates
        self.dir = dir

    def create_xml(self):
        content = """ <data>
                        <cmd type="instruction"> 
                           <dir>""" + str(self.dir) + """ </dir>
                           <coordinates>""" + str(self.coordinates) + """ </coordinates>
                        </cmd>
                    </data>"""
        return content


class Info(Data):
    def __init__(self, op, info):
        Data.__init__(self, op)
        self.info = info

    def create_xml(self):
        content = """ <data> 
                         <cmd type="info"> 
                           <info>""" + str(self.info) + """ </info>
                        </cmd>
                    </data>"""

        return content