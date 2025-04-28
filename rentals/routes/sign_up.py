import mysql.connector

from argon2 import PasswordHasher
from bottle import get, post, request, response

from .. import db
from ..components import (
    html,
    simple_account_form,
    simple_account_form_position,
    with_navbar,
)
from ..util import chain_return_url, error


@get("/sign-up")
def sign_up():
    form = simple_account_form_position(
        simple_account_form(
            "sign-up",
            f"""
            <h1>Sign up</h1>
            <label for="email">Email:</label>
            <input type="email" name="email" id="email" placeholder="ola.nordmann@gmail.com" required>
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" placeholder="********" required>
            <label for="confirm-password">Confirm password:</label>
            <input type="password" name="confirm-password" id="confirm-password" placeholder="********" required>
            <div id="error-target"></div>
            <button>Sign up</button>
            <p class="centered"><a href="{chain_return_url("/log-in")}">Log in</a></p>
            """,
        )
    )
    return html(
        "Sign up",
        with_navbar(f"""
            <main id="sign-up">
                <div>
                {form}
                </div>
            </main>
        """),
    )


@post("/sign-up")
def sign_up_submit():
    email = request.forms["email"]
    password = request.forms["password"]
    confirm_password = request.forms["confirm-password"]

    if password != confirm_password:
        # TODO: Better error handling
        return error("Passwords do not match")
    if "@" not in email or email[-1] == "@" or email[0] in ["@", "+"]:
        # More complex sanity checks are likely not worth it.
        # TODO: Better error handling
        return error("Invalid email")

    ph = PasswordHasher()
    pwhash = ph.hash(password)

    cnx = db.cnx()

    cur = cnx.cursor()
    try:
        cur.execute(
            """INSERT INTO UserAccount(Email, PasswordHash)
               VALUES (%s, %s)""",
            (email, pwhash),
        )
    except mysql.connector.errors.IntegrityError:
        # TODO: Better error handling
        return error("Email is already in use")
    cnx.commit()

    cur.close()

    # TODO: Send actual confirmation email.
    response.status = 303
    response.add_header("Location", chain_return_url("/log-in"))
