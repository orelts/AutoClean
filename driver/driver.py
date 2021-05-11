import keyboard
from sabertooth import *
from sql.sql_config import *

conn, cursor = connect_to_db()


class Driver(Sabertooth):
    def __init__(self):
        Sabertooth.__init__(self)

    def handle_command(self, angle, distance=5, rotation_speed=100, driving_speed = 100 ):
        try:
            self.rotate_in_angle(angle, rotation_speed)
            self.drive_distance(distance, driving_speed)
        except Exception as e:
            Sabertooth.stop()
            raise e

    def rotate_in_angle(self, angle, speed=100):
        try:
            initial_heading = get_last_table_elem(cursor, "heading", "SensorsInfo")
            while abs(initial_heading - get_last_table_elem(cursor, "heading", "SensorsInfo")) < angle:
                if angle < 0:  # rotate left
                    Sabertooth.turn_left(speed)
                else:
                    Sabertooth.turn_right(speed)
        except Exception as e:
            Sabertooth.stop()
            raise e
        Sabertooth.stop()

    def drive_distance(self, distance, speed=100):
        duration = distance/ speed
        start = time.time()
        try:
            while time.time() - start < duration:
                if distance < 0:  # drive backward
                    Sabertooth.drive_backwards(speed)
                else:
                    Sabertooth.drive_forward(speed)
        except Exception as e:
            Sabertooth.stop()
            raise e
        Sabertooth.stop()


if __name__ == '__main__':

    while True:
        try:
            driver = Driver()
            curr_ID ,new_command = get_row_by_condition(cursor, "is_commited=0", "driver")
            if new_command is None:
                continue

            angle_ = get_column_idx(cursor, "driver", "angle")
            angle = new_command[0][angle_]
            speed_ = get_column_idx(cursor, "driver", "speed")
            speed = new_command[0][speed_]
            distance_ = get_column_idx(cursor, "driver", "distance")
            distance = new_command[0][distance_]

            try:
                driver.handle_command(angle, distance, 100, speed)
            except Exception as drv_cmd_err:
                print("driving command with ID={} failed".format(curr_ID))
                raise drv_cmd_err
            set_element_in_row(cursor, "is_commited", curr_ID, "driver", "1")
        except Exception as e:
            print("Driver Exception:", e)
            saber.stop()
            while True:
                if keyboard.is_pressed('c'):
                    break
            continue

        if keyboard.is_pressed('q'):
            # saber.stop()
            print("Saber stop")
            while True:
                if keyboard.is_pressed('c'):
                    break


