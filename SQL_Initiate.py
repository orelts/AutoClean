import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'        #dont change
                      'Server=localhost;'     #server name can be parsed from name in the SQL SERVER MANAGEMENT
                      'Database=AutoCleanDB;'   #name of the database you want to parse from
                      'uid=sa;'
                      'pwd=ItamarOrel2020;')    #dont change
cursor = conn.cursor()


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

conn.commit()



