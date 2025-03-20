import mysql.connector
from bottle import route, response, request
from ..components import html, with_navbar
import json
import os
from .. import db


def get_search_results(location, check_in, check_out, guests):
    conn = db.db_cnx()
    cursor = conn.cursor()

    params = []

    condition = ""
    if location != "":
        location = f"%{location}%"
        params += [location]
        condition = """PropertyListing.Address LIKE %s"""

    if check_in != "" and check_out != "":
        if condition != "":
            time_check += " AND "
        time_check += """
        PropertyListing.PropertyListingID NOT IN (
            SELECT Booking.PropertyListingID
            FROM Booking
            WHERE (
                (Booking.StartTime <= %s AND %s <= Booking.EndTime)
                OR (%s < Booking.StartTime AND Booking.StartTime < %s)
                OR (%s < Booking.EndTime AND Booking.EndTime < %s)
            )
        )
        """
        params += [
            check_in,
            check_out,
            check_in,
            check_out,
            check_in,
            check_out,
        ]

    if guests != "":
        if condition != "":
            condition += " AND "
        condition += "PropertyListing.Beds >= %s"
        params += [guests]

    query = f"""
        SELECT DISTINCT PropertyListing.PropertyListingID, PropertyListing.Address, 
            PropertyListing.Description, PropertyListing.Beds, COALESCE(Picture.Filename, 'default.jpg') AS Filename
        FROM PropertyListing
        LEFT JOIN PropertyPicture ON PropertyListing.PropertyListingID = PropertyPicture.PropertyListingID
        LEFT JOIN Picture ON PropertyPicture.PictureID = Picture.PictureID
        WHERE {condition}
        """
    print(query)
    cursor.execute(
        query,
        tuple(params),
    )
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    result_html = ""
    for property_id, adress, description, beds, filename in results:
        image_path = (
            f"/static/uploads/{filename}" if filename else "/static/default.jpg"
        )

        result_html += f"""
            <div class="property-card">
                <img src="{image_path}" alt="Bilde av {adress}">
                <h3>{adress}</h3>
                <p>{description}</p>
                <p>{beds} senger</p>
            </div>
        """

    return result_html if result_html else "<p>Ingen resultater funnet.</p>"


@route("/search_results")
def search_results():
    location = request.query.get("location", "").strip()
    check_in = request.query.get("checkin", "").strip()
    check_out = request.query.get("checkout", "").strip()
    guests = request.query.get("guests", "").strip() or 1

    return get_search_results(location, check_in, check_out, guests)


def get_data(query):
    conn = db.db_cnx()
    cursor = conn.cursor()
    cursor.execute(query)
    data = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return data


def get_location():
    response.content_type = "text/html"
    locations = get_data("SELECT DISTINCT Address FROM PropertyListing")
    location_list_html = "\n".join(
        '<li onclick=\'selectOption(this, "location-input", "{}")\'>'.format(loc)
        + str(loc)
        + "</li>"
        for loc in locations
    )

    return f"""
    <ul>
        {location_list_html}
    </ul>
    """


def get_dates(select_id):
    response.content_type = "text/html"
    check_in_dates = get_data("SELECT DISTINCT StartTime FROM Booking")
    check_out_dates = get_data("SELECT DISTINCT EndTime FROM Booking")

    checkin_list_html = "".join(
        f'<li onclick=\'selectOption(this, "{select_id}", "{{}}")\'>'.format(date)
        + str(date)
        + "</li>"
        for date in check_in_dates
    )

    checkout_list_html = "".join(
        f'<li onclick=\'selectOption(this, "{select_id}", "{{}}")\'>'.format(date)
        + str(date)
        + "</li>"
        for date in check_out_dates
    )

    return "<ul>" + checkin_list_html + checkout_list_html + "</ul>"


def get_guests():
    response.content_type = "text/html"

    return """
    <div>
        Adults (13+ years):
        <button type="button" id="decrease-adults">-</button>
        <span id="adult-count" value="0">0</span>
        <button type="button" id="increase-adults">+</button>
    </div>
    <div>
        Children (0-12 years):
        <button type="button" id="decrease-children">-</button>
        <span id="children-count" value="0">0</span>
        <button type="button" id="increase-children">+</button>
    </div>
    """


@route("/search")
def search_bar():
    result = search_results()

    return html(
        "Search",
        with_navbar(f"""
            <main id="search-page">
                <div class="spacer"></div>
                <div id="search-bar">
                    <form class="search-container">
                        <div hx-get="/get_locations" hx-target="find div.dropdown" hx-swap="innerHTML" class="input-box" onclick="toggleDropdown('location-box')">
                            <label>Where</label>
                            <input id="location-input" name="location" type="text" placeholder="search destination" readonly>
                            <div id="location-box" class="dropdown"></div>
                        </div>
                        <div hx-get="/get_dates/checkin-input" hx-trigger="click" hx-target="#checkin-box" hx-swap="innerHTML"
                            class="input-box" onclick="toggleDropdown('checkin-box')">
                            <label>Check in</label>
                            <input id="checkin-input" name="checkin" type="text" placeholder="Add dates" readonly>
                            <div id="checkin-box" class="dropdown"></div>
                        </div>
                        <div hx-get="/get_dates/checkout-input" hx-trigger="click" hx-target="#checkout-box" hx-swap="innerHTML"
                            class="input-box" onclick="toggleDropdown('checkout-box')">
                            <label>Check out</label>
                            <input id="checkout-input" name="checkout" type="text" placeholder="Add dates" readonly>
                            <div id="checkout-box" class="dropdown"></div>
                        </div>
                        <div
                            hx-get="/get_guests"
                            hx-trigger="click"
                            hx-target="#guests-box"
                            hx-swap="innerHTML"
                            hx-on::after-swap="setGuestEventListeners()"
                            class="input-box" onclick="toggleDropdown('guests-box')">
                            <label>Who</label>
                            <input type="text" placeholder="Add guest" readonly>
                            <div id="guests-box" class="dropdown" hx-trigger="click consume"></div>
                        </div>
                        <button
                            type="submit"
                            class="search-btn">🔍 Søk</button>
                    </form>
                </div>
                <div class="spacer"></div>
                <div id="search-results">
                    {result}
                </div>
            </main>
       """),
    )


@route("/get_locations")
def locations():
    return get_location()


@route("/get_dates/<select_id>")
def dates(select_id):
    return get_dates(select_id)


@route("/get_guests")
def guests():
    return get_guests()
