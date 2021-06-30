"""!
@brief sensors: reading data out of sensors of the vehicle to sql server using telemetry class
"""

import telemetry
import time
import argparse
import os
from multiprocessing import Process

from sql.sql_config import *

module_path = os.path.abspath(os.getcwd())



"""
Parsing given arguments
"""
## action chooses true or false hardcoded for the arguments of this module
parser = argparse.ArgumentParser(description="Drone detection project")
parser.add_argument("--is-vehicle", action='store_true',
                    help="If a drone is connected to the TX2")
parser.add_argument("--is_flight", action='store_true',
                    help="If we intend arm the drone (necessary for flight)")
parser.add_argument("--in-door", action='store_true',
                    help="If we are indoor (no GPS connection)")
args = parser.parse_args()

HISTORY_WRITE = 10

##  this function runs as a parallel process in sensors module.
#   Exports the sensors sql table to xlsx format using sql_to_excel function in sql_config (possible to change to csv)
def export_sensors_to_excel():
    conn, cursor = connect_to_db()
    while True:
        sql_to_excel(conn, "SensorsInfo", "sql/SensorsInfo.xlsx")
        time.sleep(1)


if __name__ == '__main__':

    conn, cursor = connect_to_db() # connection to sql server
    init_database(cursor, conn) # connection to AutoCleanDB
    init_sql_table(cursor, conn, "SensorsInfo", d_sensors, False) # create sensors info table if it doesn't exist
    print_sql_row(cursor, "SensorsInfo") # for sanity prints the table (might limit rows so it will print limited amount of rows)

    vehicleConnected = True; flightMode = False; inDoor = True

    # initiate contact with vehicle computer #
    TX_Pixhawk_telem = telemetry.Telemetry(vehicleConnected)  # can't open SITL simulation on TX2 ARM (only on computer)
    TX_Pixhawk_telem.initialize(inDoor)

    p = Process(target=export_sensors_to_excel) # starting backround process for excel exporting. might change the function for other background routine
    p.start()

    while True:
        try:
            sensors_info = TX_Pixhawk_telem.read_information() # reads sensors info from dronekit API
            sensors_info = tuple(vars(sensors_info).values()) # turns class members to tuple for sql row insert
            update_sql(cursor, conn, "SensorsInfo", sensors_info, False, d_sensors) # inserts to sql sensors table in the fields that parsed from d_sensors
            time.sleep(0.2) # to prevent heavy load on sql server we insert with delay
        except Exception as e:
            print("something's wrong with transmission. Exception is {}".format(e))

    # for now - we don't reach here
    p.join()
    TX_Pixhawk_telem.close()
    print("Main closed. Bye")

