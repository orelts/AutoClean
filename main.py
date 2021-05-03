from time import sleep
from sql.sql_config import *
import os


if __name__ == '__main__':

    os.system("python2.7 ./sql/sql_initiate.py > initiate_log.txt")
    os.system("python2.7 ./sensors/sensors.py --is-vehicle --in-door & > sensors_log.txt")
    # subprocess.Popen("python3 sabertooth.py", shell=True)
    # subprocess.Popen("python3 ./driver/manual_driver.py", shell=True)
    # subprocess.Popen("python3 ./crane/lynxmotion.py", shell=True)
    conn, cursor = connect_to_db()
    while True:
        print_sql_row(cursor)
        sleep(1)
