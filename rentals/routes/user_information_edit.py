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


@get("/user-information/edit")
def user_information():
    cnx = db.cnx()
    cur = cnx.cursor()
    session_token = get_session_token()
    cur.execute(
        """
        SELECT FirstName,LastName,PhoneNumber,HomeAddress,PostalCode
        FROM User, Session
        WHERE User.Email=Session.Email
            AND Session.Token=_binary %s
        """,
        (session_token,),
    )
    (first_name, last_name, phone_number, home_address, post_code) = cur.fetchone()
    form = simple_account_form_position(
        simple_account_form(
            "user-information-edit",
            f"""
            <h1>User information</h1>
            <label for="firstname">First name:</label>
            <input id="firstname" name="firstname" type="text" required value="{first_name}">
            <label for="lastname">Last name:</label>
            <input id="lastname"name="lastname" type="text" required value="{last_name}">
            <label for="phonenumber">Phone number:</label>
            <input id="phonenumber" name="phonenumber" type="tel" required value="{phone_number}">
            <label for="address">Home address:</label>
            <input id="address" name="address" type="text" required value="{home_address}">
            <label for="postcode">Post code:</label>
            <input id="postcode" name="postcode" type="text" required value="{post_code}">
            <div id="error-target"></div>
            <button>Confirm</button>
            <p class="centered"><a href="http://localhost:8080/user-profile">Cancel</a></p>
            """,
        )
    )
    return html(
        "User iformation edit",
        with_navbar(f"""
            <main id="user-information">
                <div>
                {form}
                </div>
            </main>
        """),
    )


@post("/user-information/edit")
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
        query_params = [firstName, lastName, phoneNumber, address, postCode]
        query_params.append(session_token)
        cur.execute(
            f"""
            UPDATE User
            SET FirstName = %s, LastName = %s, PhoneNumber = %s, HomeAddress = %s, PostalCode = %s
            WHERE User.Email=(
                SELECT Email
                FROM Session
                WHERE Session.Token=_binary %s
            )
            """,
            tuple(query_params),
        )
    except mysql.connector.errors.DataError as e:
        if "Data too long for column 'FirstName'" in str(e):
            return error("First name is too long. Up to 30 symbols is allowed.")
        if "Data too long for column 'LastName'" in str(e):
            return error("Last name is too long. Up to 30 symbols is allowed.")
        if "Data too long for column 'PhoneNumber'" in str(e):
            return error(
                "Phone number is too long. Up to 16 symbols is allowed."
            )
        if "Data too long for column 'HomeAddress'" in str(e):
            return error(
                "Home adress is too long. Up to 100 symbols is allowed."
            )
        if "Data too long for column 'PostalCode'" in str(e):
            return error(
                "Postal code is too long. Up to 10 symbols is allowed."
            )
        return error("Unexpected server error")

    cnx.commit()
    cur.close()

    pop_return("/user-profile")
