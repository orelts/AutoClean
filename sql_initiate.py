"""!
@brief sql_initiate: lazy initializing all the needed sql server tables for the modules interactions.
sql server is Microsoft SQL server.
"""

import pyodbc


## printing updated sql data in a dict way (Column, row). optional to choose table name
def print_sql_row(curs ,table_name = "SensorsInfo"):
    table_rows = curs.execute("SELECT * FROM " + table_name)
    columns = [column[0] for column in curs.description]
    print(columns)
    for row in table_rows:
        for idx in range(len(columns)):
            print(columns[idx], row[idx])


## initiation sql SensorsInfo table (create if not created and insert initial values)
def init_table(curs):

    curs.execute('''
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

    groundspeed_per = 0
    home_location_per = 0
    battery_per = 0
    last_heartbeat_per = 0

    sensors_inf = (str(groundspeed_per), str(home_location_per), str(battery_per), str(last_heartbeat_per),
                   str(groundspeed_per), str(home_location_per), str(battery_per), str(last_heartbeat_per))
    cursor.execute('''
                   IF NOT EXISTS (SELECT * FROM  dbo.SensorsInfo WHERE ID = 1) 

                       INSERT INTO dbo.SensorsInfo(ID, groundspeed, home_location, battery, last_heartbeat)
                       VALUES(1, ?, ?, ?, ?)

                   ELSE

                       UPDATE dbo.SensorsInfo
                       SET groundspeed = ?, home_location = ?, battery = ?, last_heartbeat= ?
                       WHERE ID = 1 ''', sensors_inf)


if __name__ == '__main__':

    server = 'localhost'
    username = 'sa'
    password = 'ItamarOrel1995'
    # database = 'Master' # Replace this with the actual database name from your deployment. If you do not have a database created, you can use Master database.

    db_connection_string = "Driver={FreeTDS};Server=" + server + ";port=1433" + ";UID=" + username + ";PWD=" + password + ";"

    conn = pyodbc.connect(db_connection_string,  autocommit=True)
    cursor = conn.cursor()

    # cursor.execute("CREATE DATABASE AutoCleanDB")
    cursor.execute("USE AutoCleanDB")

    init_table(cursor)
    print_sql_row(cursor)




