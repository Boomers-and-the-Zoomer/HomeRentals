from os import environ

import mysql.connector


def db_cnx_init(no_db: bool = False):
    global cnx
    global cnx_close

    config = {
        "user": environ["DB_USERNAME"],
        "password": environ["DB_PASSWORD"],
        "host": environ["DB_HOST"],
        "raise_on_warnings": True,
    }
    if not no_db:
        config["database"] = "HomeRentals"

    my_cnx = mysql.connector.connect(**config)

    def _db_cnx():
        print("_db_cnx")
        return my_cnx

    def _db_cnx_close():
        global cnx
        global cnx_close
        cnx = db_cnx_init
        cnx_close = lambda: None
        my_cnx.close()

    cnx = _db_cnx
    cnx_close = _db_cnx_close

    return my_cnx


cnx = db_cnx_init
cnx_close = lambda: None
