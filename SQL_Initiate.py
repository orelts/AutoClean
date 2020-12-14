import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'        #dont change
                      'Server=DESKTOP-N49DF0R;'     #server name can be parsed from name in the SQL SERVER MANAGEMENT
                      'Database=AutoCleanDB;'   #name of the database you want to parse from
                      'Trusted_Connection=yes;')    #dont change
cursor = conn.cursor()

## initiation of SQL for Sensors module
cursor.execute('''
CREATE TABLE [IF NOT EXISTS] AutoCleanDB.dbo.SensorsInfo
(
  [KEY] int NOT NULL PRIMARY KEY CLUSTERED
  , [GPS] nvarchar(100) NOT NULL
  , [Battery] varchar(100) NOT NULL
  , [Last Heartbeat] varchar(100) NOT NULL
  , [Is Armable?] nvarchar(1024) NOT NULL
  , [System status] decimal (10,2) NOT NULL
  , [Mode] decimal (10,2) NOT NULL
  , [ValidFrom] datetime2 GENERATED ALWAYS AS ROW START
  , [ValidTo] datetime2 GENERATED ALWAYS AS ROW END
  , PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
 )
WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.EmployeeHistory));
''')



