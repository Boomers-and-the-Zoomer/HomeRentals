from hashlib import sha256

import bottle
import mysql.connector

from dotenv import load_dotenv

from rentals import db, util, routes, auth, icons


def main():
    run_db_update()
    bottle.run(host="localhost", port=8080, reloader=True)
    db.db_cnx_close()


def run_db_update():
    with open("./sql/schema.sql") as f:
        schema = f.read()
    with open("./sql/testData.sql") as f:
        testdata = f.read()
    schema_hash = sha256(schema.encode()).hexdigest()
    testdata_hash = sha256(testdata.encode()).hexdigest()

    cnx = db.db_cnx(no_db=True)
    with cnx.cursor() as cur:

        def run_schema():
            cur.execute(schema)
            cur.execute(testdata)

        try:
            cur.execute("USE HomeRentals;")
        except mysql.connector.errors.ProgrammingError as e:
            raise_if_err_not_ends_with(e, "Unknown database 'homerentals'")

            print("No schema found in the mysql instance")

            run_schema()
            cur.execute("USE HomeRentals;")

            print("-> Schema created")

    # Re-open the database connection to unfuck the connection state
    db.db_cnx_close()
    cnx = db.db_cnx()
    cur = cnx.cursor()

    metadata_existed = False

    def create_and_fill_metadata_table(cur):
        cur.execute(
            """
            CREATE TABLE _metadata (
                SchemaHash CHAR(64),
                TestDataHash CHAR(64)
            )
            """
        )
        # This only gets inserted if the table didn't already exist
        cur.execute(
            """INSERT INTO _metadata (SchemaHash, TestDataHash) VALUES (%s, %s)""",
            (schema_hash, testdata_hash),
        )
        cnx.commit()

    try:
        create_and_fill_metadata_table(cur)
        print("-> Initial hashes inserted")
    except mysql.connector.errors.ProgrammingError as e:
        raise_if_err_not_ends_with(e, "Table '_metadata' already exists")
        metadata_existed = True

    if metadata_existed:
        cur.execute("SELECT * FROM _metadata")
        schema_db_hash, testdata_db_hash = cur.fetchone()
        if schema_db_hash != schema_hash or testdata_db_hash != testdata_hash:
            choice = input(
                "Schema/testdata change detected. Do you wish to re-run the schema and testdata scripts? (Y/n): "
            )
            if choice.lower().startswith("y") or choice == "":
                print("-> Re-running scripts")
                run_schema()
                # Re-open the database connection to unfuck the connection state
                cur.close()
                db.db_cnx_close()
                cnx = db.db_cnx()
                cur = cnx.cursor()
                create_and_fill_metadata_table(cur)
                print("-> DB is updated")
            else:
                print("-> No changes applied")

    print()
    cur.close()
    db.db_cnx_close()


def raise_if_err_not_ends_with(err, string):
    if not str(err).endswith(string):
        raise err


if __name__ == "__main__":
    load_dotenv()
    main()
