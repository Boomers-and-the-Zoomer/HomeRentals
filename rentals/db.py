from os import environ

import mysql.connector


def db_cnx_init(no_db: bool = False):
    config = {
        "user": environ["DB_USERNAME"],
        "password": environ["DB_PASSWORD"],
        "host": environ["DB_HOST"],
        "raise_on_warnings": True,
    }
    if not no_db:
        config["database"] = "HomeRentals"

    cnx = mysql.connector.connect(**config)

    def _db_cnx():
        return cnx

    def _db_cnx_close():
        db_cnx = db_cnx_init
        db_cnx_close = lambda: None
        cnx.close()

    db_cnx = _db_cnx
    db_cnx_close = _db_cnx_close

    return _db_cnx()


db_cnx = db_cnx_init
db_cnx_close = lambda: None
