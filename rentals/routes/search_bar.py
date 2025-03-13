import mysql.connector
from bottle import route, response, request
from ..components import html, with_navbar

from .. import db


def get_search_results(location, check_in, check_out, guests):
    conn = db.db_cnx()
    cursor = conn.cursor()

    query = """
        SELECT * FROM PropertyListing
        WHERE Adress = %s AND check_in <= %s AND check_out >= AND guests >= %s
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
        f'<li onclick=\'selectOption("location-input", "{loc}")\'>{loc}</li>'
        for loc in locations
    )

    return f"""
    <ul>
        {location_list_html}
    </ul>
    """


def get_dates():
    response.content_type = "application/json"
    return {
        "check_in": get_data("SELECT DISTINCT check_in FROM Booking"),
        "check_out": get_data("SELECT DISTINCT check:out FROM Booking"),
    }


def get_guests():
    response.content_type = "application/json"
    return {"guests": get_data("SELECT DISTINCT guests FROM Booking")}


@route("/searchbar")
def search_bar():
    return html(
        "Searchbar",
        with_navbar("""
            <main id="search-bar">
                <div class="search-container">
                    <div hx-get="/get_locations" hx-target="find div.dropdown" class="input-box" onclick="toggleDropdown('location-box')">
                        <label>Where</label>
                        <input type="text" placeholder="search destination" readonly>
                        <div id="location-box" class="dropdown">
                            <ul>
                                <li>Hønefoss</li>
                                <li>Trondheim</li>
                                <li>Bergen</li>
                                <li>Hamar</li>
                                <li>Oslo</li>
                            </ul>
                        </div>
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
                            <p>Children (2-12 years): <button>-</button> 0 <button>+</button></p>
                            <p>Infant (Under 2 years): <button>-</button> 0 <button>+</button></p>
                            <p>Pet: <button>-</button> 0 <button>+</button></p>
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
