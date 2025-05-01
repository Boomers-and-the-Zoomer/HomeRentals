import mysql.connector

from bottle import get, post, request, response

from ..auth import requires_user_session, get_session_token
from ..components import (
    html,
    simple_account_form,
    simple_account_form_position,
    with_navbar,
)
from .. import db
from ..util import pop_return, chain_return_url, get_return_url_or, error


@get("/user-information")
def user_information():
    cnx = db.cnx()
    cur = cnx.cursor()
    session_token = get_session_token()
    cur.execute(
        """
        SELECT User.Email
        FROM User, Session
        WHERE User.Email=Session.Email
            AND Session.Token=_binary %s
        """,
        (session_token,),
    )
    row = cur.fetchone()
    if row != None:
        response.status = 303
        response.add_header("Location", "/")
        cur.close()
        return

    form = simple_account_form_position(
        simple_account_form(
            "user-information",
            f"""
            <h1>User information</h1>
            <label for="firstname">First name:</label>
            <input id="firstname" name="firstname" type="text" required>
            <label for="lastname">Last name:</label>
            <input id="lastname"name="lastname" type="text" required>
            <label for="phonenumber">Phone number:</label>
            <input id="phonenumber" name="phonenumber" type="tel" required>
            <label for="address">Home address:</label>
            <input id="address" name="address" type="text" required>
            <label for="postcode">Post code:</label>
            <input id="postcode" name="postcode" type="text" required>
            <div id="error-target"></div>
            <button>Confirm</button>
            <p class="centered"><a href={get_return_url_or("/")}>Do it later</a></p>
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

    try:
        cur.execute(
            """
            INSERT INTO User (Email, FirstName, LastName, Phonenumber, HomeAddress, PostalCode)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (email, firstName, lastName, phoneNumber, address, postCode),
        )
    except mysql.connector.errors.DataError as e:
        if "Data too long for column 'FirstName'" in str(e):
            return error("First name is too long. Up to 30 symbols is allowed.")
        else:
            if "Data too long for column 'LastName'" in str(e):
                return error("Last name is too long. Up to 30 symbols is allowed.")
            else:
                if "Data too long for column 'PhoneNumber'" in str(e):
                    return error("Phone number is too long. Up to 16 symbols is allowed.")
                else: 
                    if "Data too long for column 'HomeAddress'" in str(e):
                        return error("Home adress is too long. Up to 100 symbols is allowed.")
                    else:
                        if "Data too long for column 'PostalCode'" in str(e):
                            return error("Postal code is too long. Up to 10 symbols is allowed.")
                        else:
                            return error("Unexpected server error")
    
    cnx.commit()
    cur.close()

    pop_return("/")
