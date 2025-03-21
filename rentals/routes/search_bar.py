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

    # TODO: Handle the case where only one of check_in and check_out are specified.
    if check_in != "" and check_out != "":
        if condition != "":
            condition += " AND "
        condition += """
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

    if guests != 0:
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
        """
    if condition:
        query += f" WHERE {condition}"

    print(query)
    cursor.execute(
        query,
        tuple(params),
    )
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    result_html = ""
    for property_id, address, description, beds, filename in results:
        image_path = (
            f"/static/uploads/{filename}" if filename else "/static/default.jpg"
        )

        result_html += f"""
            <a href="/view-rental/{property_id}" class="property-link">
                <div class="property-card">
                    <img src="{image_path}" alt="Bilde av {address}">
                    <h3>{address}</h3>
                    <p>{description}</p>
                    <p class="beds">{beds} Beds</p>
                </div>
            </a>
        """

    return result_html if result_html else "<p>Ingen resultater funnet.</p>"


@route("/search_results")
def search_results():
    location = request.query.get("location", "").strip()
    check_in = request.query.get("checkin", "").strip()
    check_out = request.query.get("checkout", "").strip()
    children = request.query.get("children", "").strip()
    adults = request.query.get("adults", "").strip()

    guests = 0
    try:
        guests += int(children)
    except ValueError:
        pass

    try:
        guests += int(adults)
    except ValueError:
        pass

    print(children)
    return get_search_results(location, check_in, check_out, guests)


@route("/search")
def search_bar():
    result = search_results()

    location = request.query.get("location", "").strip()
    check_in = request.query.get("checkin", "").strip()
    check_out = request.query.get("checkout", "").strip()
    children = request.query.get("children", "").strip()
    adults = request.query.get("adults", "").strip()

    return html(
        "Search",
        with_navbar(f"""
            <main id="search-page">
                <div class="spacer"></div>
                <div id="search-bar">
                    <form class="search-container">
                        <div class="input-box">
                            <label>Where</label>
                            <input id="location-input" name="location" type="text" placeholder="search destination" {location != "" and f"value=\"{location}\""}>
                        </div>
                        <div class="input-box">
                            <label>Check in</label>
                            <input id="checkin-input" name="checkin" type="date" placeholder="Add dates" {check_in != "" and f"value=\"{check_in}\""}>
                        </div>
                        <div class="input-box">
                            <label>Check out</label>
                            <input id="checkout-input" name="checkout" type="date" placeholder="Add dates" {check_out != "" and f"value=\"{check_out}\""}>
                        </div>
                        <div id="who-box" class="input-box">
                            <label>Who</label>
                            <label for="children">Children:</label>
                            <input id="children" name="children" type="number" min="0" {children != "" and f"value=\"{children}\""}>
                            <label for="children">Adults:</label>
                            <input id="adults" name="adults" type="number" min="0" {adults != "" and f"value=\"{adults}\""}>
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
