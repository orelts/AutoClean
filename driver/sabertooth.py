import time
from pysabertooth import Sabertooth


# configure the serial connections (the parameters that we see here are stated in the sabertooth's specs)
saber = Sabertooth('/dev/ttyS0', baudrate=9600, address=128, timeout=0.1)


if __name__ == '__main__':
    # sample driving
    # drive(number, speed)
    # number: 1-2
    # speed: -100 - 100


    while True:
        x = input("PLease press to move")
        if x == "x":
            saber.drive(2, 30)
            saber.drive(1, 30)
            time.sleep(2)
        saber.stop()




