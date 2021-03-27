

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

# configure the serial connections (the parameters that we see here are stated in the sabertooth's specs)
# ttyS0 is UART0 in auvidea j121 board
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.open()

## according to sabertooth specs, page 18
def drive(speed,command,address,duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        msg = [address, command, speed, ((address + command + speed) & 0b01111111)]
        msg = bytes(bytearray(msg))
        ser.write(msg)
        ser.flush()
def drive_forward(speed,address=128,duration=3):
    drive(speed,8,address,duration)

def drive_backwards(speed,address=128,duration=3):
    drive(speed,9,address,duration)

def turn_right(speed,address=128,duration=5):
    drive(speed,10,address,duration)

def turn_left(speed,address=128,duration=3):
    drive(speed,11,address,duration)

#sample driving commands
if __name__ == '__main__':
    drive_forward(50,duration=7)
    turn_right(50)
    drive_backwards(50)
    turn_left(50)

    ser.stop()
    ser.close()