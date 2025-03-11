from urllib.parse import unquote

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from bottle import get, post, request, response

from ..auth import validate_session_or_refresh, initialize_session
from ..components import (
    html,
    simple_account_form,
    simple_account_form_position,
    with_navbar,
)
from .. import db


@get("/log-in")
def log_in():
    form = simple_account_form_position(
        simple_account_form(
            "log-in",
            """
            <h1>Log in</h1>
            <label for="email">Email:</label>
            <input type="email" name="email" id="email" placeholder="ola.nordmann@gmail.com" required>
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" placeholder="********" required>
            <button>Log in</button>
            <p class="centered"><a href="reset-password">Forgot your password?</a></p>
            <p class="centered">Don't have an account?</p>
            <p class="centered"><a href="sign-up">Sign up instead</a></p>
            """,
        )
    )
    return html(
        "Log in",
        with_navbar(f"""
            <main id="log in">
                <div>
                    {form}
                </div>
            </main>
        """),
    )


@post("/log-in")
def log_in_submit():
    if validate_session_or_refresh():
        return html("Notice", "You were already logged in")

    email = request.forms["email"]
    password = request.forms["password"]

    cnx = db.db_cnx()
    cur = cnx.cursor()

    cur.execute(
        """
        SELECT PasswordHash
        FROM UserAccount
        WHERE Email=%s
        """,
        (email,),
    )
    dbhash = cur.fetchone()
    if dbhash == None:
        return html("Error", "Invalid email and password combination")
    dbhash = dbhash[0]

    # ============= Password validation ============= #

    ph = PasswordHasher()
    try:
        ph.verify(dbhash, password)
    except VerifyMismatchError:
        return html("Error", "Invalid email and password combination")

    # ============= Password is valid below this line ============= #

    # If the password hasher's parameters don't match what's in the DB, update
    # the hash in the DB to be hashed with the new parameters.
    if ph.check_needs_rehash(dbhash):
        new_hash = ph.hash(password)
        cur.execute(
            """
            UPDATE UserAccount
            WHERE Email=%s
            SET PasswordHash=%s
            """,
            (email, new_hash),
        )

    initialize_session(email)

    response.status = 303
    try:
        return_to = unquote(request.query["return-to"])
        response.add_header("Location", return_to)
    except KeyError:
        response.add_header("Location", "/")
