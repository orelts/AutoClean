

# # configure the serial connections (the parameters that we see here are stated in the sabertooth's specs)
# saber = Sabertooth('/dev/ttyS0', baudrate=9600, address=128, timeout=0.1)
#
# #sample driving
# if __name__ == '__main__':
#     # drive(number, speed)
#     # number: 1-2
#     # speed: -100 - 100
#     while True:
#         saber.drive(1, 30)
#         time.sleep(2)
#         saber.drive(2, 30)
#         time.sleep(2)

import time
import serial

class sabertooth:

# configure the serial connections (the parameters that we see here are stated in the sabertooth's specs)
# ttyS0 is UART0 in auvidea j121 board
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        self.ser.open()

    ## according to sabertooth specs, page 18
    def drive(self,speed,command,address,duration):
        end_time = time.time() + duration
        while time.time() < end_time:
            msg = [address, command, speed, ((address + command + speed) & 0b01111111)]
            msg = bytes(bytearray(msg))
            self.ser.write(msg)
            self.ser.flush()
    def drive_forward(self,speed,address=128,duration=1):
        self.drive(speed,8,address,duration)

    def drive_backwards(self,speed,address=128,duration=1):
        self.drive(speed,9,address,duration)

    def turn_right(self,speed,address=128,duration=1):
        self.drive(speed,10,address,duration)

    def turn_left(self,speed,address=128,duration=1):
        self.drive(speed,11,address,duration)

#sample driving commands
# if __name__ == '__main__':
#     drive_forward(50,duration=7)
#     turn_right(50)
#     drive_backwards(50)
#     turn_left(50)
#
#     ser.stop()
#     ser.close()