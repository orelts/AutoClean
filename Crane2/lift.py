
import serial
from sql.sql_config import *
import time

class Crane:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
    )


if __name__ == '__main__':
    ## connect to SQL
    conn, cursor = connect_to_db()
    init_database(cursor, conn)
    init_sql_table(cursor, conn, "lift", d_lift, False)

    print_sql_row(cursor, "lift")

    cr = Crane()

    while True:
        try:
            ## get the next row that hasnt been executed yet
            curr_ID, new_command = get_row_by_condition(cursor, "is_commited=0", "lift")
            print(new_command)
            if new_command is None:
                continue

            ## extract angle,speed and driving distance from the row
            try:
                ## execute command
                cr.pick()
                print("finished command?")
            except Exception as crane_error:
                print(crane_error)
            ## update the row to executed status
            set_element_in_row(cursor, "is_commited", curr_ID, "lift", "1")
        except Exception as err:
            print(err)





