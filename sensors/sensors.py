"""!
@brief sensors: reading data out of sensors of the vehicle to sql server using telemetry class
"""
import telemetry
import time
import argparse
from sql.sql_config import *


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


if __name__ == '__main__':

    conn, cursor = connect_to_db()
    vehicleConnected = True; flightMode = False; inDoor = True

    # initiate contact with flight computer #
    TX_Pixhawk_telem = telemetry.Telemetry(vehicleConnected)  # can't open SITL simulation on TX2 ARM (only on computer)
    TX_Pixhawk_telem.initialize(inDoor)

    # while (not TX_Pixhawk_telem.is_arm()) and flightMode:
    #     print("In flight mode. Waiting the drone to be armed to continue")
    #     time.sleep(1)

    while True:
        try:
            sensors_info = TX_Pixhawk_telem.read_information()
            sensors_info = tuple(vars(sensors_info).values())
            update_sql(cursor, conn, "SensorsInfo", sensors_info, True, d_sensors)
            time.sleep(0.01)
        except Exception as e:
            print("something's wrong with transmission. Exception is {}".format(e))

    # for now - we don't reach here
    TX_Pixhawk_telem.close()
    print("Main closed. Bye")

