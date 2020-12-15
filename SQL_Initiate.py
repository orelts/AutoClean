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
	  , [GPS] varchar(100) NOT NULL
	  , [Battery] varchar(200) NOT NULL
	  , [Last_Heartbeat] numeric(5,3) NOT NULL
	  , [Is_Armable] varchar(5) NOT NULL
	  , [System_status] varchar(100) NOT NULL
	  , [Mode] varchar(100) NOT NULL
	  , [ValidFrom] datetime2 GENERATED ALWAYS AS ROW START
	  , [ValidTo] datetime2 GENERATED ALWAYS AS ROW END
	  , PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
	 )
	WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.SensorsInfoHistory));

''')

conn.commit()



