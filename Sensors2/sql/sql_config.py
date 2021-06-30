"""!
@brief sql_config: function for easy sql use for the sensors tables, to read and insert in many use cases.
the table is parsed from the dictionary so if dictionary is changes need to drop table and init again using init_sql_table(cursor, conn, "SensorsInfo", d_sensors, False)
"""

from __future__ import print_function
import pyodbc
import pandas as pd

d_sensors = {
    "alt": "0",
    "heading_": "0",
    "relative_alt": "0",
    "groundspeed": "0",
    # "home_location": "0",
    "last_heartbeat": "0",
}


## deletes a table from the SQL
def drop_table(cursor, conn, table, history_table=None):

    if history_table is None:
        cursor.execute('''DROP TABLE ''' + table)
    else:
        cursor.execute(''' ALTER TABLE ''' + table + ''' SET (SYSTEM_VERSIONING = OFF)  
                        DROP TABLE AutoCleanDB.dbo.''' + table + ''' 
                        DROP TABLE AutoCleanDB.dbo.''' + history_table)

    conn.commit()

## opens a new database in the server
def init_database(curs, conn):
    curs.execute('''
                    IF EXISTS 
                       (
                         SELECT name FROM master.dbo.sysdatabases 
                        WHERE name = N'AutoCleanDB'
                        )
                    BEGIN
                        SELECT 'Database Name already Exist' AS Message
                    END
                    ELSE
                    BEGIN
                        CREATE DATABASE [AutoCleanDB]
                        SELECT 'AutoCleanDB is Created'
                    END
                         '''
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

## connects to the database in order to uses the tables inside
def connect_to_db():
    server = 'localhost'
    username = 'sa'
    password = 'nvidia19951994'
    db_connection_string = "Driver={FreeTDS};Server=" + server + ";port=1433" + ";UID=" + username + ";PWD=" + password + ";"

    conn = pyodbc.connect(db_connection_string,  autocommit=True)
    cursor = conn.cursor()
    init_database(cursor, conn)

    return conn, cursor

## in order to insert a line to a table.
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
        values_str = ',?' * n
        values_str = values_str[1:]

        curs.execute('''
                    INSERT INTO dbo.''' + table + '''(''' + data_line + ''')
                    VALUES(''' + values_str + ''')
                    ''', data
                     )

    conn.commit()


def get_column_idx(curs, table_name, field):
    curs.execute("SELECT * FROM " + table_name)
    columns = [column[0] for column in curs.description]
    for idx in range(len(columns)):
        if field == columns[idx]:
            return idx
    return None


## printing updated sql data in a dict way (Column, row). optional to choose table name and number of last rows to print
def print_sql_row(curs, table_name="SensorsInfo", num_of_last_rows=None):
    if num_of_last_rows == None:
        table_rows = curs.execute("SELECT TOP " + str(num_of_last_rows) + " FROM " + table_name + " ORDER BY ID DESC")
    else:
        table_rows = curs.execute("SELECT * FROM " + table_name)
    columns = [column[0] for column in curs.description]
    print(columns)
    for row in table_rows:
        for idx in range(len(columns)):
            print(row[idx],  end=', ')
        print("")

def get_last_table_elem(curs, field, table_name):
    query = "SELECT MAX(id) FROM " + table_name
    ID = curs.execute(query).fetchone()
    query = "SELECT " + field + " FROM " + table_name + " WHERE ID = " + str(ID[0])
    x = curs.execute(query).fetchone()
    return x[0]



def get_top_table_elem(curs, field, table_name, top):
    query = "SELECT TOP " + str(top) + " " + field + " FROM " + table_name + " ORDER BY ID DESC"
    x = curs.execute(query).fetchall()
    lst = []
    for i in range(top):
        lst.append(x[i][0])
    return lst



## returns entire row with the input id
def get_row_by_id(curs, ID, table_name):
    table_row = curs.execute("SELECT * FROM " + table_name + " WHERE ID = " + str(ID)).fetchall()
    return table_row



## will later be used to determine if there exists a row which wasnt already executed
def get_row_by_condition(curs, condition, table_name):
    query = "SELECT ID FROM " + table_name + " WHERE " + condition
    ID = curs.execute(query).fetchone()
    if ID == None:
        return None, None
    row = get_row_by_id(curs, ID[0], table_name)
    return ID[0], row


def set_element_in_row(curs, elem, ID, table_name, new_val):
    query = "SELECT " + elem + " FROM " + table_name + " WHERE ID = " + str(ID)
    curs.execute(query)
    set = '''UPDATE dbo.''' + table_name + ''' SET ''' + elem  + '''=''' + new_val +''' WHERE ID='''  + str(ID)
    curs.execute(set)


## will later be used to raise a status of a row to "already excuted"
def set_element_by_condition(curs, elem, condition, table_name, new_val):
    query = "SELECT ID FROM " + table_name + " WHERE " + condition
    ID = curs.execute(query).fetchnone()
    set_element_in_row(curs, elem, ID[0], table_name, new_val)

def sql_to_excel(conn, table, file_path):
        pd.read_sql('SELECT * FROM ' + table, conn).to_excel(file_path)


