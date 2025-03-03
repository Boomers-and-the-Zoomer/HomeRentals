import bottle

from dotenv import load_dotenv

from rentals import db, util, routes


def main():
    bottle.run(host="localhost", port=8080, reloader=True)
    db.db_cnx_close()


if __name__ == "__main__":
    load_dotenv()
    main()
