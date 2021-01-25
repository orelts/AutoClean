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
    db_connection_string = "Driver={FreeTDS};Server=" + server + ";port=1433" + ";UID=" + username + ";PWD=" + password + ";"

    conn = pyodbc.connect(db_connection_string,  autocommit=True)
    cursor = conn.cursor()

    init_database(cursor, conn)
    init__sensors_table(cursor, conn)

    print_sql_row(cursor, "SensorsInfo")




