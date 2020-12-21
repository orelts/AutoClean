import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'        #dont change
                      'Server=DESKTOP-N49DF0R;'     #server name can be parsed from name in the SQL SERVER MANAGEMENT
                      'Database=AutoCleanDB;'   #name of the database you want to parse from
                      'Trusted_Connection=yes;')    #dont change
cursor = conn.cursor()

## initiation of SQL for Sensors module
cursor.execute('''
if not exists (select * from sysobjects where name='SensorsInfo' and xtype='U')
	CREATE TABLE dbo.SensorsInfo
	(
	  [ID] int NOT NULL PRIMARY KEY CLUSTERED
	  , [GPS_lat] numeric(20,15) NOT NULL
	  , [GPS_lon] numeric(20,15) NOT NULL
	  , [GPS_alt] numeric(20,15) NOT NULL
	  , [groundspeed] numeric(6,3) NOT NULL
	  , [home_location] numeric(6,3) NOT NULL
	  , [battery] numeric(6,3) NOT NULL
	  , [last_heartbeat] numeric(6,3) NOT NULL
	  , [ValidFrom] datetime2 GENERATED ALWAYS AS ROW START
	  , [ValidTo] datetime2 GENERATED ALWAYS AS ROW END
	  , PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
	 )
	WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.SensorsInfoHistory));

''')

conn.commit()



