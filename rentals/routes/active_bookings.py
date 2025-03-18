from bottle import route, run, template, request, HTTPError, redirect
from datetime import datetime, timedelta
import urllib.parse
from urllib.parse import unquote

from ..auth import requires_user_session, get_session_token
from ..components import html, with_navbar
from .. import db


@route("/bookings/active")
@requires_user_session(referer=True)
def view_active_bookings():
    token = get_session_token()

    cnx = db.db_cnx()
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
        SELECT Booking.StartTime, Booking.EndTime, Booking.Email,
                PropertyListing.Address, PropertyListing.Bedrooms, PropertyListing.Bathrooms, PropertyListing.ParkingSpots
        FROM Booking, PropertyListing
        WHERE Booking.PropertyListingID = PropertyListing.PropertyListingID
            AND Booking.Email = %s
            AND Booking.StartTime >= NOW()
        ORDER BY Booking.StartTime
        """,
        (email,),
    )
    activeBookings = cursor.fetchall()

    return active_booking_template(activeBookings, email)


def active_booking_template(activeBookings, email):
    booking_html = ""
    if not activeBookings:
        booking_html = """<h2>You have no active bookings.</h2>"""
    else:
        for booking in activeBookings:
            (
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
                </ul>
            </div><br>
            """

    full_page = with_navbar(f"""
        <main id="active-booking">
            <h2>Active Bookings for: {email}</h2>
            {booking_html}
        </main>
    """)

    return html(f"Active Bookings for: {email}", full_page)
