import time
import serial
import pysabertooth

# configure the serial connections (the parameters that we see here are stated in the sabertooth's specs)
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.open()

## according to sabertooth specs, page 18
def drive_forward(speed,address=128,duration=3):
    end_time = time.time() + duration
    while time.time() < end_time:
        ser.write(bytes(address))
        ser.write(bytes(8))        #command
        ser.write(bytes(speed))
        ser.write(bytes((address + 8 + speed) & 0b01111111))
        ser.flush()

def drive_backwards(speed,address=128,duration=3):
    end_time = time.time() + duration
    while time.time() < end_time:
        ser.write(bytes(address))
        ser.write(bytes(9))
        ser.write(bytes(speed))
        ser.write(bytes((address + 9 + speed) & 0b01111111))
        ser.flush()

def turn_right(speed,address=128,duration=5):
    end_time = time.time() + duration
    while time.time() < end_time:
        ser.write(bytes(address))
        ser.write(bytes(10))
        ser.write(bytes(speed))
        ser.write(bytes((address + 10 + speed) & 0b01111111))
        ser.flush()

def turn_left(speed,address=128,duration=3):
    end_time = time.time() + duration
    while time.time() < end_time:
        ser.write(bytes(address))
        ser.write(bytes(11))
        ser.write(bytes(speed))
        ser.write(bytes((address + 11 + speed) & 0b01111111))
        ser.flush()

#sample driving commands
if __name__ == '__main__':
    drive_forward(50)
    turn_right(50)
    drive_backwards(50)
    turn_left(50)

    ser.stop()
    ser.close()