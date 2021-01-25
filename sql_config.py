
d_sensors = {
    "groundspeed": "0",
    "home_location": "0",
    "battery": "0",
    "last_heartbeat": "0"
}


def drop_table(cursor, conn, table, history_table = None):
    cursor.execute('''ALTER TABLE dbo.''' + table + ''' SET (SYSTEM_VERSIONING = OFF)
                      DROP TABLE AutoCleanDB.dbo.''' + table)
    if history_table is not None:
        cursor.execute(''' DROP TABLE AutoCleanDB.dbo.''' + history_table)

    conn.commit()


def init_database(curs, conn):
    curs.execute('''
                    IF EXISTS (SELECT name FROM master.sys.databases WHERE name = N'AutoCleanDB')
                        USE AutoCleanDB
                    ELSE
                         CREATE DATABASE AutoCleanDB'''
                 )
    conn.commit()


## initiation sql SensorsInfo table (create if not created and insert initial values)
def init__sensors_table(curs, conn):
    sensors_sql_columns = ""
    for key,value in d_sensors.items():
        sensors_sql_columns += ", [" + key + "]" + " varchar(100)\n"

    curs.execute('''
    if not exists (select * from sysobjects where name='SensorsInfo' and xtype='U')
        CREATE TABLE dbo.SensorsInfo
        (
          [ID] int NOT NULL PRIMARY KEY CLUSTERED
          ''' + sensors_sql_columns + '''
          , [ValidFrom] datetime2 GENERATED ALWAYS AS ROW START
          , [ValidTo] datetime2 GENERATED ALWAYS AS ROW END
          , PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
         )
        WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.SensorsInfoHistory));
    ''')
    conn.commit()

    initial_sensors_info = [(v) for k, v in d_sensors.items()][0:]


    sensors_data_line = ""
    for key, value in d_sensors.items():
        sensors_data_line += key + ","
    sensors_data_line = sensors_data_line[:-1]


    n = len(d_sensors)
    values_str = ',?' * len(d_sensors)
    curs.execute('''
                   IF NOT EXISTS (SELECT * FROM  dbo.SensorsInfo WHERE ID = 1) 

                       INSERT INTO dbo.SensorsInfo( ID, ''' + sensors_data_line + ''')
                       VALUES(1''' + values_str + ''')
                    ''', initial_sensors_info
                )

    conn.commit()


def update_sensors_sql_row(curs, conn, data):
    sensors_data_line = ""

    for key, value in d_sensors.items():
        sensors_data_line += key + "=?,"

    sensors_data_line = sensors_data_line[:-1]
    print(sensors_data_line)
    curs.execute('''
                UPDATE dbo.SensorsInfo
                SET ''' + sensors_data_line + '''
                WHERE ID = 1 ''', data)

    conn.commit()


## printing updated sql data in a dict way (Column, row). optional to choose table name
def print_sql_row(curs ,table_name = "SensorsInfo"):
    table_rows = curs.execute("SELECT * FROM " + table_name)
    columns = [column[0] for column in curs.description]
    print(columns)
    for row in table_rows:
        for idx in range(len(columns)):
            print(columns[idx], row[idx])


