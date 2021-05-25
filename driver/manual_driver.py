
"""!
@brief manual_driver: module which is set for manual control over the robot
entering manual driving mode by pressing 'enter', exiting by pressing 'escape'
arrows control the direction of movement
WASD control the crane
note: there is also a git commit where xbox controller is configured to control the robot
"""


import keyboard
import sabertooth
import time
import os
import sys
from crane.lynxmotion import *

module_path = os.path.abspath(os.getcwd())

if module_path not in sys.path:

    sys.path.append(module_path)

from sql.sql_config import *

if __name__ == '__main__':
    conn, cursor = connect_to_db()
    manual_driving_mode = 'OFF'
    end_time = time.time() + 60


    while(manual_driving_mode == 'OFF' and time.time() < end_time):
        if keyboard.is_pressed('enter'):
                manual_driving_mode = 'ON'
                saber = sabertooth.Sabertooth()
                #lynx = Lynxmotion()

    while (manual_driving_mode == 'ON'):
        x = get_last_table_elem(cursor, "heading_", "SensorsInfo")
        time.sleep(1)
        if keyboard.is_pressed('esc'):
            manual_driving_mode = 'OFF'
            saber.stop()
        elif keyboard.is_pressed('up'):
            print('fwd')
            saber.drive_forward(70)
        elif keyboard.is_pressed('down'):
            print('back')
            saber.drive_backwards(100)
            time.sleep(1)
        elif keyboard.is_pressed('left'):
            x = get_last_table_elem(cursor, "heading_", "SensorsInfo")
            while abs(int(x) - int(get_last_table_elem(cursor, "heading_", "SensorsInfo"))) < 90  and not keyboard.is_pressed('space'):
                print('left')
                saber.turn_right(70)
                time.sleep(0.5)
            saber.stop()
        elif keyboard.is_pressed('right'):
            x = get_last_table_elem(cursor, "heading_", "SensorsInfo")
            while abs(int(x) - int(get_last_table_elem(cursor, "heading_", "SensorsInfo"))) < 90 and not keyboard.is_pressed('space'):
                print('right')
                saber.turn_left(70)
                time.sleep(0.5)
            saber.stop()
        elif keyboard.is_pressed('space'):
            print('stop')
            saber.stop()
            time.sleep(0.5)
        # elif keyboard.is_pressed('s'):
        #     print('cage close')
        #     lynx.close_cage()
        #     time.sleep(0.5)
        # elif keyboard.is_pressed('w'):
        #     print('cage open')
        #     lynx.open_cage()
        #     time.sleep(0.5)
        # elif keyboard.is_pressed('a'):
        #     print('arm up')
        #     lynx.arm_up()
        #     time.sleep(0.5)
        # elif keyboard.is_pressed('d'):
        #     print('arm down')
        #     lynx.arm_down()
        #     time.sleep(0.5)

    exit()


