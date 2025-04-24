from bottle import route, run, template, request, HTTPError, redirect, response
from datetime import datetime, timedelta
import urllib.parse  # trengte litt hjelp fra denne for å få riktig format på URL(Hadde problemer med å overføre @)
from urllib.parse import unquote

from ..auth import requires_user_session, get_session_token
from ..components import html, with_navbar
from .. import db


@route("/view-rental/<listing>")
def view_rental(listing: int):
    from_date = request.get_cookie("from_date", "") or ""
    to_date = request.get_cookie("to_date", "") or ""

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
            <input type="date" id="from_date" name="from_date" required value="{from_date}"><br>
            <label for="to_date">To Date:</label>
            <input type="date" id="to_date" name="to_date" required value="{to_date}"><br>
            <input type="hidden" name="PropertyListingID" value="{PropertyListingID}"><br>
            <div class="buttons">
                <button class="button_confirm" type="submit">Book Now</button>
            </div>
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


def book_rental_pre_auth_hook():
    from_date = request.forms.get("from_date", "")
    to_date = request.forms.get("to_date", "")

    response.set_cookie("from_date", from_date, maxage=15 * 60)
    response.set_cookie("to_date", to_date, maxage=15 * 60)


@route("/book-rental", method="POST")
@requires_user_session(referer=True, pre_auth_hook=book_rental_pre_auth_hook)
def book_rental():
    raw_from_date = request.forms.get("from_date")
    raw_to_date = request.forms.get("to_date")
    PropertyListingID = request.forms.get("PropertyListingID")
    token = get_session_token()

    try:
        from_date = datetime.strptime(raw_from_date, "%Y-%m-%d")
        to_date = datetime.strptime(raw_to_date, "%Y-%m-%d")
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

    cursor.execute("""DELETE FROM BookingSession WHERE ExpiryTime <= NOW()""")
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

    confirmation_url = f"/booking-confirmation/{PropertyListingID}"
    redirect(confirmation_url)


@route("/booking-confirmation/<PropertyListingID>", method="GET")
@requires_user_session()
def booking_confirmation(PropertyListingID):
    cnx = db.cnx()
    cursor = cnx.cursor()

    token = get_session_token()

    property_id = int(PropertyListingID)

    cursor.execute(
        """
        SELECT PropertyListingID, StartTime, EndTime, ExpiryTime
        FROM BookingSession
        WHERE Token = _binary %s AND PropertyListingID = %s AND ExpiryTime > NOW()
        """,
        (token, property_id),
    )

    bConfirmation = cursor.fetchone()

    if not bConfirmation:
        raise HTTPError(404, "Booking not found or session expired")

    cursor.execute(
        """
        SELECT Address, Bedrooms, Beds, Bathrooms, SquareMeters, ParkingSpots, Kitchens
        FROM PropertyListing
        WHERE PropertyListingID = %s
        """,
        (property_id,),
    )
    address, bedrooms, beds, bathrooms, squareMeters, parkingSpots, kitchens = (
        cursor.fetchone()
    )

    cursor.close()

    return booking_confirmation_template(
        bConfirmation,
        property_id,
        address,
        bedrooms,
        beds,
        bathrooms,
        squareMeters,
        parkingSpots,
        kitchens,
    )


def booking_confirmation_template(
    bConfirmation,
    property_id,
    address,
    bedrooms,
    beds,
    bathrooms,
    squareMeters,
    parkingSpots,
    kitchens,
):
    expiryTime = bConfirmation[3]
    return html(
        f"Booking confirmation for: {address}",
        with_navbar(f"""
            <main id="book-confirm">
                <h1>Confirm order</h1>
                <input type="hidden" id="expiry_time" name="expiry_time" value="{expiryTime}">
                <h1>Your booking summary for: {address}</h1>
                <ul>
                    <li>Bedrooms: {bedrooms}</li>
                    <li>Beds: {beds}</li>
                    <li>Bathrooms: {bathrooms}</li>
                    <li>Area: {squareMeters} m²</li>
                    <li>Parking spots allocated: {parkingSpots}</li>
                    <li>Kitchens: {kitchens}</li><br>
                    <li>Start: {bConfirmation[1]}</li>
                    <li>End: {bConfirmation[2]}</li>
                </ul>
                <form id="finalizeForm" action="/finalize-booking" method="post">
                    <input type="hidden" name="PropertyListingID" value="{property_id}">
                    <input type="hidden" name="from_date" value="{bConfirmation[1].isoformat()}">
                    <label class="checkbox" for="TOS">
                        <input type="checkbox" id="TOS" name="TOS" required>
                        I accept the <a href="https://www.boilerplate.co/terms-of-service" target="_blank">terms and conditions</a>
                    </label>
                </form>
                <form id="cancelBooking" action="/cancel-temp-booking" method="post">
                    <input type="hidden" name="PropertyListingID" value="{property_id}">
                    <input type="hidden" name="from_date" value="{bConfirmation[1].isoformat()}">
                </form>
                <div class="buttons">
                    <button class="button_cancel" form="cancelBooking" type="submit">Cancel booking</button>
                    <button class="button_confirm" form="finalizeForm" type="submit">Finalize booking</button>
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

    cursor.execute(
        """
        DELETE FROM BookingSession
        WHERE Token=_binary  %s AND PropertyListingID= %s
        """,
        (token, property_id),
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

    if not token or not tos:
        raise HTTPError(403, "User not authenticated or TOS validation missing")

    cursor.execute(
        """
        SELECT * FROM BookingSession
        WHERE Token=_binary %s AND PropertyListingID=%s
        AND ExpiryTime> NOW()
        """,
        (token, property_id),
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

    cursor.execute(
        """
        DELETE FROM BookingSession
        WHERE Token=_binary  %s AND PropertyListingID= %s
        """,
        (token, property_id),
    )

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

    response.set_cookie(
        "BookingData", ",".join([str(property_listing_id), str(start_time), email])
    )
    redirect(f"/payment")
