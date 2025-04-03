from bottle import post, response

from ..auth import get_session_token
from .. import db


@post("/log-out")
def log_out():
    session_token = get_session_token()

    cnx = db.cnx()
    cur = cnx.cursor()

    cur.execute(
        """
        DELETE FROM Session
        WHERE Token=_binary %s
        """,
        (session_token,),
    )
    cnx.commit()

    cur.close()

    response.delete_cookie("Session")
    response.status = 303
    response.add_header("Location", "/")
