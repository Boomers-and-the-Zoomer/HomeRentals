from bottle import route, run, template, request, HTTPError, redirect
from datetime import datetime, timedelta
import urllib.parse
from urllib.parse import unquote

from ..auth import requires_user_session, get_session_token
from ..components import html, with_navbar
from .. import db


@route("/bookings/active")
@requires_user_session()
def view_active_bookings():
    token = get_session_token()

    cnx = db.cnx()
    cursor = cnx.cursor()

    cursor.execute(
        """
        SELECT Email FROM Session
        WHERE Token=_binary %s
        """,
        (token,),
    )
    userResult = cursor.fetchone()
    if not userResult:
        raise HTTPError(403, "User not found")
    email = userResult[0]

    cursor.execute(
        """
        SELECT Booking.PropertyListingID, Booking.StartTime, Booking.EndTime, Booking.Email, PropertyListing.Address,
                PropertyListing.Bedrooms, PropertyListing.Bathrooms, PropertyListing.ParkingSpots
        FROM Booking, PropertyListing
        WHERE Booking.PropertyListingID = PropertyListing.PropertyListingID
            AND Booking.Email = %s
            AND Booking.EndTime >= NOW()
        ORDER BY Booking.StartTime
        """,
        (email,),
    )
    activeBookings = cursor.fetchall()

    cursor.close()

    return active_booking_template(activeBookings, email)


def active_booking_template(activeBookings, email):
    booking_html = ""
    if not activeBookings:
        booking_html = """<h2>You have no active bookings.</h2>"""
    else:
        for booking in activeBookings:
            (
                property_listing_id,
                start_time,
                end_time,
                email,
                address,
                bedrooms,
                bathrooms,
                parking,
            ) = booking

            booking_html += f"""
            <div class="booking">
                <h3>{address.strip()}</h3>
                <ul>
                    <li>Start Time: {start_time}</li>
                    <li>End Time: {end_time}</li>
                    <li>Bedrooms: {bedrooms}</li>
                    <li>Bathrooms: {bathrooms}</li>
                    <li>Parking spots: {parking}</li>
                <form id="CancelBookingPermanent" action="/cancel-booking" method="post">
                    <input type="hidden" name="PropertyListingID" value="{property_listing_id}">
                    <input type="hidden" name="StartTime" value="{start_time}">
                    <input type="hidden" name="Email" value="{email}">
                    <button class="button_cancel" type="submit" onclick="return confirmCancellation()">Cancel Booking</button>
                </form>
                </ul>
            </div><br>
            """

    full_page = with_navbar(f"""
        <main id="bookings-pages">
            <h2>Active Bookings for: {email}</h2>
            {booking_html}
        </main>
    """)

    return html(f"Active Bookings for: {email}", full_page)


@route("/cancel-booking", method="POST")
@requires_user_session(referer=True)
def cancel_temp_booking():
    cnx = db.cnx()
    cursor = cnx.cursor()

    property_listing_id = request.forms.get("PropertyListingID")
    start_time = request.forms.get("StartTime")
    email = request.forms.get("Email")

    cursor.execute(
        """
        DELETE FROM Booking
        WHERE PropertyListingID= %s AND StartTime= %s AND Email= %s
        """,
        (property_listing_id, start_time, email),
    )

    cnx.commit()
    cursor.close()

    redirect(f"/bookings/active")
