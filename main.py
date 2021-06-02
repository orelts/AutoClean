from pynput.keyboard import Key, Listener
from time import sleep
from sql.sql_config import *
import threading
import subprocess
from driver.sabertooth import *

try:
    if __name__ == '__main__':
        running = False
        conn, cursor = connect_to_db()
        subprocess.run("python3 ./sql/sql_initiate.py", shell=True)
        subprocess.Popen("python3 ./sensors/sensors.py --is-vehicle --in-door".split(), shell=False)

        def main_loop():
            global running
            global p
            p = subprocess.Popen("python3 ./driver/driver.py".split(), shell=False)
            while running:
                # print("in runing")
                # angle_ = input("angle")
                # speed_ = input("speed")
                # distance_ = input("distance")
                # update_sql(cursor, conn, "driver", (angle_, speed_, distance_, "0"), False, d_driver)
                # print_sql_row(cursor, "driver")
                sleep(1)

        def on_press(key):
            global running
            global p
            if key.char == "q":
                running = False
                p.terminate()
                saber = Sabertooth()
                saber.stop()
                print("stop")

            elif key.char == "s":
                running = True
                print("start")
                t = threading.Thread(target=main_loop)
                # start thread
                t.start()


        # Collect events until released
        with Listener(
                on_press=on_press) as listener:
            listener.join()

except Exception as e:
    p.terminate()
    saber = Sabertooth()
    saber.stop()
