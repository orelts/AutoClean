from time import sleep
from sql_config import *
import subprocess

if __name__ == '__main__':

    subprocess.run("python3 sql_initiate.py", shell=True)
    subprocess.Popen("python3 sensors.py --is-vehicle --in-door", shell=True, close_fds=True)
    subprocess.Popen("python3 sabertooth.py", shell=True)

    conn, cursor = connect_to_db()
    while True:
        print_sql_row(cursor, "SensorsInfo")
        sleep(2)

