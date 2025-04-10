import urllib.parse
import mysql.connector
from bottle import route, response, request
from ..components import html, with_navbar
import json
import os
from .. import db, icons
from datetime import datetime


def hent_alle_tags():
    conn = db.cnx()
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM Tag ORDER BY Name")
    tags = [rad[0] for rad in cursor.fetchall()]
    cursor.close()
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
    def add_condition(new_condition, new_params):
        nonlocal condition
        nonlocal params
        if condition != "":
            condition += " AND "
        condition += new_condition
        params += new_params

    if location != "":
        add_condition("PropertyListing.Address LIKE %s", [f"%{location}%"])

    if check_in and check_out:
        add_condition(
            """
            PropertyListing.PropertyListingID NOT IN (
                SELECT Booking.PropertyListingID
                FROM Booking
                WHERE (
                    (Booking.StartTime <= %s AND %s <= Booking.EndTime)
                    OR (%s < Booking.StartTime AND Booking.StartTime < %s)
                    OR (%s < Booking.EndTime AND Booking.EndTime < %s)
                )
            )
            """,
            [check_in, check_out, check_in, check_out, check_in, check_out],
        )
    elif check_in:
        add_condition(
            """
            PropertyListing.PropertyListingID NOT IN (
                SELECT Booking.PropertyListingID
                FROM Booking
                WHERE %s BETWEEN Booking.StartTime AND Booking.EndTime
                    OR Booking.StartTime > %s
            )
            """,
            [check_in, check_in],
        )
    elif check_out:
        add_condition(
            """
            PropertyListing.PropertyListingID NOT IN (
                SELECT Booking.PropertyListingID
                FROM Booking
                WHERE %s BETWEEN Booking.StartTime AND Booking.EndTime
                    OR Booking.EndTime < %s
            )
            """,
            [check_out, check_out],
        )

    if guests != 0:
        add_condition("PropertyListing.Beds >= %s", [guests])

    if type_:
        add_condition(
            """
            PropertyListing.PropertyListingID IN (
                SELECT PropertyTag.PropertyListingID
                FROM PropertyTag
                JOIN Tag ON Tag.TagID = PropertyTag.TagID
                WHERE Tag.Name = %s
            )
            """,
            [type_],
        )

    if tags is not None and len(tags) > 0:
        placeholders = ", ".join(["%s"] * len(tags))
        add_condition(
            f"""
            PropertyListing.PropertyListingID IN (
                SELECT PropertyTag.PropertyListingID
                FROM PropertyTag
                JOIN Tag ON Tag.TagID = PropertyTag.TagID
                WHERE Tag.Name IN ({placeholders})
                GROUP BY PropertyTag.PropertyListingID
                HAVING COUNT(*) = {len(tags)}
            )
            """,
            tags,
        )

    query = f"""
    SELECT PropertyListing.PropertyListingID,
        PropertyListing.Address,
        PropertyListing.Description,
        PropertyListing.Price,
        PropertyListing.Beds,
        COALESCE(MIN(Picture.Filename), 'default.jpg') AS Filename
    FROM PropertyListing
    LEFT JOIN PropertyPicture ON PropertyListing.PropertyListingID = PropertyPicture.PropertyListingID
    LEFT JOIN Picture ON PropertyPicture.PictureID = Picture.PictureID
    """
    if condition:
        query += f" WHERE {condition}"

    query += " GROUP BY PropertyListing.PropertyListingID"

    if sort_by == "price_asc":
        query += " ORDER BY PropertyListing.Price ASC"
    elif sort_by == "price_desc":
        query += " ORDER BY PropertyListing.Price DESC"
    elif sort_by == "beds_asc":
        query += " ORDER BY PropertyListing.Beds ASC"
    elif sort_by == "beds_desc":
        query += " ORDER BY PropertyListing.Beds DESC"

    print(query)
    cursor.execute(
        query,
        tuple(params),
    )
    results = cursor.fetchall()

    cursor.close()

    # Hack around the SQL query returning one row per picture per property listing
    properties_seen = []
    result_html = ""
    for property_id, address, description, price, beds, filename in results:
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
                    <p class="price">{price} kr / Night</p>
                </div>
            </a>
        """

    return (
        result_html
        if result_html
        else '<p class="no-results">Ingen resultater funnet.</p>'
    )


def title(location=None):
    title = "Search"
    if location != None and location != "":
        title += f' "{location}"'
    return title


@route("/search_results")
def search_results():
    location = request.query.get("location", "").strip()
    sort_by = request.query.get("sort_by", "")
    check_in = request.query.get("checkin", "").strip()
    check_out = request.query.get("checkout", "").strip()
    guests = request.query.get("guests", "").strip()
    type_ = request.query.get("type", "").strip()
    tags = request.query.getall("tag")

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
    result_html = get_search_results(
        location, check_in, check_out, guests, type_, tags, sort_by
    )

    url = urllib.parse.urlparse(request.url)
    url = url._replace(path="/").geturl()
    response.add_header("HX-Replace-Url", url)

    return f"""
            <div id="search-results">
                <title>{title(location)}</title>
                {result_html}
            </div>
            """


@route("/search")
def search_bar():
    location = request.query.get("location", "").strip()
    check_in = request.query.get("checkin", "").strip()
    check_out = request.query.get("checkout", "").strip()
    guests = request.query.get("guests", "").strip()
    sort_by = request.query.get("sort_by", "")

    sort_icon = icons.sort_asc() if sort_by.endswith("asc") else icons.sort_desc()

    result = get_search_results(
        location,
        check_in,
        check_out,
        guests,
        request.query.get("type", ""),
        request.query.getall("tag"),
        sort_by,
    )

    tags = hent_alle_tags()
    type_tags = ["apartment", "cabin", "house", "basement"]
    types = [tag for tag in tags if tag in type_tags]
    features = [tag for tag in tags if tag not in type_tags]

    type_filter = f'''
    <fieldset class="type-group">
        <legend>Property Type</legend>
        {"".join([
            f'''
            <label class="radio-option">
                <input type="radio" name="type" value="{t}"
                    {"checked" if request.query.get("type") == t else ""}
                    hx-get="/search_results"
                    hx-target="#search-results"
                    hx-trigger="change"
                    hx-include="#search-form">
                {t.capitalize()}
            </label>
            ''' for t in types
        ])}
    </fieldset>
    '''

    tag_filter = f'''
    <fieldset class="feature-group">
        <legend>Features</legend>
        {"".join([
            f'''
            <label class="checkbox-option">
                <input type="checkbox" name="tag" value="{tag}"
                    {"checked" if tag in request.query.getall("tag") else ""}
                    hx-get="/search_results"
                    hx-target="#search-results"
                    hx-trigger="change"
                    hx-include="#search-form,#sort_by">
                {tag}
            </label>
            ''' for tag in features
        ])}
    </fieldset>
    '''

    return html(
        title(location),
        with_navbar(f"""
            <main id="search-page">
                <div id="search-bar-container">
                    <div id="search-bar">
                        <form class="search-container" id="search-form">
                            <div class="input-box">
                                <label>Where</label>
                                <input id="location-input" name="location" type="text" placeholder="search destination"
                                    value="{location}"
                                    hx-get="/search_results"
                                    hx-target="#search-results"
                                    hx-trigger="input changed"
                                    hx-include="#search-form">
                            </div>
                            <div class="input-box">
                                <label>Check in</label>
                                <input id="checkin-input" name="checkin" type="date"
                                    value="{check_in}"
                                    hx-get="/search_results"
                                    hx-target="#search-results"
                                    hx-trigger="change"
                                    hx-include="#search-form">
                            </div>
                            <div class="input-box">
                                <label>Check out</label>
                                <input id="checkout-input" name="checkout" type="date"
                                    value="{check_out}"
                                    hx-get="/search_results"
                                    hx-target="#search-results"
                                    hx-trigger="change"
                                    hx-include="#search-form">
                            </div>
                            <div id="who-box" class="input-box">
                                <label for="guests">Guests</label>
                                <input id="guests" name="guests" type="number" placeholder="Type in guests" min="0"
                                    value="{guests}"
                                    hx-get="/search_results"
                                    hx-target="#search-results"
                                    hx-trigger="input changed"
                                    hx-include="#search-form">
                            </div>
                            <button popovertarget="sort-popover" type="button" class="icon-button" aria-label="Sort">
                                {sort_icon}
                            </button>

                            <button popovertarget="filter-popover" type="button" class="icon-button" aria-label="Filter">
                                {icons.filter()}
                            </button>

                            <button type="submit" class="search-btn">🔍 Search</button>
                        </form>
                    </div>
                    <div id="popover-container">
                        <div popover id="sort-popover" class="filter-box">
                            <fieldset class="sort-by-group">
                                <legend>Sort by</legend>
                                <label class="radio-option"><input type="radio" name="sort_by" value="" {"checked" if sort_by == "" else ""} hx-get="/search_results" hx-target="#search-results" hx-trigger="change" hx-include="#search-form"> Default</label>
                                <label class="radio-option"><input type="radio" name="sort_by" value="price_asc" {"checked" if sort_by == "price_asc" else ""} hx-get="/search_results" hx-target="#search-results" hx-trigger="change" hx-include="#search-form"> Price: Low to High</label>
                                <label class="radio-option"><input type="radio" name="sort_by" value="price_desc" {"checked" if sort_by == "price_desc" else ""} hx-get="/search_results" hx-target="#search-results" hx-trigger="change" hx-include="#search-form"> Price: High to Low</label>
                                <label class="radio-option"><input type="radio" name="sort_by" value="beds_asc" {"checked" if sort_by == "beds_asc" else ""} hx-get="/search_results" hx-target="#search-results" hx-trigger="change" hx-include="#search-form"> Beds: Fewest First</label>
                                <label class="radio-option"><input type="radio" name="sort_by" value="beds_desc" {"checked" if sort_by == "beds_desc" else ""} hx-get="/search_results" hx-target="#search-results" hx-trigger="change" hx-include="#search-form"> Beds: Most First</label>
                            </fieldset>
                        </div>
                        <div popover id="filter-popover" class="filter-box">
                            {type_filter}
                            {tag_filter}
                        </div>
                    </div>
                </div>
                <div id="search-results">
                    {result}
                </div>
            </main>
        """),
    )


@route("/sort_icon")
def sort_icon_route():
    sort_by = request.query.get("sort_by", "")
    if sort_by.endswith("asc"):
        return f'<span id="sort-icon">{icons.sort_asc()}</span>'
    else:
        return f'<span id="sort-icon">{icons.sort_desc()}</span>'
