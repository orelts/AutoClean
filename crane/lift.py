
import serial

class crane:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
    )

    def move_arm(self, servo_num, location, speed):
        msg = "#" + str(servo_num) + "P" + str(location)+"S" + str(speed)+ "\r"
        msg = bytes(bytearray(msg.encode()))
        self.ser.write(msg)
        self.ser.flush()



if __name__ == '__main__':


    cr= crane()
    cr.move_arm(1,5, 5)
    cr.move_arm(3, 5, 5)