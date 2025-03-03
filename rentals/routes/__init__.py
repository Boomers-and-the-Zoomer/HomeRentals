from bottle import route, static_file

from ..components import html
from .. import db


@route("/")
def index():
    # cnx = db.db_cnx()
    return html(
        "Hello world", "<h1>Hello world</h1>", body={"class": "foo", "id": "bar"}
    )


@route("/static/<path:path>")
def static(path):
    return static_file(path, "./static")
