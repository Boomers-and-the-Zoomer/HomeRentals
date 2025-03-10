from bottle import route, static_file

from ..components import html, with_navbar
from .. import db

from . import sign_up
from . import search_bar
from . import register_new_listing
from . import book_calendar


@route("/")
def index():
    cnx = db.db_cnx()
    return html(
        "Hello world",
        with_navbar("<h1>Hello world</h1>"),
        body={"class": "foo", "id": "bar"},
    )


@route("/static/<path:path>")
def static(path):
    return static_file(path, "./static")
