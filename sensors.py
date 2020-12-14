print ("Start simulator (SITL)")
import dronekit_sitl
import pyodbc
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

# Get some vehicle attributes (state)
print ("Get some vehicle attribute values:" )
print (" GPS: ", vehicle.gps_0)
print (" Battery: " , vehicle.battery)
print (" Last Heartbeat: " , vehicle.last_heartbeat)
print (" Is Armable?: " , vehicle.is_armable)
print (" System status: ", vehicle.system_status.state)
print (" Mode: ", vehicle.mode.name )   # settable

wait_time = 1
while True :
    cursor.execute('''
    INSERT INTO AutoCleanDB.dbo.SensorsInfo
    SET
        key = 'key', generation = 'generation'
    ON DUPLICATE KEY
    UPDATE key = 'key', generation = (generation + 1)
    ;
    ''')

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
sitl.stop()
print("Completed")

