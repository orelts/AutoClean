# /usr/bin/python
import socket
import sys
import time

"""
Periodic transmission from TX2 to ground-station (match with 'GroundDB 01.09.2020.xlsx').
Each msg starts with "^" and ends with "|". 
"""

class Transmission:
    # for example: trans = Transmission('192.168.16.101', 10001, '10')
    def __init__(self, ip, port, droneId):
        self.ip = ip
        self.port = port
        self.droneId = droneId
        self.header = '^'
        self.footer = '|'
        self.create()

    def create(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a TCP/IP socket
        print(sys.stderr, 'connecting to {} port {}' .format(self.ip, self.port))
        self.sock.connect((self.ip, self.port))  # connect the socket to the port where the server is listening

        # pre-message
        message = self.header + 'N' + ','.join([self.droneId, '-1', '-1', '-1']) + self.footer
        print(sys.stderr, 'sending pre-message "{}" & wait 1 second' .format(message))
        self.sock.sendall(message.encode('utf-8'))
        time.sleep(1)


    def transmit(self, *data):  # if data = None, will send a default message
        # Send data
        if data is not None:
            message = self.composeMsg(*data)
        else:  # default msg
            print('default message')
            message = self.composeMsg()

        print(sys.stderr, 'sending "{}"'.format(message))
        self.sock.sendall(message.encode('utf-8'))


    def composeMsg(self, MsgID=0, DroneID='DroneID', TimeStampTransmission=0.0, DroneGPSLatitude=0.0, DroneGPSLongitude=0.0, DroneGPSAltitude=0.0,
                   DroneCompass=0.0, PixhawkHeight=0.0, TimeStampPictureTaken=0.0, PicGPSLatitude=0.0, PicGPSLongitude=0.0, PicGPSAltitude=0.0, PicCompass=0.0,
                   CameraYaw=0.0, CameraPitch=0.0, CameraRoll=0.0, TargetPixelX=0, TargetPixelY=0, TargetCertainty=0.0):

        drone_data = ','.join([str(MsgID), DroneID, str(TimeStampTransmission)])

        pixhawk_data = ','.join([str(DroneGPSLatitude), str(DroneGPSLongitude), str(DroneGPSAltitude), str(DroneCompass), str(PixhawkHeight)])

        camera_data = ','.join([str(TimeStampPictureTaken), str(PicGPSLatitude), str(PicGPSLongitude), str(PicGPSAltitude), str(PicCompass), str(CameraYaw),
                                str(CameraPitch), str(CameraRoll)])

        targets_data = ','.join([str(TargetPixelX), str(TargetPixelY), str(TargetCertainty)])

        message = ','.join([drone_data, pixhawk_data, camera_data, targets_data])
        #example: 'T106RecordID,DroneID,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,[3, 14],[3, 14],3,|'

        return self.header + 'T' + message + self.footer


    def close(self):
        print(sys.stderr, 'closing socket')
        self.sock.close()