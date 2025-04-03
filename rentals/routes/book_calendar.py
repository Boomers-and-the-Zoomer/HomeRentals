from bottle import route, run, template, request, HTTPError, redirect
from datetime import datetime, timedelta
import urllib.parse  # trengte litt hjelp fra denne for å få riktig format på URL(Hadde problemer med å overføre @)
from urllib.parse import unquote

from ..auth import requires_user_session, get_session_token
from ..components import html, with_navbar
from .. import db


@route("/view-rental/<listing>")
def view_rental(listing: int):
    cnx = db.cnx()
    cursor = cnx.cursor()

    cursor.execute(
        """
        SELECT PropertyListingID,Address,Description,Bedrooms,Beds,Bathrooms,ParkingSpots
        FROM PropertyListing
        WHERE PropertyListingID=%s
        """,
        (listing,),
    )

    PropertyListingID, address, description, bedrooms, beds, bathrooms, parking = (
        cursor.fetchone()
    )

    cursor.execute(
        """
        SELECT Filename
        FROM PropertyPicture, Picture
        WHERE PropertyPicture.PictureID=Picture.PictureID
            AND PropertyListingID=%s
        """,
        (listing,),
    )
    pictures = cursor.fetchall()
    imgs = [f'src="/static/uploads/{row[0]}" ' for row in pictures]
    while len(imgs) < 5:
        imgs += [""]

    cursor.close()

    var = f"""
    <h1>{address}</h1>
    <div class="left">
        <div class="main-gallery">
            <img {imgs[0]}width=485 height=270>

            <div class="sub-gallery">
                <img {imgs[1]}width=230 height=130>
                <img {imgs[2]}width=230 height=130>
                <img {imgs[3]}width=230 height=130>
                <img {imgs[4]}width=230 height=130>
            </div>
        </div>

        <p>{bedrooms} bedrooms · {beds} beds · {bathrooms} bathrooms · {parking} parking spots</p>
        <p class="description">{description}</p>
    </div>
    <div class="calendar">
    <form action="/book-rental" method="post">
        <label for="from_date">From Date:</label>
        <input type="datetime-local" id="from_date" name="from_date" required><br>
        <label for="to_date">To Date:</label>
        <input type="datetime-local" id="to_date" name="to_date" required><br>
        <input type="hidden" name="PropertyListingID" value="{PropertyListingID}">
        <button type="submit">Book Now</button>
    </form>

    </div>
    """

    return html(
        "View Rental",
        with_navbar(
            f"""
            <main id="view-rental">
            {var}
            </main>
            """
        ),
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

    cnx = db.cnx()
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
    cursor.close()

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
    cnx = db.cnx()
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
        SELECT * FROM PropertyListing
        WHERE PropertyListingID = %s
    """,
        (property_id,),
    )
    rental = cursor.fetchone()
    cursor.close()
    if not rental:
        raise HTTPError(404, "Property listing not found")

    return booking_confirmation_template(bConfirmation, rental)


def booking_confirmation_template(bConfirmation, rental):
    expiryTime = bConfirmation[3]
    return html(
        f"Booking confirmation for: {rental[2]}",
        with_navbar(f"""
            <main id="book-confirm">
                <h1>Confirm order</h1>
                <input type="hidden" id="expiry_time" name="expiry_time" value="{expiryTime}">
                <h2>Your booking summary for: {rental[2]}</h2>
                <ul>
                    <li>Bedrooms: {rental[5]}</li>
                    <li>Beds: {rental[6]}</li>
                    <li>Bathrooms: {rental[7]}</li>
                    <li>Area: {rental[8]} m²</li>
                    <li>Parking spots allocated: {rental[9]}</li>
                    <li>Kitchens: {rental[10]}</li><br>
                    <li>Start: {bConfirmation[1]}</li>
                    <li>End: {bConfirmation[2]}</li>
                </ul>
                <form id="finalizeForm" action="/finalize-booking" method="post">
                    <input type="hidden" name="PropertyListingID" value="{rental[0]}">
                    <input type="hidden" name="from_date" value="{bConfirmation[1].isoformat()}">
                    <label for="TOS">
                        <input type="checkbox" id="TOS" name="TOS" required>
                        I accept the <a href="https://www.boilerplate.co/terms-of-service" target="_blank">terms and conditions</a>
                    </label>
                </form>
                <form id="cancelBooking" action="/cancel-temp-booking" method="post">
                    <input type="hidden" name="PropertyListingID" value="{rental[0]}">
                    <input type="hidden" name="from_date" value="{bConfirmation[1].isoformat()}">
                </form>
                <div>
                <button form="finalizeForm" type="submit">Finalize booking</button>
                <button form="cancelBooking" type="submit">Cancel booking</button>
                </div>
            </main>
        """),
    )


@route("/cancel-temp-booking", method="POST")
@requires_user_session(referer=True)  # Legger til denne ved POST
def cancel_temp_booking():
    cnx = db.cnx()
    cursor = cnx.cursor()

    token = get_session_token()
    property_id = request.forms.get("PropertyListingID")
    from_date_str = request.forms.get("from_date")
    if not from_date_str:
        raise HTTPError(400, "Missing start date for booking.")

    from_date_dt = datetime.fromisoformat(from_date_str)

    cursor.execute(
        """
        DELETE FROM BookingSession
        WHERE Token=_binary  %s AND PropertyListingID= %s AND StartTime= %s
        """,
        (token, property_id, from_date_dt),
    )

    cnx.commit()
    cursor.close()

    redirect(f"/view-rental/{property_id}")


@route("/finalize-booking", method="POST")
@requires_user_session()
def finalize_booking():
    cnx = db.cnx()
    cursor = cnx.cursor(buffered=True)

    token = get_session_token()
    property_id = request.forms.get("PropertyListingID")
    tos = request.forms.get("TOS")
    from_date_str = request.forms.get("from_date")
    if not from_date_str:
        raise HTTPError(400, "Missing start date for booking.")

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

    cursor.execute(
        """
        SELECT BookingSession.PropertyListingID, BookingSession.StartTime, BookingSession.EndTime, User.Email
        FROM BookingSession, Session, User
        WHERE BookingSession.Token=Session.Token
            AND Session.Email=User.Email
            AND BookingSession.Token=_binary %s
        """,
        (token,),
    )
    CompleteBooking = cursor.fetchone()

    if CompleteBooking is None:
        raise HTTPError(404, "Failed to retrive complete booking details")

    if CompleteBooking is not None:
        property_listing_id = CompleteBooking[0]
        start_time = CompleteBooking[1]
        end_time = CompleteBooking[2]
        email = CompleteBooking[3]

    cursor.execute(
        """
        INSERT INTO Booking (PropertyListingID, StartTime, EndTime, Email)
        VALUES (%s, %s, %s, %s)
        """,
        (property_listing_id, start_time, end_time, email),
    )
    cnx.commit()
    cursor.close()

    redirect(f"/bookings/active")
