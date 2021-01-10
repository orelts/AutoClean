# /usr/bin/python
import socket
import sys
import time

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
        print(sys.stderr, 'connecting to {} port {}' .format(self.ip, self.port))
        self.sock.connect((self.ip, self.port))  # connect the socket to the port where the server is listening

        # pre-message
        message = self.header + 'N' + ','.join([ '-1', '-1', '-1']) + self.footer
        print(sys.stderr, 'sending pre-message "{}" & wait 1 second' .format(message))
        self.sock.sendall(message.encode('utf-8'))
        time.sleep(1)

    ##  transmit data to the server
    # sends msg in the format of "^<msg>|" where ^ is the header and | is the footer.
    # the msg is created by the composeMsg method.
    def transmit(self, *data):  # if data = None, will send a default message
        # Send data
        if data is not None:
            message = self.composeMsg(*data)
        else:  # default msg
            print('default message')
            message = self.composeMsg()

        print(sys.stderr, 'sending "{}"'.format(message))
        self.sock.sendall(message.encode('utf-8'))

    ##  composing the msg for transmission
    # @params sensors information
    # @returns msg
    def composeMsg(self, MsgID=0, TimeStampTransmission=0.0, DroneGPSLatitude=0.0, DroneGPSLongitude=0.0, DroneGPSAltitude=0.0,
                   DroneCompass=0.0, PixhawkHeight=0.0, TimeStampPictureTaken=0.0, PicGPSLatitude=0.0, PicGPSLongitude=0.0, PicGPSAltitude=0.0, PicCompass=0.0,
                   CameraYaw=0.0, CameraPitch=0.0, CameraRoll=0.0, TargetPixelX=0, TargetPixelY=0, TargetCertainty=0.0):

        vehicle_data = ','.join([str(MsgID), str(TimeStampTransmission)])

        pixhawk_data = ','.join([str(DroneGPSLatitude), str(DroneGPSLongitude), str(DroneGPSAltitude), str(DroneCompass), str(PixhawkHeight)])

        camera_data = ','.join([str(TimeStampPictureTaken), str(PicGPSLatitude), str(PicGPSLongitude), str(PicGPSAltitude), str(PicCompass), str(CameraYaw),
                                str(CameraPitch), str(CameraRoll)])

        targets_data = ','.join([str(TargetPixelX), str(TargetPixelY), str(TargetCertainty)])

        message = ','.join([vehicle_data, pixhawk_data, camera_data, targets_data])
        #example: 'T106RecordID,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,[3, 14],[3, 14],3,|'

        return self.header + 'T' + message + self.footer

    ##  receive msg from the server
    # @params -
    # @returns received msg
    def receive(self):
        print(sys.stderr, 'sending "{}"'.format(message))
        msg = self.sock.recv(msg_length)
        while msg:
            print('Received:' + msg.decode())
            msg =  self.sock.recv(1024)
        return msg

    ##  closing the tcp-ip socket of the client-server
    def close(self):
        print(sys.stderr, 'closing socket')
        self.sock.close()