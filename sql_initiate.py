"""!
@brief sql_initiate: lazy initializing all the needed sql server tables for the modules interactions.
sql server is Microsoft SQL server.
"""

import pyodbc
server = 'localhost' # Replace this with the actual name of your SQL Edge Docker container
username = 'sa' # SQL Server username
password = 'ItamarOrel1995' # Replace this with the actual SA password from your deployment
# database = 'Master' # Replace this with the actual database name from your deployment. If you do not have a database created, you can use Master database.
db_connection_string = "Driver={FreeTDS};Server=" + server + ";port=1433" + ";UID=" + username + ";PWD=" + password + ";"
conn = pyodbc.connect(db_connection_string,  autocommit=True)


## pyodcb handle for accessing and acting on the server
cursor = conn.cursor()

cursor.execute("CREATE DATABASE AutoCleanDB")
cursor.execute("USE AutoCleanDB")

## initiation of SQL for Sensors module
cursor.execute('''

if not exists (select * from sysobjects where name='SensorsInfo' and xtype='U')
	CREATE TABLE dbo.SensorsInfo
	(
	  [ID] int NOT NULL PRIMARY KEY CLUSTERED
	  , [groundspeed] varchar(100) 
	  , [home_location] varchar(100) 
	  , [battery] varchar(100)  
	  , [last_heartbeat] varchar(100) 
	  , [ValidFrom] datetime2 GENERATED ALWAYS AS ROW START
	  , [ValidTo] datetime2 GENERATED ALWAYS AS ROW END
	  , PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
	 )
	WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.SensorsInfoHistory));

''')

for row in cursor.tables():
    print(row.table_name)

conn.commit()



