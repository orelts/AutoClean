"""!
@brief lynxmotion: class implementation for initialization and activation of the servo-motors.
"""

import serial
import time
class lynxmotion:
    def __init__(self):
        ## serial connection initialization
        # cage_state and arm_state hold the current states of the crane
        # preferebly there are 2 states in which the cage can be - open or closed, but there can be much more freedom
        # in sellection of the apperature of the cage. same for the position of the arm - up or down

        self.ser = serial.Serial(
            port='COM4', ## or ttyUSB0 or ttyS0
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )


    ## supporting method
    # message format is according to lynxmotion guide
    def use_servo(self, servo_num, location, speed):
        msg = "#" + str(servo_num) + "P" + str(location)+"S" + str(speed)+ "\r"
        msg = bytes(bytearray(msg.encode()))
        self.ser.write(msg)
        self.ser.flush()

    def close_cage(self):
            cr.use_servo(8, 800, 900)  # marked with L.  800=cage closed
            cr.use_servo(11, 2050, 900)  # marked with R.  2050=cage closed

    def open_cage(self):
            self.use_servo(8, 2300, 900)  # marked with L.  1500=cage open
            self.use_servo(11, 600, 900)  # marked with R.  1400=cage open


    def arm_down(self):
            self.use_servo(4, 500, 900)  # marked with L.  500=away from black plate
            self.use_servo(7, 2500, 900)  # marked with R.  500=towards the black plate

    def arm_up(self):
            self.use_servo(4, 1800, 900)  # marked with L.  500=away from black plate
            self.use_servo(7, 1200, 900)  # marked with R.  500=towards the black plate

    def wrist_down(self):
            cr.use_servo(12, 800, 900)  # marked with L.  950=on ground
            cr.use_servo(15, 2200, 900)  # marked with R.  2050=on ground

    def wrist_up(self):
            self.use_servo(12, 1100, 900)
            self.use_servo(15, 1900, 900)


if __name__ == '__main__':
    cr = lynxmotion()
    time.sleep(3)
    cr.close_cage()
    time.sleep(2)
    cr.arm_up()
    cr.wrist_up()
    time.sleep(1.5)
    cr.open_cage()
    # cr.use_servo(8, 800, 900)  #marked with L.  800=cage closed
    # cr.use_servo(11, 2050,900)  #marked with R.  2050=cage closed



    # time.sleep(1)
    # cr.open_cage()



