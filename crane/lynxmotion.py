
import serial

class lynxmotion:
    def __init__(self):
        self.cage_state = 'OPEN'
        self.arm_state = 'UP'
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        self.close_cage()
        self.arm_down()

    def use_servo(self, servo_num, location, speed):
        msg = "#" + str(servo_num) + "P" + str(location)+"S" + str(speed)+ "\r"
        msg = bytes(bytearray(msg.encode()))
        self.ser.write(msg)
        self.ser.flush()

    def close_cage(self):
        if self.cage_closed == 'CLOSED':
            return
        else:
            self.use_servo(1,500,600)
            self.cage_closed = 'CLOSED'

    def open_cage(self):
        if  self.cage_closed == 'OPEN':
            return
        else:
            self.use_servo(1,1500,600)
            self.cage_closed = 'OPEN'

    def arm_down(self):
        if self.arm_state == 'DOWN':
            return
        else:
            self.use_servo(3,500,600)
            self.arm_state = 'DOWN'

    def arm_up(self):
        if self.arm_state == 'UP':
            return
        else:
            self.use_servo(3,1500,600)
            self.arm_state = 'UP'



if __name__ == '__main__':


    cr = lynxmotion()


    while True:
        x = input("Enter ")
        if x == "o1":
            print("Open")
            cr.use_servo(1, 1500, 600)
        elif x == "c1":
            print("Close")
            cr.use_servo(1, 500, 600)
        elif x == "o3":
            print("Open")
            cr.use_servo(3, 1500, 600)

        elif x == "c3":
            print("Open")
            cr.use_servo(3, 800, 600)


