from bottle import route, run, template, request, HTTPError, redirect
from datetime import datetime, timedelta
import urllib.parse
from urllib.parse import unquote

from ..auth import requires_user_session, get_session_token
from ..components import html, with_navbar
from .. import db


@route("/bookings/historical")
@requires_user_session()
def view_historical_bookings():
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
            AND Booking.EndTime <= NOW()
        ORDER BY Booking.StartTime
        """,
        (email,),
    )
    historicalBookings = cursor.fetchall()

    cursor.close()

    return historical_booking_template(historicalBookings, email)


def historical_booking_template(historicalBookings, email):
    booking_html = ""
    if not historicalBookings:
        booking_html = """<h2>You have no rental records with HomeRentals.</h2>"""
    else:
        for booking in historicalBookings:
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
                <form id="LeaveReview" action="/leave-review" method="post">
                    <input type="hidden" name="PropertyListingID" value="{property_listing_id}">
                    <input type="hidden" name="StartTime" value="{start_time}">
                    <input type="hidden" name="Email" value="{email}">
                    <button type="submit">Leave Review</button>
                </form>
                </ul>
            </div><br>
            """

    full_page = with_navbar(f"""
        <main id="historical-booking">
            <h2>Previous Rentals for: {email}</h2>
            {booking_html}
        </main>
    """)

    return html(f"Previous Rentals for: {email}", full_page)


@route("/leave-review", method="POST")
def view_rental_reviews():
    raise HTTPError(403, "Reviews page under construction")
