"""!
@brief sabertooth: class implementation for initialization and activation of the motors.
"""

import time
import serial

class sabertooth:
    def __init__(self):
        ## serial connection initialization according to the sabertooth guide
        # ttyS0 is UART0 in auvidea j121 board
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        ## mixed mode works only when valid data is first sent to turn and drive commands
        self.drive_forward(0,work_once=True)
        self.turn_right(0,work_once=True)

    ## supporting method
    # driving methods must be sent consecutively using loops
    # work_once is used to initialize the motors when creating a sabertooth instance
    def drive(self,speed,command,address,duration,work_once):
        end_time = time.time() + duration
        while time.time() < end_time:
            msg = [address, command, speed, ((address + command + speed) & 0b01111111)]
            msg = bytes(bytearray(msg))
            self.ser.write(msg)
            self.ser.flush()
            if(work_once):
                break

    def drive_forward(self,speed,address=128,duration=0.5,work_once=False):
        self.drive(speed,8,address,duration,work_once)

    def drive_backwards(self,speed,address=128,duration=0.5,work_once=False):
        self.drive(speed,9,address,duration,work_once)

    def turn_right(self,speed,address=128,duration=0.5,work_once=False):
        self.drive(speed,10,address,duration,work_once)

    def turn_left(self,speed,address=128,duration=0.5,work_once=False):
        self.drive(speed,11,address,duration,work_once)

    def stop(self,address=128):
        self.drive(0, 8, address, 1,True)

if __name__ == '__main__':

    saber = sabertooth()

    saber.drive_forward(50,address=128,duration=5)
    saber.turn_left(50,address=128,duration=3)
    saber.stop()


