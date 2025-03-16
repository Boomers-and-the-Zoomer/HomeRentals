from bottle import route, run, template, request, HTTPError, redirect
from datetime import datetime, timedelta
import urllib.parse  # trengte litt hjelp fra denne for å få riktig format på URL(Hadde problemer med å overføre @)
from urllib.parse import unquote

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
def book_rental():
    PropertyListingID = request.forms.get("PropertyListingID")
    token = request.get_cookie("token")
    raw_from_date = request.forms.get("from_date")
    raw_to_date = request.forms.get("to_date")

    if not token:
        raise HTTPError(403, "User not authenticated")

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

    expiryTime = datetime.now() + timedelta(minutes=15)

    print(
        "Booking rental: PropertyListingID={}, from_date={}, to_date={}".format(
            PropertyListingID, from_date, to_date
        )
    )

    cursor.execute(
        """
    INSERT INTO BookingSession (Token, PropertyListingID, StartTime, EndTime)
    VALUES (%s, %s, %s, %s)
    """,
        (token, PropertyListingID, from_date, to_date),
    )

    cnx.commit()
    cnx.close()

    from_date_str = (
        from_date.isoformat() if hasattr(from_date, "isoformat") else from_date
    )
    encoded_from_date = urllib.parse.quote(from_date_str)

    confirmation_url = "/booking-confirmation/{}/{}".format(
        PropertyListingID, encoded_from_date
    )
    redirect(confirmation_url)


@route("/booking-confirmation/<PropertyListingID>/<from_date>", method="GET")
def booking_confirmation(PropertyListingID, from_date):
    cnx = db.db_cnx()
    cursor = cnx.cursor()

    token = request.get_cookie("token")

    if not token:
        raise HTTPError(403, "User not authenticated")

    decoded_from_date = unquote(from_date)
    property_id = int(PropertyListingID)
    from_date_dt = datetime.fromisoformat(decoded_from_date)

    cursor.execute(  # Dette er midlertidig som cleanup av BookingSessions, vurderer å gjøre den om til en def.
        """DELETE FROM BookingSession WHERE ExpiryTime <= NOW()
    """
    )
    cnx.commit()
    cnx.close()

    cursor.execute(
        """
        SELECT PropertyListingID, StartTime, EndTime, ExpiryTime
        FROM BookingSession
        WHERE Token = %s AND PropertyListingID = %s AND StartTime = %s AND ExpiryTime > NOW()
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
    return html(
        f"Booking confirmation for: {rental[2]}",
        with_navbar(f"""
            <main id="book-confirm">
                <h2>Confirm order</h2>
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
def cancel_temp_booking():
    cnx = db.db_cnx()
    cursor = cnx.cursor()

    property_id = request.forms.get("PropertyListingID")
    token = request.get_cookie("token")
    from_date_str = request.forms.get("from_date")

    from_date_dt = datetime.fromisoformat(from_date_str)

    cursor.execute(
        """
        DELETE FROM BookingSession
        WHERE Token= %s AND PropertyListingID= %s AND StartTime= %s

    """,
        (token, property_id, from_date_dt),
    )

    cnx.commit()
    cnx.close()

    redirect(f"/view-rental/{property_id}")


@route("/finalize-booking", method="POST")
def finalize_booking():
    pass
