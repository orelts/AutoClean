import time
import serial

# configure the serial connections (the parameters that we see here are stated in the sabertooth's specs)
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

## according to sabertooth specs, page 18
def drive_forward(address,speed):
    ser.write(address)
    ser.write(8)
    ser.write(speed)
    ser.write((address + 8 + speed) & 0b01111111)

def drive_backwards(address,speed):
    ser.write(address)
    ser.write(9)
    ser.write(speed)
    ser.write((address + 9 + speed) & 0b01111111)

def turn_right(address,speed):
    ser.write(address)
    ser.write(10)
    ser.write(speed)
    ser.write((address + 10 + speed) & 0b01111111)

def turn_left(address,speed):
    ser.write(address)
    ser.write(11)
    ser.write(speed)
    ser.write((address + 11 + speed) & 0b01111111)

#sample driving commands
if __name__ == '__main__':
    drive_forward(128,50)
    time.sleep(2)
    drive_forward(128, 0)
    time.sleep(0.5)

    drive_backwards(128,100)
    time.sleep(2)
    drive_backwards(0, 100)
    time.sleep(0.5)

    turn_left(128,10)
    time.sleep(2)
    turn_left(128,0)
    time.sleep(0.5)

    turn_right(128,20)
    time.sleep(2)
    turn_right(128,0)
    time.sleep(0.5)
