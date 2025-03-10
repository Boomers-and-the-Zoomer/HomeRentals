import mysql.connector

from argon2 import PasswordHasher
from bottle import get, post, request


from ..components import html, with_navbar
from .. import db


@get("/sign-up")
def sign_up():
    return html(
        "Sign up",
        with_navbar("""
            <main id="sign-up">
                <div>
                    <form name="sign-up" id="sign-up" action="" method="post">
                        <h1>Sign up</h1>
                        <label for="email">Email:</label>
                        <input type="email" name="email" id="email" placeholder="ola.nordmann@gmail.com" required>
                        <label for="password">Password:</label>
                        <input type="password" name="password" id="password" placeholder="********" required>
                        <label for="confirm-password">Confirm password:</label>
                        <input type="password" name="confirm-password" id="confirm-password" placeholder="********" required>
                        <button>Sign up</button>
                        <p>Already have an account?</p>
                        <p><a href="login">Log in instead</a></p>
                    </form>
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
        return html("Passwords do not match")
    if "@" not in email or email[-1] == "@" or email[0] in ["@", "+"]:
        # More complex sanity checks are likely not worth it.
        # TODO: Better error handling
        return html("Error", "Invalid email")

    ph = PasswordHasher()
    pwhash = ph.hash(password)

    cnx = db.db_cnx()

    cur = cnx.cursor()
    try:
        cur.execute(
            """INSERT INTO UserAccount(Email, PasswordHash)
               VALUES (%s, %s)""",
            (email, pwhash),
        )
    except mysql.connector.errors.IntegrityError:
        # TODO: Better error handling
        return html("Error", "Email is already in use")
    cnx.commit()

    cur.close()

    # TODO: Send actual confirmation email.
    return html("Account registered", "Account registered")
