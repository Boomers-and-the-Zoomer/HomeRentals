from bottle import route, run, template, request, HTTPError, redirect
from datetime import datetime, timedelta
import urllib.parse  # trengte litt hjelp fra denne for å få riktig format på URL(Hadde problemer med å overføre @)
from urllib.parse import unquote

from ..auth import requires_user_session, get_session_token
from ..components import html, with_navbar
from .. import db


@route("/view-rental/<PropertyListingID>")
def view_rental(PropertyListingID):
    print("Accessing view-rental", PropertyListingID)
    cnx = db.db_cnx()
    cursor = cnx.cursor()

    cursor.execute(
        """
        SELECT * FROM PropertyListing WHERE PropertyListingID = %s
        """,
        (PropertyListingID,),
    )
    rental = cursor.fetchone()
    print("Rental:", rental)

    if not rental:
        raise HTTPError(404, "Property listing not found")

    return view_rental_template(rental)


def view_rental_template(rental):
    return html(
        f"Rental Unit {rental[2]}",
        with_navbar(f"""
                <main id="book-calendar">
                
                    <h1>Address: {rental[2]}</h1>
                    <ul>Information</ul>
                        <li>Bedrooms: {rental[4]}</li>
                        <li>Bathrooms: {rental[5]}</li>
                        <li>{rental[6]} m²</li>
                        <li>Parking spots: {rental[7]}</li>
                        <li>Kitchens: {rental[8]}</li>
                    <form action="/book-rental" method="post">
                        <label for="from_date">From Date:</label>
                        <input type="datetime-local" id="from_date" name="from_date" required><br>
                        <label for="to_date">To Date:</label>
                        <input type="datetime-local" id="to_date" name="to_date" required><br>
                        <input type="hidden" name="PropertyListingID" value="{rental[0]}">
                        <button type="submit">Book Now</button>
                    </form>
                </main>
        """),
    )


@route("/book-rental", method="POST")
@requires_user_session(referer=True)
def book_rental():
    PropertyListingID = request.forms.get("PropertyListingID")
    raw_from_date = request.forms.get("from_date")
    raw_to_date = request.forms.get("to_date")

    token = get_session_token()

    try:
        from_date = datetime.strptime(raw_from_date, "%Y-%m-%dT%H:%M")
        to_date = datetime.strptime(raw_to_date, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise HTTPError(400, "Invalid date format provided.")

    if from_date >= to_date:
        raise HTTPError(400, "Invalid booking: Start date must be before end date")

    cnx = db.db_cnx()
    cursor = cnx.cursor()
    # Burde nok legge en sjekk for BookingSession her også
    overlappingSjekk = """
        SELECT * FROM Booking
        WHERE PropertyListingID=%s
            AND (StartTime<%s AND EndTime >%s)
    """
    parameterForBooking = (PropertyListingID, to_date, from_date)

    cursor.execute(overlappingSjekk, parameterForBooking)

    if cursor.fetchone() is not None:
        raise HTTPError(400, "Booking dates overlap with an existing booking.")

    print(
        "Booking rental: PropertyListingID={}, from_date={}, to_date={}".format(
            PropertyListingID, from_date, to_date
        )
    )

    expiryTime = datetime.now() + timedelta(
        minutes=15
    )  # TODO: Legg denne inn med JS, slik at brukeren kan se en timer på booking
    cursor.execute(
        """
    INSERT INTO BookingSession (Token, PropertyListingID, StartTime, EndTime, ExpiryTime)
    VALUES (_binary %s, %s, %s, %s, %s)
    """,
        (token, PropertyListingID, from_date, to_date, expiryTime),
    )

    cnx.commit()

    from_date_str = (
        from_date.isoformat() if hasattr(from_date, "isoformat") else from_date
    )
    encoded_from_date = urllib.parse.quote(from_date_str)

    confirmation_url = "/booking-confirmation/{}/{}".format(
        PropertyListingID, encoded_from_date
    )
    redirect(confirmation_url)


@route("/booking-confirmation/<PropertyListingID>/<from_date>", method="GET")
@requires_user_session()
def booking_confirmation(PropertyListingID, from_date):
    cnx = db.db_cnx()
    cursor = cnx.cursor()

    token = get_session_token()

    decoded_from_date = unquote(from_date)
    property_id = int(PropertyListingID)
    from_date_dt = datetime.fromisoformat(decoded_from_date)

    cursor.execute(  # Dette er midlertidig som cleanup av BookingSessions, vurderer å gjøre den om til en def.
        """DELETE FROM BookingSession WHERE ExpiryTime <= NOW()
    """
    )
    cnx.commit()

    cursor.execute(
        """
        SELECT PropertyListingID, StartTime, EndTime, ExpiryTime
        FROM BookingSession
        WHERE Token = _binary %s AND PropertyListingID = %s AND StartTime = %s AND ExpiryTime > NOW()
    """,
        (token, property_id, from_date_dt),
    )

    bConfirmation = cursor.fetchone()

    if not bConfirmation:
        raise HTTPError(404, "Booking not found or session expired")

    cursor.execute(
        """
        SELECT * FROM PropertyListing WHERE PropertyListingID = %s
    """,
        (property_id,),
    )
    rental = cursor.fetchone()
    if not rental:
        raise HTTPError(404, "Property listing not found")

    return booking_confirmation_template(bConfirmation, rental)


def booking_confirmation_template(bConfirmation, rental):
    expiryTime = bConfirmation[3]
    return html(
        f"Booking confirmation for: {rental[2]}",
        with_navbar(f"""
            <main id="book-confirm">
                <h2>Confirm order</h2>
                <input type="hidden" id="expiry_time" name="expiry_time" value="{expiryTime}">
                <h1>Your booking summary for: {rental[2]}</h1>
                <ul>
                    <li>Bedrooms: {rental[4]}</li>
                    <li>Bathrooms: {rental[5]}</li>
                    <li>Area: {rental[6]} m²</li>
                    <li>Kitchens: {rental[8]}</li>
                    <li>Parking spots allocated: {rental[7]}</li><br>
                    <li>Start: {bConfirmation[1]}</li>
                    <li>End: {bConfirmation[2]}</li>
                </ul>
                <form id="finalizeForm" action="/finalize-booking" method="post">
                    <label for="TOS">
                        <input type="checkbox" id="TOS" name="TOS" required>
                        I accept the <a href="https://www.boilerplate.co/terms-of-service" target="_blank">terms and conditions</a>
                    </label>
                    <button type="submit">Finalize booking</button>
                </form>
                <form id="cancelBooking" action="/cancel-temp-booking" method="post">
                    <input type="hidden" name="PropertyListingID" value="{rental[0]}">
                    <input type="hidden" name="from_date" value="{bConfirmation[1]}">
                    <button type="submit">Cancel booking</button>
                </form>
            </main>
        """),
    )


@route("/cancel-temp-booking", method="POST")
@requires_user_session(referer=True)  # Legger til denne ved POST
def cancel_temp_booking():
    cnx = db.db_cnx()
    cursor = cnx.cursor()

    token = get_session_token()
    property_id = request.forms.get("PropertyListingID")
    from_date_str = request.forms.get("from_date")

    from_date_dt = datetime.fromisoformat(from_date_str)

    cursor.execute(
        """
        DELETE FROM BookingSession
        WHERE Token=_binary  %s AND PropertyListingID= %s AND StartTime= %s

    """,
        (token, property_id, from_date_dt),
    )

    cnx.commit()

    redirect(f"/view-rental/{property_id}")


@route("/finalize-booking", method="POST")
@requires_user_session()
def finalize_booking():
    cnx = db.db_cnx()
    cursor = cnx.cursor()

    token = get_session_token()
    property_id = request.forms.get("PropertyListingID")
    from_date_str = request.forms.get("from_date")
    tos = request.forms.get("TOS")

    from_date_dt = datetime.fromisoformat(from_date_str)

    if not token or not tos:
        raise HTTPError(403, "User not authenticated or TOS validation missing")

    cursor.execute(
        """
        SELECT * FROM BookingSession
        WHERE Token=_binary %s AND PropertyListingID= %s AND StartTime= %s
        AND ExpiryTime> NOW()
    
    """,
        (token, property_id, from_date_dt),
    )
    sessionRecord = cursor.fetchone()

    if not sessionRecord:
        raise HTTPError(404, "Booking not found or session expired")
