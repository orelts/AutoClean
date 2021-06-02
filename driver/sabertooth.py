"""!
@brief sabertooth: class implementation for initialization and activation of the motors.
"""

import time
import serial

class Sabertooth:
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
        self.stop()

    def send_driving_command(self,speed, command, address=128):
        msg = [address, command, speed, ((address + command + speed) & 0b01111111)]
        msg = bytes(bytearray(msg))
        self.ser.write(msg)
        self.ser.flush()

    ## supporting method
    # driving methods must be sent consecutively using loops
    # work_once is used to initialize the motors when creating a sabertooth instance
    def drive(self,speed,command,address,duration, work_once):
        start_time = time.time()
        end_time = start_time + duration
        while time.time() < end_time:
            self.send_driving_command(speed, command, address)
            if work_once:
                break

    def drive_forward(self,speed, duration=1, work_once=False, address=128):
        self.drive(speed,8,address,duration,work_once)

    def drive_backwards(self,speed, duration=1, work_once=False, address=128):
        self.drive(speed,9,address,duration,work_once)

    def turn_right(self,speed, duration=1, work_once=False, address=128):
        self.drive(speed,10,address,duration,work_once)

    def turn_left(self,speed, duration=1, work_once=False, address=128):
        self.drive(speed,11,address,duration,work_once)

    def stop(self,address=128):
        print("Stop")
        for i in range(8,12):
            msg = [address, i, 0, ((address + i) & 0b01111111)]
            msg = bytes(bytearray(msg))
            self.ser.write(msg)
            self.ser.flush()





if __name__ == '__main__':

    saber = Sabertooth()



