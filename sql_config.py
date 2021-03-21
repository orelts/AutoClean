import pyodbc

d_sensors = {
    "alt": "0",
    "heading_": "0",
    "relative_alt": "0",
    "groundspeed": "0",
    # "home_location": "0",
    "last_heartbeat": "0",
}


def drop_table(cursor, conn, table, history_table=None):

    if history_table is None:
        cursor.execute('''DROP TABLE AutoCleanDB.dbo.''' + table)
    else:
        cursor.execute(''' ALTER TABLE dbo.''' + table + ''' SET (SYSTEM_VERSIONING = OFF)
                      DROP TABLE AutoCleanDB.dbo.''' + table + '''
                      DROP TABLE AutoCleanDB.dbo.''' + history_table)

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
def init_sql_table(curs, conn, table, sql_dict, is_one_row, history_table=None):
    sql_columns = ""
    for key, value in sql_dict.items():
        sql_columns += ", [" + key + "]" + " varchar(100)\n"

    if history_table is None:
        history_str = ""
    else:
        history_str = "WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo." + history_table + "))"
    if is_one_row:
        incremental_id_str = ""
    else:
        incremental_id_str = "IDENTITY(1,1)"

    curs.execute('''
    if not exists (select * from sysobjects where name=\'''' + table + '''\' and xtype='U')
        CREATE TABLE dbo.''' + table + '''
        (
          [ID] int ''' + incremental_id_str + ''' NOT NULL PRIMARY KEY CLUSTERED
          ''' + sql_columns + '''
          , [ValidFrom] datetime2 GENERATED ALWAYS AS ROW START
          , [ValidTo] datetime2 GENERATED ALWAYS AS ROW END
          , PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
         )
        ''' + history_str + ''';
    ''')

    conn.commit()

    initial_info = [v for k, v in sql_dict.items()][0:]

    data_line = ""
    for key, value in sql_dict.items():
        data_line += key + ","
    data_line = data_line[:-1]

    n = len(sql_dict)
    values_str = ',?' * len(sql_dict)
    if is_one_row:
        values_str = "1" + values_str
        data_line = "ID," + data_line
    else:
        values_str = values_str[1:]

    curs.execute('''
                   IF NOT EXISTS (SELECT * FROM  dbo.''' + table + ''' WHERE ID = 1) 
                       INSERT INTO dbo.'''+table + '''(''' + data_line + ''')
                       VALUES(''' + values_str + ''')
                    ''', initial_info
                 )

    conn.commit()


def connect_to_db():
    server = 'localhost'
    username = 'sa'
    password = 'ItamarOrel1995'
    db_connection_string = "Driver={FreeTDS};Server=" + server + ";port=1433" + ";UID=" + username + ";PWD=" + password + ";"

    conn = pyodbc.connect(db_connection_string,  autocommit=True)
    cursor = conn.cursor()
    init_database(cursor, conn)

    return conn, cursor


def update_sql(curs, conn, table, data, is_one_row, sql_dict):
    data_line = ""

    if is_one_row:
        for key, value in sql_dict.items():
            data_line += key + "=?,"
        data_line = data_line[:-1]

        curs.execute('''
                    UPDATE dbo.''' + table + '''
                    SET ''' + data_line + '''
                    WHERE ID = 1 ''', data)
    else:
        for key, value in sql_dict.items():
            data_line += key + ","
        data_line = data_line[:-1]

        n = len(sql_dict)
        values_str = ',?' * len(sql_dict)
        values_str = values_str[1:]

        curs.execute('''
                        INSERT INTO dbo.''' + table + '''(''' + data_line + ''')
                        VALUES(''' + values_str + ''')
                        ''', data
                     )

    conn.commit()


## printing updated sql data in a dict way (Column, row). optional to choose table name
def print_sql_row(curs, table_name="SensorsInfo"):
    table_rows = curs.execute("SELECT * FROM " + table_name)
    columns = [column[0] for column in curs.description]
    print(columns)
    for row in table_rows:
        for idx in range(len(columns)):
            print(columns[idx], row[idx])


