"""!
@brief sql_initiate: lazy initializing all the needed sql server tables for the modules interactions.
sql server is Microsoft SQL server.
"""

import pyodbc
from sql_config import *

if __name__ == '__main__':

    server = 'localhost'
    username = 'sa'
    password = 'ItamarOrel1995'
    db_connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=" + server + ";port=1433" + ";UID=" + username + ";PWD=" + password + ";"

    conn = pyodbc.connect(db_connection_string,  autocommit=True)
    cursor = conn.cursor()

    init_database(cursor, conn)
    # drop_table(cursor, conn, "SensorsInfo","SensorsInfoHistory")

    init_sql_table(cursor, conn, "SensorsInfo", d_sensors, True, "SensorsInfoHistory")

    # update_sql(cursor, conn, "SensorsInfo", (str(1), str(5), str(3), str(4)), True, d_sensors)
    
    print_sql_row(cursor, "SensorsInfo")
    print_sql_row(cursor, "SensorsInfoHistory")



