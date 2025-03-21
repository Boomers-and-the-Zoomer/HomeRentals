from datetime import datetime, timedelta, timezone
import secrets
from argon2 import PasswordHasher
import mysql.connector
from bottle import get, post, request, response
from .. import db
from ..components import (
    html,
    with_navbar,
    simple_account_form,
    simple_account_form_position,
)


@get("/reset-password")
def reset_password_side():
    form = simple_account_form_position(
        simple_account_form(
            "Reset Password",
            """
            <h1>Reset Password</h1>
            <br>
            <p>Enter your e-mail and we will send you an email with a
            password-reset link</p>
            <br>
            <label>E-mail:</label>
            <input type="email" name="email" id="email" placeholder="Enter your e-mail here">
            <button>Send link</button>
            """,
        )
    )
    return html(
        "Reset Password",
        with_navbar(f"""
                    <main id="reset-password">
                        <div>
                        {form}
                        </div>
                    </main>
                    """),
    )


@post("/reset-password")
def reset_password_side_submit():
    # Checking if submitted email is valid

    email = request.forms["email"]

    cnx = db.db_cnx()
    cur = cnx.cursor()

    cur.execute("SELECT EXISTS (SELECT * FROM UserAccount WHERE Email=%s)", (email,))

    email_exists = cur.fetchone()[0]

    if email_exists == 1:
        # lag et timestamp 24 timer inn i fremtiden
        # retry = True
        # while retry:
        #   generer lenke
        #   prøv å sett inn lenke i db med timestamp
        #   hvis ingen integritetsfeil, retry=False
        expiry_time = datetime.now(timezone.utc) + timedelta(hours=24)
        loop = True
        failures = 0
        while loop:
            token = secrets.token_urlsafe(16)
            try:
                cur.execute(
                    """
                     INSERT INTO ResetLink
                     VALUES (%s,%s,%s)
                     """,
                    (token, email, expiry_time),
                )

                cnx.commit()
                loop = False
            except mysql.connector.errors.IntegrityError as e:
                failures += 1
                if failures >= 5:
                    raise e

    cur.close()

    response.status = 303
    response.add_header("Location", "/reset-password/sent")


@get("/reset-password/sent")
def reset_password_sent():
    return (
        "We have sent the e-mail address submitted a mail with a password reset link."
    )


def reset_token_is_valid(cur, reset_token: str) -> str | None:
    time = datetime.now(timezone.utc)
    cur.execute(
        """
        SELECT Email
        FROM ResetLink
        WHERE Token=%s
            AND ExpiryTime>=%s
        """,
        (reset_token, time),
    )
    email = cur.fetchone()
    return email


@get("/reset-password/<reset_token>")
def reset_password_with_token(reset_token):
    cnx = db.db_cnx()
    cur = cnx.cursor()

    if not reset_token_is_valid(cur, reset_token):
        response.status = 404
        return

    form = simple_account_form_position(
        simple_account_form(
            "Reset Password",
            """
            <h1>Reset Password</h1>
            <br>
            <p>Type in your new password twice</p>        
            <label>New password:</label>
            <input type="password" name="password1" id="password1" placeholder="Password">
            <label>Confirm new password:</label>
            <input type="password" name="password2" id="password2" placeholder="Password">
            <button>Reset Password</button>
            """,
        )
    )

    return html(
        "Reset Password",
        with_navbar(f"""
            <main id="reset-password-with-token">
                <div>
                {form}
                </div>
            </main>
            """),
    )


@post("/reset-password/<reset_token>")
def reset_password_with_token_submit(reset_token):
    # 1. Sjekk at token er gyldig
    # 2. Hvis gylidg, lagre nytt passord
    # 3. Hvis ikke gylidg, 404

    cnx = db.db_cnx()
    cur = cnx.cursor()

    email = reset_token_is_valid(cur, reset_token)
    if email == None:
        response.status = 404
        return

    password1 = request.forms["password1"]
    password2 = request.forms["password2"]

    if password1 != password2:
        response.status = 400
        return "Passwords do not match. Navigate backwards to try again."

    ph = PasswordHasher()
    hash = ph.hash(password1)

    # 1. Oppdater hashen i databasen
    cur.execute
    (
        """
        UPDATE UserAccount
        SET PasswordHash="%s"
        WHERE Email=%s
        """,
        (
            hash,
            email,
        ),
    )

    # 2. Delete reset link i database
    cur.execute(
        """
        DELETE FROM ResetLink
        WHERE Token=%s
        """,
        (reset_token,),
    )

    cnx.commit()

    return "Password updated"
