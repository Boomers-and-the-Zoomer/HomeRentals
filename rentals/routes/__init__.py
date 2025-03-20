from bottle import route, static_file, Request

from ..components import html, with_navbar
from .. import db

from . import sign_up
from . import log_in
from . import search_bar
from . import reset_password
from . import view_rental
from . import register_new_listing
from . import book_calendar
from . import user_profile
from . import user_profile_edit
from . import active_bookings
from . import log_out


# Increase this limit to 16MiB so we can actually upload images.
# It's unclear if this is the "proper" way to increase this limit.
Request.MEMFILE_MAX = 16777216


@route("/")
def index():
    return search_bar.search_bar()


@route("/static/<path:path>")
def static(path):
    return static_file(path, "./static")
