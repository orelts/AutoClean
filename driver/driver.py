from pynput.keyboard import Key, Listener
from sabertooth import *
from sql.sql_config import *
import keyboard

conn, cursor = connect_to_db()


class Driver(Sabertooth):
    def __init__(self):
        super(Driver, self).__init__()

    def handle_command(self, angle, distance=5, rotation_speed=100, driving_speed = 100 ):
        try:
            print("angle in driver is {}, distance is {} and speed is {}".format(angle, distance, driving_speed))
            # print ("Vehcile rotating in {} degrees for distance {} in speed {}".format(angle, distance, driving_speed))

            self.rotate_in_angle(angle, rotation_speed)

            self.drive_distance(distance, driving_speed)
        except Exception as e:
            self.saber.stop()
            raise e

    def rotate_in_angle(self, angle, speed=100):
        try:
            initial_heading = get_last_table_elem(cursor, "heading_", "SensorsInfo")
            x = abs(int(initial_heading) - int(get_last_table_elem(cursor, "heading_", "SensorsInfo")))
            print("x is {}".format(x))
            print("angle is {} ". format(angle))
            while x < int(angle):
                x = abs(int(initial_heading) - int(get_last_table_elem(cursor, "heading_", "SensorsInfo")))
                if angle < 0:  # rotate left
                    print("left with speed {}".format(speed))
                    self.turn_left(speed)
                else:
                    print("right with speed {}".format(speed))
                    self.turn_right(speed)

        except Exception as e:
            self.stop()
            raise e
        self.stop()

    def drive_distance(self, distance, speed=100):
        print("speed in drive distance is {}".format(speed))
        if speed == 0:
            return
        duration = distance/ speed
        start = time.time()
        try:
            self.drive_forward(speed, duration=5)
            # while time.time() - start < 5:
            #     if distance < 0:  # drive backward
            #         self.saber.drive_backwards(speed)
            #     else:
            #         self.saber.drive_forward(speed)
        except Exception as e:
            self.stop()
            raise e
        self.stop()

if __name__ == '__main__':
    driver = Driver()
    while True:
        try:
            curr_ID ,new_command = get_row_by_condition(cursor, "is_commited=0", "driver")
            print(new_command)
            if new_command is None:
                continue

            angle_ = get_column_idx(cursor, "driver", "angle")
            angle = new_command[0][angle_]
            speed_ = get_column_idx(cursor, "driver", "speed")
            speed = new_command[0][speed_]
            distance_ = get_column_idx(cursor, "driver", "distance")
            distance = new_command[0][distance_]
            try:
                driver.handle_command(int(angle), int(distance), 100, int(speed))
                print("finished command?")
            except Exception as drv_cmd_err:
                print("driving command with ID={} failed".format(curr_ID))
                raise drv_cmd_err
            print("finished command?!")
            set_element_in_row(cursor, "is_commited", curr_ID, "driver", "1")
        except Exception as e:
            driver.saber.stop()
        if keyboard.is_pressed('q'):
            driver.stop()

