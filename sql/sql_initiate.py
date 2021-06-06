"""!
@brief sql_initiate: lazy initializing all the needed sql server tables for the modules interactions.
sql server is Microsoft SQL server.
"""


from sql.sql_config import *


if __name__ == '__main__':

    conn, cursor = connect_to_db()
    init_database(cursor, conn)


    init_sql_table(cursor, conn, "SensorsInfo", d_sensors, False)
    init_sql_table(cursor, conn, "lift", d_lift, False)
    init_sql_table(cursor, conn, "driver", d_driver, False)

    update_sql(cursor, conn, "driver", (90, 60, 5, "0"), False, d_driver)
    update_sql(cursor, conn, "driver", (90, 60, 5, "0"), False, d_driver)
    update_sql(cursor, conn, "driver", (90, 60, 5, "0"), False, d_driver)
    update_sql(cursor, conn, "driver", (90, 60, 5, "0"), False, d_driver)
    update_sql(cursor, conn, "driver", (90, 60, 5, "0"), False, d_driver)
    update_sql(cursor, conn, "driver", (90, 60, 5, "0"), False, d_driver)

    print_sql_row(cursor, "driver")
    # update_sql(cursor, conn, "SensorsInfo", (str(1), str(5), str(3), str(4)), True, d_sensors)
