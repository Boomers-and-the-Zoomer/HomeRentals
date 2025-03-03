from os import environ

import mysql.connector


def db_cnx_init():
    config = {
        "user": environ["DB_USERNAME"],
        "password": environ["DB_PASSWORD"],
        "host": environ["DB_HOST"],
        "database": "HomeRentals",
        "raise_on_warnings": True,
    }

    cnx = mysql.connector.connect(**config)

    def _db_cnx():
        return cnx

    def _db_cnx_close():
        cnx.close()

    db_cnx = _db_cnx
    db_cnx_close = _db_cnx_close

    return _db_cnx()


db_cnx = db_cnx_init
db_cnx_close = lambda: None
