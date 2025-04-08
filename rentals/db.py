import inspect
from os import environ, getcwd
from pathlib import Path

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

    def oops_you_closed_the_db():
        raise Exception(
            "You have accidentally closed the database. Don't do that, please and thank you :)"
        )

    my_cnx._super_secret_lose = my_cnx.close
    my_cnx.close = oops_you_closed_the_db

    # Cursor lifecycle debugging
    if False:
        real_cursor = my_cnx.cursor

        my_cnx._my_cursors = set()

        def my_cursor(*args, **kwargs):
            cursor = real_cursor(*args, **kwargs)
            info = get_project_frame_and_file()
            if info != None:
                my_cnx._my_cursors.add(cursor)
                real_close = cursor.close

                def my_cursor_close():
                    real_close()
                    my_cnx._my_cursors.remove(cursor)
                    info = get_project_frame_and_file()
                    print(
                        f"[{info[1]}:{info[0].lineno}] Cursor removed. Current sum is: {len(my_cnx._my_cursors)}"
                    )

                cursor.close = my_cursor_close
                print(
                    f"[{info[1]}:{info[0].lineno}] Cursor added. Current sum is: {len(my_cnx._my_cursors)}"
                )
            return cursor

        my_cnx.cursor = my_cursor

    def _db_cnx():
        print("_db_cnx")
        return my_cnx

    def _db_cnx_close():
        global cnx
        global cnx_close
        cnx = db_cnx_init
        cnx_close = lambda: None
        my_cnx._super_secret_lose()

    cnx = _db_cnx
    cnx_close = _db_cnx_close

    return my_cnx


def get_project_frame_and_file():
    # Skips internal mysql-connector-python sillyness
    extern_frame_budget = 1
    for frame in inspect.getouterframes(inspect.currentframe()):
        cwd = Path(getcwd())
        file = Path(frame.filename)
        if file.name != "db.py":
            for parent in file.parents:
                if parent.name == ".venv":
                    if extern_frame_budget != 0:
                        extern_frame_budget -= 1
                        break
                    else:
                        return None
                if cwd == parent and file.name != "db.py":
                    return frame, file.relative_to(cwd)


cnx = db_cnx_init
cnx_close = lambda: None
