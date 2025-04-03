import mysql.connector
from bottle import route, response, request
from ..components import html, with_navbar
import json
import os
from .. import db
from datetime import datetime


def hent_alle_tags():
    conn = db.cnx()
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM Tag ORDER BY Name")
    tags = [rad[0] for rad in cursor.fetchall()]
    conn.close()
    return tags


def get_search_results(
    location, check_in, check_out, guests, type_="", tags=None, sort_by=""
):
    if tags is None:
        tags = []

    conn = db.cnx()
    cursor = conn.cursor()

    params = []

    condition = ""
    if location != "":
        location = f"%{location}%"
        params += [location]
        condition = """PropertyListing.Address LIKE %s"""

    if check_in and check_out:
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
        params += [check_in, check_out, check_in, check_out, check_in, check_out]

    elif check_in:
        if condition != "":
            condition += " AND "
        condition += """
        PropertyListing.PropertyListingID NOT IN (
            SELECT Booking.PropertyListingID
            FROM Booking
            WHERE %s BETWEEN Booking.StartTime AND Booking.EndTime
                OR Booking.StartTime > %s
        )
        """
        params += [check_in, check_in]

    elif check_out:
        if condition != "":
            condition += " AND "
        condition += """
        PropertyListing.PropertyListingID NOT IN (
            SELECT Booking.PropertyListingID
            FROM Booking
            WHERE %s BETWEEN Booking.StartTime AND Booking.EndTime
                OR Booking.EndTime < %s
        )
        """
        params += [check_out, check_out]

    if guests != 0:
        if condition != "":
            condition += " AND "
        condition += "PropertyListing.Beds >= %s"
        params += [guests]

    if type_:
        if condition:
            condition += " AND "
        condition += """
        PropertyListing.PropertyListingID IN (
            SELECT PropertyTag.PropertyListingID
            FROM PropertyTag
            JOIN Tag ON Tag.TagID = PropertyTag.TagID
            WHERE Tag.Name = %s
        )
        """
        params.append(type_)

    if tags is not None and len(tags) > 0:
        placeholders = ", ".join(["%s"] * len(tags))
        condition += f"""
        AND PropertyListing.PropertyListingID IN (
            SELECT PropertyTag.PropertyListingID
            FROM PropertyTag
            JOIN Tag ON Tag.TagID = PropertyTag.TagID
            WHERE Tag.Name IN ({placeholders})
            GROUP BY PropertyTag.PropertyListingID
            HAVING COUNT(*) = {len(tags)}
        )
        """
        for tag in tags:
            params.append(tag)

    query = f"""
        SELECT DISTINCT PropertyListing.PropertyListingID, PropertyListing.Address,
            PropertyListing.Description, PropertyListing.Beds, COALESCE(Picture.Filename, 'default.jpg') AS Filename
        FROM PropertyListing
        LEFT JOIN PropertyPicture ON PropertyListing.PropertyListingID = PropertyPicture.PropertyListingID
        LEFT JOIN Picture ON PropertyPicture.PictureID = Picture.PictureID
        """
    if condition:
        query += f" WHERE {condition}"

    if sort_by == "price_asc":
        query += " ORDER BY PropertyListing.Price ASC"
    elif sort_by == "price_desc":
        query += " ORDER BY PropertyListing.Price DESC"
    elif sort_by == "beds_desc":
        query += " ORDER BY PropertyListing.Beds DESC"

    print(query)
    cursor.execute(
        query,
        tuple(params),
    )
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    # Hack around the SQL query returning one row per picture per property listing
    properties_seen = []
    result_html = ""
    for property_id, address, description, beds, filename in results:
        if property_id in properties_seen:
            continue
        properties_seen += [property_id]

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
    sort_by = request.query.get("sort_by", "")
    check_in = request.query.get("checkin", "").strip()
    check_out = request.query.get("checkout", "").strip()
    guests = request.query.get("guests", "").strip()
    type_ = request.query.get("type", "").strip()
    tags = request.query.get("tag")

    try:
        guests = int(guests)
    except ValueError:
        guests = 0

    if check_in and check_out:
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
            if check_in_date >= check_out_date:
                return html(
                    "Search error",
                    with_navbar(
                        "<main><p>Ugyldig dato: Utsjekksdato må være etter innsjekksdato.</p></main>"
                    ),
                )
        except ValueError:
            return html(
                "Search error", with_navbar("<main><p>Ugyldig dataformat.</p></main>")
            )
    return get_search_results(
        location, check_in, check_out, guests, type_, tags, sort_by
    )


@route("/search")
def search_bar():
    result = search_results()

    location = request.query.get("location", "").strip()
    check_in = request.query.get("checkin", "").strip()
    check_out = request.query.get("checkout", "").strip()
    guests = request.query.get("guests", "").strip()
    tags = hent_alle_tags()
    type_tags = ["apartment", "cabin", "house", "basement"]
    types = [tag for tag in tags if tag in type_tags]
    features = [tag for tag in tags if tag not in type_tags]
    type_dropdown = '<div class="input-box"><label for="type">Property Type</label><select name="type" id="type" hx-get="/search_results" hx-target="#search-results" hx-trigger="change" hx-include="closest form">'
    type_dropdown += '<option value="">All</option>'

    for t in types:
        selected = "selected" if request.query.get("type") == t else ""
        type_dropdown += f'<option value="{t}" {selected}>{t.capitalize()}</option>'

    type_dropdown += "</select></div>"

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
                            <label for="guests">Guests</label>
                            <input id="guests" name="guests" type="number" placeholder="Type in guests" min="0" {guests != "" and f"value=\"{guests}\""}>
                        </div>
                        <button popovertarget="search-popover" type="button">Filter</button>
                        <div popover id="search-popover">
                            <h1>Filter</h1>
                            <button type="button" popovertarget="search-popover" popovertargetaction="hide" style="float: right;">❌ Close</button>
                            {type_dropdown}
                            <fieldset>
                                <legend>Features</legend>
                                {"".join([
                                    f'<label><input type="checkbox" name="tag" value="{tag}" {"checked" if tag in request.query.getall("tag") else ""} hx-get="/search_results" hx-target="#search-results" hx-trigger="change" hx-include="closest form"> {tag}</label><br>'
                                    for tag in features
                                ])}
                            </fieldset>
                            <div class="input-box">
                                <label for="sort_by">Sort by</label>
                                <select name="sort_by" id="sort_by">
                                    <option value="">--</option>
                                    <option value="price_asc" {{ "selected" if request.query.get("sort_by") == "price_asc" else "" }}>Price: Low to High</option>
                                    <option value="price_desc" {{ "selected" if request.query.get("sort_by") == "price_desc" else "" }}>Price: High to Low</option>
                                    <option value="beds_desc" {{ "selected" if request.query.get("sort_by") == "beds_desc" else "" }}>Beds: Most First</option>
                                </select>
                            </div>
                        </div>
                        <button
                            type="submit"
                            class="search-btn">🔍 Search</button>
                    </form>
                </div>
                <div class="spacer"></div>
                <div id="search-results">
                    {result}
                </div>
            </main>
       """),
    )
