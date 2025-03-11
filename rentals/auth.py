import secrets

from datetime import datetime, timezone, timedelta
from urllib.parse import quote

import mysql.connector

from bottle import request, response, HTTPResponse

from . import db


def create_and_insert_session_token(email: str) -> bytes:
    """
    Create a session token and insert it into the DB
    """
    cnx = db.db_cnx()
    with cnx.cursor() as cur:
        expiry_time = datetime.now(timezone.utc) + timedelta(hours=1)
        while True:
            token = secrets.token_bytes(16)
            try:
                cur.execute(
                    """
                    INSERT INTO Session
                    VALUES (_binary %s, %s, %s);
                    """,
                    (token, email, expiry_time),
                )
                cnx.commit()
                break
            except mysql.connector.errors.IntegrityError:
                pass
    return token


def set_session_token(token: bytes):
    """
    Set the session token cookie in the response
    """
    response.set_cookie("Session", token.hex(), maxage=3600, secure=True, httponly=True)


def initialize_session(email: str):
    """
    Create a session token, insert it into the DB, and set the session token
    cookie  in the response
    """
    token = create_and_insert_session_token(email)
    set_session_token(token)


def validate_session_or_refresh() -> bool:
    """
    Returns `True` if the user has a valid session.
    """
    session_token = request.get_cookie("Session")
    if session_token == None:
        return False

    cnx = db.db_cnx()
    with cnx.cursor() as cur:
        session_token = bytes.fromhex(session_token)
        cur.execute(
            """
            SELECT ExpiryTime, Email
            FROM Session
            WHERE Token=_binary %s
            """,
            (session_token,),
        )
        row = cur.fetchone()
        if row == None:
            return False
        expiry_time, email = row
        expiry_time = expiry_time.replace(tzinfo=timezone.utc)
        refresh_time = expiry_time - timedelta(hours=0.5)
        now = datetime.now(timezone.utc)
        if expiry_time >= now:
            if now >= refresh_time:
                initialize_session(email)
                cur.execute(
                    """
                    DELETE FROM Session
                    WHERE Token=_binary %s
                    """,
                    (session_token,),
                )
                cnx.commit()
            return True
    return False


def requires_user_session(func):
    """
    Decorator that ensures that a user is logged in before running the decorated function.
    """

    def inner():
        if validate_session_or_refresh():
            return func()
        else:
            query = request.urlparts[3]
            if query != "":
                query = "?" + query
            raise HTTPResponse(
                status=303,
                location=f"/log-in?return-to={quote(request.urlparts[2] + query)}",
            )

    return inner
