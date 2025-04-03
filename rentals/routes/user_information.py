from bottle import get, post, request, response

from ..auth import requires_user_session, get_session_token
from ..components import (
    html,
    simple_account_form,
    simple_account_form_position,
    with_navbar,
)
from .. import db


@get("/user-information")
def user_information():
    form = simple_account_form_position(
        simple_account_form(
            "user-information",
            """
            <h1>User information</h1>
            <label for="firstname">First name:</label>
            <input id="firstname" name="firstname" type="text" required>
            <label for="lastname">Last name:</label>
            <input id="lastname"name="lasttname" type="text" required>
            <label for="phonenumber">Phone number:</label>
            <input id="phonenumber" name="phonenumber" type="tel" required>
            <label for="address">Home adress:</label>
            <input id="address" name="address" type="text" required>
            <label for="postcode">Post code:</label>
            <input id="postcode" name="postcode" type="text" required>
            <button>Confirm</button>
            """,
        )
    )
    return html(
        "User iformation",
        with_navbar(f"""
            <main id="user-information">
                <div>
                {form}
                </div>
            </main>
        """),
    )


@post("/user-information")
@requires_user_session()
def user_profile_edit():
    cnx = db.cnx()
    cur = cnx.cursor()

    session_token = get_session_token()

    cur.execute(
        """
        SELECT UserAccount.Email
        FROM UserAccount, Session
        WHERE UserAccount.Email=Session.Email
            AND Session.Token=_binary %s
        """,
        (session_token,),
    )
    (email,) = cur.fetchone()
    cur.close()

    cnx = db.cnx()
    cur = cnx.cursor()

    session_token = get_session_token()

    firstName = request.forms["firstname"]
    lastName = request.forms["lastname"]
    phoneNumber = request.forms["phonenumber"]
    address = request.forms["address"]
    postCode = request.forms["postcode"]

    cur.execute(
        """
        INSERT INTO User
        SET Email = %s, FirstName = %s, LastName = %s, PhoneNumber = %s, HomeAddress = %s, PostalCode = %s
        WHERE User.Email=(
            SELECT Email
            FROM Session
            WHERE Session.Token=_binary %s
            )
        """,
        (email, firstName, lastName, phoneNumber, address, postCode, session_token),
    )

    cnx.commit()
    cur.close()

    response.status = 303
    response.add_header("Location", "/user-information")
