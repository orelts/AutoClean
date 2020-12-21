print ("Start simulator (SITL)")
import dronekit_sitl
import pyodbc
import time
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

## connecting to the SQL Server
conn = pyodbc.connect('Driver={SQL Server};'        #dont change
                      'Server=DESKTOP-N49DF0R;'     #server name can be parsed from name in the SQL SERVER MANAGEMENT
                      'Database=AutoCleanDB;'   #name of the database you want to parse from
                      'Trusted_Connection=yes;')    #dont change
cursor = conn.cursor()

# Import DroneKit-Python
from dronekit import connect, VehicleMode

# Connect to the Vehicle.
print("Connecting to vehicle on: ", (connection_string,))
vehicle = connect(connection_string, wait_ready=True)

wait_time = 1
count = 0
while True :
    # Get some vehicle attributes (state)
    print ("Get some vehicle attribute values:" )
    print (" GPS: ", vehicle.gps_0)
    print (" Battery: " , vehicle.battery)
    print (" Last Heartbeat: " , vehicle.last_heartbeat)
    print (" Is Armable?: " , vehicle.is_armable)
    print (" System status: ", vehicle.system_status.state)
    print (" Mode: ", vehicle.mode.name )   # settable

    sensors_info = (str(vehicle.gps_0), str(vehicle.battery), vehicle.last_heartbeat,
                    str(vehicle.is_armable), str(vehicle.system_status.state), str(vehicle.mode.name),
                    str(vehicle.gps_0), str(vehicle.battery), vehicle.last_heartbeat,
                    str(vehicle.is_armable), str(vehicle.system_status.state), str(vehicle.mode.name))

    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM  dbo.SensorsInfo WHERE ID = 1)
    
        INSERT INTO dbo.SensorsInfo(ID, GPS, Battery, Last_Heartbeat, Is_Armable, System_status, Mode)
        VALUES(1, ?, ?, ?, ?, ?, ?)
    
    ELSE
    
        UPDATE dbo.SensorsInfo
        SET GPS = ?, Battery = ?, Last_Heartbeat = ?, Is_Armable = ?, System_status = ?, Mode = ?
        WHERE ID = 1
                   ''' ,sensors_info )

    conn.commit()
    time.sleep(wait_time)
    count += 1
    if count == 5 :
        break

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
sitl.stop()
print("Completed")



