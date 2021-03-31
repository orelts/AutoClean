
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


    while True:
        x = input("Enter ")
        if x == "o1":
            print("Open")
            cr.move_arm(1, 1500, 600)
        elif x == "c1":
            print("Close")
            cr.move_arm(1, 500, 600)
        elif x == "o3":
            print("Open")
            cr.move_arm(3, 1500, 600)

        elif x == "c3":
            print("Open")
            cr.move_arm(3, 800, 600)


