import secrets

from datetime import datetime, timezone, timedelta
from urllib.parse import quote, urlparse

import mysql.connector

from bottle import request, response, HTTPResponse

from .util import push_return
from . import db


def _create_and_insert_session_token(email: str) -> bytes:
    """
    Create a session token and insert it into the DB
    """
    cnx = db.cnx()
    with cnx.cursor() as cur:
        expiry_time = datetime.now(timezone.utc) + timedelta(hours=1)
        failures = 0
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
            except mysql.connector.errors.IntegrityError as e:
                failures += 1
                if failures >= 5:
                    raise e
    return token


def _set_session_token(token: bytes):
    """
    Set the session token cookie in the response
    """
    response.set_cookie("Session", token.hex(), maxage=3600, secure=True, httponly=True)


def initialize_session(email: str) -> bytes:
    """
    Create a session token, insert it into the DB, and set the session token
    cookie  in the response
    """
    token = _create_and_insert_session_token(email)
    _set_session_token(token)
    return token


def get_session_token() -> bytes | None:
    session_token = request.get_cookie("Session")
    if session_token == None:
        return None
    else:
        return bytes.fromhex(session_token)


def get_session_and_refresh() -> bytes | None:
    try:
        return request.session_token
    except AttributeError:
        pass

    session_token = get_session_token()
    if session_token == None:
        return None

    cnx = db.cnx()
    with cnx.cursor() as cur:
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
            return None
        expiry_time, email = row
        expiry_time = expiry_time.replace(tzinfo=timezone.utc)
        refresh_time = expiry_time - timedelta(hours=0.5)
        now = datetime.now(timezone.utc)
        if expiry_time >= now:
            if now >= refresh_time:
                current_token = initialize_session(email)
                cur.execute(
                    """
                    DELETE FROM Session
                    WHERE Token=_binary %s
                    """,
                    (session_token,),
                )
                cnx.commit()
            else:
                current_token = session_token
            request.session_token = session_token
            return current_token
    return None


def validate_session_or_refresh() -> bool:
    """
    Returns `True` if the user has a valid session.
    """
    return get_session_and_refresh() != None


def requires_user_session(referer: bool = False):
    """
    Decorator that ensures that a user is logged in before running the decorated function.
    """

    def inner_decorator(func):
        def inner(*args, **kwargs):
            if validate_session_or_refresh():
                return func(*args, **kwargs)
            else:
                referer_url = None
                if referer:
                    referer_url = request.get_header("Referer")
                push_return("/log-in", referer_url)

        return inner

    return inner_decorator
