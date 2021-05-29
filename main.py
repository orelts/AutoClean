from time import sleep
from sql.sql_config import *
import os


if __name__ == '__main__':

    # os.system("python2.7 ./sql/sql_initiate.py > initiate_log.txt")
    # os.system("python2.7 ./sensors/sensors.py --is-vehicle --in-door & > sensors_log.txt")
    # os.system("python2.7 ./driver/driver.py &")
    # subprocess.Popen("python3 ./crane/lynxmotion.py", shell=True)
    conn, cursor = connect_to_db()

    while True:
        angle_ = input("angle")
        speed_ = input("speed")
        distance_ = input("distance")

        print_sql_row(cursor, "driver")
        update_sql(cursor, conn, "driver", (speed_, "0", angle_, distance_), False, d_driver)
        sleep(1)
