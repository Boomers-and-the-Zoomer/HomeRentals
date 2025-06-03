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
from ..util import chain_return_url, pop_return, error


@get("/log-in")
def log_in():
    form = simple_account_form_position(
        simple_account_form(
            "log-in",
            f"""
            <h1>Log in</h1>
            <label for="email">Email:</label>
            <input type="email" name="email" id="email" placeholder="ola.nordmann@gmail.com" required>
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" placeholder="********" required>
            <div id="error-target"></div>
            <button>Log in</button>
            <p class="centered"><a href="reset-password">Forgot your password?</a></p>
            <p class="centered"><a href="{chain_return_url("/sign-up")}">Sign up</a></p>
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
        return error("You were already logged in")

    email = request.forms["email"]
    password = request.forms["password"]

    cnx = db.cnx()
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
        return error("Invalid email and password combination")
    dbhash = dbhash[0]

    # ============= Password validation ============= #

    ph = PasswordHasher()
    try:
        ph.verify(dbhash, password)
    except VerifyMismatchError:
        return error("Invalid email and password combination")

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
        cnx.commmit()

    initialize_session(email)

    cur.execute(
        """
        SELECT EXISTS (
            SELECT *
            FROM User
            WHERE Email=%s
        )
        """,
        (email,),
    )
    first_time = cur.fetchone()[0] == 0

    cur.close()

    if first_time:
        response.status = 303
        response.add_header("Location", chain_return_url("/user-information"))
    else:
        pop_return()
