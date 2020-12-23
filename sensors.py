"""
file: sensors
reading data out of sensors of the vehicle to sql server
"""
import telemetry
import time
import multiprocessing
import argparse
import pyodbc
from statistics import median

TIME_BETWEEN_MSGS = 1.  # TBM. 1 sec is the maximum allowance


## connecting to the SQL Server
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'        #dont change
                      'Server=localhost;'     #server name can be parsed from name in the SQL SERVER MANAGEMENT
                      'Database=AutoCleanDB;'   #name of the database you want to parse from
                      'uid=sa;'
                      'pwd=ItamarOrel2020;')    #dont change
cursor = conn.cursor()

"""
Parsing given arguments
"""
parser = argparse.ArgumentParser(description="Drone detection project")
parser.add_argument("--is-drone", action='store_true',
                    help="If a drone is connected to the TX2")
parser.add_argument("--is_flight", action='store_true',
                    help="If we intend arm the drone (necessary for flight)")
parser.add_argument("--in-door", action='store_true',
                    help="If we are indoor (no GPS connection)")
args = parser.parse_args()



## function to constantly update sql server with sensors data
# Send transmission to ground station if TIME_BETWEEN_MSGS seconds have passed since last transmission
def periodicSend(lastSendTime, msdId):
    print("Starting {} process".format(multiprocessing.current_process().name))
    TX_Pixhawk_telem_per = telemetry.Telemetry(vehicleConnected)  # can't open SITL simulation on TX2 ARM (only on computer)
    TX_Pixhawk_telem_per.initialize(inDoor)
    lat_per_med, lon_per_med, alt_per_med, height_per_med = [], [], [], []  # the median of the last second

    while True:
        assert time.time() - lastSendTime.value >= 0., "periodicSend: error, negative time"
        sensors_info = TX_Pixhawk_telem_per.read_information()
        lat_per = sensors_info.lat_
        lon_per = sensors_info.lon_
        alt_per = sensors_info.alt_
        height_per = sensors_info.relative_alt_

        lat_per_med.append(lat_per), lon_per_med.append(lon_per), alt_per_med.append(alt_per), height_per_med.append(height_per)

        if (time.time() - lastSendTime.value) >= TIME_BETWEEN_MSGS:  # no transmission was sent due to camera trigger, sending periodic message
            with lastSendTime.get_lock():  # can be changed also inside 'main'
                lastSendTime.value = time.time()  # TODO: NEED TO BE BEFORE OR AFTER TRANSMIT?

                sensors_info1 = TX_Pixhawk_telem_per.read_information()
                heading_per = sensors_info1.heading_
                cam_yaw_per = sensors_info1.yaw_
                cam_pit_per = sensors_info1.pitch_
                cam_rol_per = sensors_info1.roll_
                groundspeed_per = sensors_info1.groundspeed_
                home_location_per = sensors_info1.home_location_
                battery_per = sensors_info1.battery_
                last_heartbeat_per = sensors_info1.last_heartbeat_

            with msdId.get_lock():  # can be changed also inside 'main'
                msdId.value = msdId.value + 1
                print("Periodic MSG, ID {}:".format(msdId.value))
                # print("GPS lat (MED): {}, GPS lon (MED): {}, GPS alt (MED): {}, Compass: {}, Height from home (MED): {}, Yaw: {}, Pitch: {}, Roll: {}".format(lat_per_med, lon_per_med,  # for debug
                #                                                                   alt_per_med, heading_per, height_per_med, cam_yaw_per, cam_pit_per, cam_rol_per))
                
                sensors_inf = (str(groundspeed_per), str(home_location_per), str(battery_per), str(last_heartbeat_per),
                                str(groundspeed_per), str(home_location_per), str(battery_per), str(last_heartbeat_per))
                
                cursor.execute('''
                IF NOT EXISTS (SELECT * FROM  dbo.SensorsInfo WHERE ID = 1) 

                    INSERT INTO dbo.SensorsInfo(ID, groundspeed, home_location, battery, last_heartbeat)
                    VALUES(1, ?, ?, ?, ?)

                ELSE

                    UPDATE dbo.SensorsInfo
                    SET groundspeed = ?, home_location = ?, battery = ?, last_heartbeat= ?
                    WHERE ID = 1
                               ''', sensors_inf)
                conn.commit()

            lat_per_med, lon_per_med, alt_per_med, height_per_med = [], [], [], []

        time.sleep(0.1)  # will result the lists to be with a length of 10 numbers (waiting 0.1s and sending each 1s)


## sensors main uses multi processing with periodic_send function for constant updating of sql db
if __name__ == '__main__':
    vehicleConnected = args.is_drone; flightMode = args.is_flight; inDoor = args.in_door

    # initiate contact with flight computer #
    TX_Pixhawk_telem = telemetry.Telemetry(vehicleConnected)  # can't open SITL simulation on TX2 ARM (only on computer)
    TX_Pixhawk_telem.initialize(inDoor)

    while True:
        reset_value = TX_Pixhawk_telem.read_channel8()  # default value for SITL is 1800

        # shared memory (accessible throughout different processes) #
        manager = multiprocessing.Manager()
        shared_yoloOutput = manager.list()
        shared_lastMsgTime = multiprocessing.Value('d', time.time())  # 'Value' is faster than 'Manager'
        shared_msgId = multiprocessing.Value('i', 0)

        # processes #
        periodicProcess = multiprocessing.Process(name="periodic_msg", target=periodicSend, args=[shared_lastMsgTime, shared_msgId])


        while (not TX_Pixhawk_telem.is_arm()) and flightMode:
            print("In flight mode. Waiting the drone to be armed to continue")
            time.sleep(1)

        periodicProcess.start()

        lat_cam_med, lon_cam_med, alt_cam_med, height_cam_med = [], [], [], []
        while reset_value <= 1800:  # if reset is needed, drone operator will change this channel to the value of ~2000, for 3 seconds
            reset_value = TX_Pixhawk_telem.read_channel8()
            if flightMode and not TX_Pixhawk_telem.is_arm():  # when isArm()==False - the drone is still on the ground
                print("Drone has landed. Exiting main loop")
                break  # the drone has landed, exiting

            try:
                sensors_info2 = TX_Pixhawk_telem.read_information()
                lat_cam = sensors_info2.lat_
                lon_cam = sensors_info2.lon_
                alt_cam = sensors_info2.alt_
                height_cam = sensors_info2.relative_alt_
                lat_cam_med.append(lat_cam), lon_cam_med.append(lon_cam), alt_cam_med.append(alt_cam), height_cam_med.append(height_cam)
                if len(lat_cam_med) == 101:  # to take the median of the last 1s
                    lat_cam_med.pop(0), lon_cam_med.pop(0), alt_cam_med.pop(0), height_cam_med.pop(0)

                time.sleep(0.01)

            except Exception as e:
                print("something's wrong with transmission. Exception is {}".format(e))

        print("\n\nClosing main...")
        periodicProcess.terminate()  # stop working
        periodicProcess.join()  # in order to give the background machinery time to update the status of the object to reflect the termination
        print("Is process {} alive? {}".format(periodicProcess.name, periodicProcess.is_alive()))
        time.sleep(6)  # after a reset command from the operator, it takes ~3 seconds until changed again to default in the Pixhawk
        print("Reset finished")

    # for now - we don't reach here
    TX_Pixhawk_telem.close()
    print("Main closed. Bye")

