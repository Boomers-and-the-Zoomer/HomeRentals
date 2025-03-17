import mysql.connector
from bottle import route, response, request
from ..components import html, with_navbar
import json
from .. import db


def get_search_results(location, check_in, check_out, guests):
    conn = db.db_cnx()
    cursor = conn.cursor()

    query = """
        SELECT * FROM PropertyListing
        WHERE Address = %s AND check_in <= %s AND check_out >= %s AND guests >= %s
    """
    cursor.execute(query, (location, check_in, check_out, guests))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    result_html = "".join(
        f"<p>{row[1]} - {row[2]} NOK per natt - {row[3]} gjester</p>" for row in results
    )

    return result_html if result_html else "<p>Ingen resultater funnet.</p>"


@route("/search_results")
def search_results():
    location = request.query.get("location", "").strip()
    check_in = request.query.get("check_in", "").strip()
    check_out = request.query.get("check_out", "").strip()
    guests = request.query.get("guests", "").strip()

    if not location or not check_in or not check_out or not guests:
        return "<p>Vennligst fyll ut alle feltene.</p>"

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
    location_list_html = "".join(
        f'<li onclick=\'selectOption(this, "location-input", "{loc}")\'>{loc}</li>'
        for loc in locations
    )

    return f"""
    <ul>
        {location_list_html}
    </ul>
    """


def get_dates():
    response.content_type = "application/json"
    dates = {
        "check_in": [
            str(date) for date in get_data("SELECT DISTINCT StartTime FROM Booking")
        ],
        "check_out": [
            str(date) for date in get_data("SELECT DISTINCT EndTime FROM Booking")
        ],
    }
    return json.dumps(dates)


def get_guests():
    response.content_type = "application/json"
    guests = get_data("SELECT DISTINCT Beds FROM PropertyListing")
    return json.dumps({"guests": guests})


@route("/searchbar")
def search_bar():
    return html(
        "Searchbar",
        with_navbar("""
            <main id="search-bar">
                <div class="search-container">
                    <div hx-get="/get_locations" hx-target="find div.dropdown" hx-swap="innerHTML" class="input-box" onclick="toggleDropdown('location-box')">
                        <label>Where</label>
                        <input id="location-input" type="text" placeholder="search destination" readonly>
                        <div id="location-box" class="dropdown"></div>
                    </div>
                    <div class="input-box" onclick="toggleDropdown('checkin-box')">
                        <label>Check in</label>
                        <input type="text" placeholder="Add dates" readonly>
                        <div id="checkin-box" class="dropdown">
                            <input type="date">
                        </div>
                    </div>
                    <div class="input-box" onclick="toggleDropdown('checkout-box')">
                        <label>Check out</label>
                        <input type="text" placeholder="Add dates" readonly>
                        <div id="checkout-box" class="dropdown">
                            <input type="date">
                        </div>
                    </div>
                    <div class="input-box" onclick="toggleDropdown('guests-box')">
                        <label>Who</label>
                        <input type="text" placeholder="Add guest" readonly>
                        <div id="guests-box" class="dropdown">
                            <p>Adults (13+ years): <button>-</button> 0 <button>+</button></p>
                            <p>Children (0-12 years): <button>-</button> 0 <button>+</button></p>
                        </div>
                    </div>
                    <button class="search-btn">🔍 Søk</button>
                </div>
            </main>

       """),
    )


@route("/get_locations")
def locations():
    return get_location()


@route("/get_dates")
def dates():
    return get_dates()


@route("/get_guests")
def guests():
    return get_guests()
