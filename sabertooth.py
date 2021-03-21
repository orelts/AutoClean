import time
import serial
from pysabertooth import Sabertooth

# configure the serial connections (the parameters that we see here are stated in the sabertooth's specs)
saber = Sabertooth('/dev/ttyS0', baudrate=9600, address=128, timeout=0.1)

#sample driving
if __name__ == '__main__':
    # drive(number, speed)
    # number: 1-2
    # speed: -100 - 100
    while True:
        saber.drive(1, 30)
        time.sleep(2)
        saber.drive(2, 30)
        time.sleep(2)
