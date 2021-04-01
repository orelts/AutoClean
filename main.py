from time import sleep
from sql.sql_config import *
import subprocess

if __name__ == '__main__':

    subprocess.run("python3 ./sql/sql_initiate.py", shell=True)
    # subprocess.Popen("python3 ./sensors/sensors.py --is-vehicle --in-door", shell=True, close_fds=True)
    # subprocess.Popen("python3 sabertooth.py", shell=True)
    # subprocess.Popen("python3 ./driver/manual_driver.py", shell=True)
    # subprocess.Popen("python3 ./crane/lift.py", shell=True)
    conn, cursor = connect_to_db()

    while True:
        motor_angel = input("choose motoer and angel\n")
        speed = 150
        update_sql(cursor, conn, "lift", ("#"+ str(motor_angel) + "S" + str(speed),), False, d_lift)
