from bottle import route, response, post, get, request

from ..auth import requires_user_session, get_session_token
from .. import db
from ..components import html, with_navbar, image_input, image_input_carrier


@route("/new-listing")
@requires_user_session()
def new_listing():
    response.status = 307
    response.add_header("Location", "/new-listing/summary")


def page_frame(content: str, n: int = None, prev: str = None, next: str = None) -> str:
    if prev == None and n > 1:
        prev = f"page{n - 1}"

    back_button = ""
    if prev != None:
        back_button = f"""
            <div class="back-button">
                <button
                    hx-get="{prev}/content"
                    hx-push-url="{prev}"
                    hx-target="#register_new_listing"
                ><u><b>Back</b></u></button>
            </div>
        """

    if n != None and next == None:
        next = f"page{n + 1}"

    next_button = ""
    if next != None:
        next_button = f"""
            <button
                hx-get="{next}/content"
                hx-push-url="{next}"
                hx-target="#register_new_listing"
                class="button"
            >Continue</button>
        """

    id = ""
    if n != None:
        id = f"page{n}"

    counter = ""
    carriers = ""
    if n != None:
        counter = f"""<p class="page-counter"><b>{n}/6</b></p>"""
        carriers = f"""
        <!-- These hidden inputs preserve the user's data across pages -->
        <div style="display: none">
            {n != 2 and image_input_carrier() or ""}
            {n != 3 and """<input id="bedrooms" hx-preserve type="number" name="bedrooms" class="line-input" required>
                           <input id="kitchens" hx-preserve type="number" name="kitchens" class="line-input" required>
                           <input id="beds" hx-preserve type="number" name="beds" class="line-input" required>
                           <input id="parkingspots" hx-preserve type="number" name="parkingspots" class="line-input" required>
                           <input id="bathrooms" hx-preserve type="number" name="bathrooms" class="line-input" required>
                           <input id="squaremeters" hx-preserve type="number" name="squaremeters" class="line-input" required>""" or ""}
            {n != 4 and '<textarea id="description" hx-preserve name="description" placeholder="Enter your description here"></textarea>' or ""}
            {n != 5 and '<input id="address" hx-preserve type="text" name="address" class="line-input" required>' or ""}
            {n != 5 and '<input id="postalcode" hx-preserve type="text" name="postalcode" class="line-input" required>' or ""}
            {n != 6 and '<input type="text" hx-preserve id="price" name="price" required>' or ""}
        </div>
        """

    return f"""
    <main id="register_new_listing">
        <div id="{id}">
            {content}
            {counter}
            {back_button}
            {next_button}
        </div>
        {carriers}
    </main>
    """


@route("/new-listing/page1")
@requires_user_session()
def new_listing_page1():
    return html(
        "Register New Listing Page 1",
        with_navbar(new_listing_page1_content_framed()),
    )


@route("/new-listing/page1/content")
def new_listing_page1_content_framed():
    return page_frame(
        """
        <div class="maintext">
            <h1>
                We are so happy that you've decided to<br>
                rent out your home!
            </h1>
            <br>
            <br>
            <br>
            <br>
            <p>Follow these steps, this is <i><u>easy!</i></u></p>
        </div>
        """,
        1,
    )


@route("/new-listing/page2")
@requires_user_session()
def new_listing_page2():
    return html(
        "Register New Listing Page 2",
        with_navbar(new_listing_page2_content_framed()),
    )


@route("/new-listing/page2/content")
@requires_user_session()
def new_listing_page2_content_framed():
    return page_frame(new_listing_page2_content(), 2)


def new_listing_page2_content():
    return f"""
    <div></div>
    <div class="maintext">
        <h1>Show us what your beautiful<br> home looks like!</h1>
        <br><br>
    </div>
    <div class="image-upload-container">
        {image_input()}
    </div>
    """


@route("/new-listing/page3")
@requires_user_session()
def new_listing_page3():
    return html(
        "Register New Listing Page 3",
        with_navbar(new_listing_page3_content_framed()),
    )


@route("/new-listing/page3/content")
@requires_user_session()
def new_listing_page3_content_framed():
    return page_frame(new_listing_page3_content(), 3)


def new_listing_page3_content():
    return f"""
    <div class="maintext">
        <h1>Lets count up the essentials -<br>rooms, beds and space!</h1>
    </div>
    <table>
        <tr>
            <td>
                <div class="form-row">
                    <label class="form-label" for="bedrooms">Bedrooms:</label>
                    <input id="bedrooms" hx-preserve type="number" name="bedrooms" class="line-input" required>
                </div>
            </td>
            <td>
                <div class="form-row">
                    <label class="form-label" for="kitchens">Kitchens:</label>
                    <input id="kitchens" hx-preserve type="number" name="kitchens" class="line-input" required>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <div class="form-row">
                    <label class="form-label" for="beds">Beds:</label>
                    <input id="beds" hx-preserve type="number" name="beds" class="line-input" required>
                </div>
            </td>
            <td>
                <div class="form-row">
                    <label class="form-label" for="parkingspots">Parking spots:</label>
                    <input id="parkingspots" hx-preserve type="number" name="parkingspots" class="line-input" required>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <div class="form-row">
                    <label class="form-label" for="bathrooms">Bathrooms:</label>
                    <input id="bathrooms" hx-preserve type="number" name="bathrooms" class="line-input" required>
                </div>
            </td>
            <td>
                <div class="form-row">
                    <label class="form-label" for="squaremeters">Square meters (m&sup2;):</label>
                    <input id="squaremeters" hx-preserve type="number" name="squaremeters" class="line-input" required>
                </div>
            </td>
        </tr>
    </table>
    """


@route("/new-listing/page4")
@requires_user_session()
def new_listing_page4():
    return html(
        "Register New Listing Page 4",
        with_navbar(new_listing_page4_content_framed()),
    )


@route("/new-listing/page4/content")
@requires_user_session()
def new_listing_page4_content_framed():
    return page_frame(
        f"""
        {new_listing_page4_content()}
        <div style="display: none">
            {image_input_carrier()}
        </div>
        """,
        4,
    )


def new_listing_page4_content():
    return """
        <div class="maintext">
            <h1>Enter a description of your home!</h1>
            <br><br>
            <p>Is it a peaceful retreat, a great place to gather with friends<br> or is it something truly unique?</p>
        </div>
        <div class="textarea">
            <textarea id="description" hx-preserve name="description" placeholder="Enter your description here"></textarea>
        </div>
    """


@route("/new-listing/page5")
@requires_user_session()
def new_listing_page5():
    return html(
        "Register New Listing Page 5", with_navbar(new_listing_page5_content_framed())
    )


@route("/new-listing/page5/content")
@requires_user_session()
def new_listing_page5_content_framed():
    return page_frame(
        f"""
        {new_listing_page5_content()}
        <div style="display: none">
            {image_input_carrier()}
            <textarea id="description" hx-preserve name="description" placeholder="Enter your description here"></textarea>
        </div>
        """,
        5,
    )


def new_listing_page5_content():
    return """
    <div class="maintext">
        <h1>Where exactly is your home?</h1>
        <table>
            <tr>
                <td><label for="address">Address:</label></td>
                <td><input id="address" hx-preserve type="text" name="address" class="line-input" required></td>
            </tr>
            <tr>
                <td><label for="postalcode">Postal code:</label></td>
                <td><input id="postalcode" hx-preserve type="text" name="postalcode" class="line-input" required></td>
            </tr>
        </table>
    </div>
    """


@route("/new-listing/page6")
@requires_user_session()
def new_listing_page6():
    return html(
        "Register New Listing Page 6", with_navbar(new_listing_page6_content_framed())
    )


@route("/new-listing/page6/content")
@requires_user_session()
def new_listing_page6_content_framed():
    return page_frame(
        f"""
        {new_listing_page6_content()}
        """,
        6,
        next="summary",
    )


def new_listing_page6_content():
    return """
    <div class="maintext">
        <div class="page6">
            <h1>How much does it cost to rent your home <i>per</i> night?</h1>
            <br>
            <br>
            <form oninput="outputNumber.value = price.value ? (parseFloat(price.value * 0.95).toFixed(2)) : ''">
                <p>
                    <label class="left" for="price">Enter price:</label>
                    <input type="text" hx-preserve id="price" name="price" maxlength="7" pattern="\d{1,7}" inputmode="numeric" required>
                    <span class="right"><b>NOK</b> per night</span>
                </p>
                <p>
                    <span class="middle">After the price of our services (5%), you're</span>
                </p>
                <p>
                    <span class="left">left with:</span>
                    <output id="outputNumber" name="outputNumber"> </output>
                    <span class="right"><b>NOK</b> per night</span>
                </p>
            </form>
        </div>
    </div>
    """


@get("/new-listing/summary")
@requires_user_session()
def new_listing_summary():
    return html(
        "Summary",
        with_navbar(new_listing_summary_content()),
    )


@route("/new-listing/summary/content")
@requires_user_session()
def new_listing_summary_content():
    return page_frame(
        f"""
        <div id="summary">
            <div class="maintext">
                <h1>Your summary!</h1>
               

                <h2><b>Pictures:</b></h2>
                <p>Show us what your beautiful home looks like!</p>
                {image_input()}

                <h2><b>Description:</b></h2>
                <p>Is it a peaceful retreat, a great place to gather with friends or is it something truly unique?</p>
                <div class="fields">
                    <textarea id="description" hx-preserve name="description" placeholder="Enter your description here"></textarea>
                </div>

                <h2><b>Location:</b></h2>
                <p>Where exactly is your home?</p>
                <div class="fields">
                    <label>Address:</label>
                    <input id="address" hx-preserve type="text" name="address" class="line-input" required>
                    <label>Postal code:</label>
                    <input id="postalcode" hx-preserve type="text" name="postalcode" class="line-input" required>
                </div>

                <h2><b>Number of:</b></h2>
                <p>Beds, bathrooms, kitchens and more!</p>
                <div class="fields">
                    <label>Bedrooms:</label>
                    <input id="bedrooms" hx-preserve type="number" name="bedrooms" class="line-input" required>
                    <label>Beds:</label>
                    <input id="beds" hx-preserve type="number" name="beds" class="line-input" required>
                    <label>Bathrooms:</label>
                    <input id="bathrooms" hx-preserve type="number" name="bathrooms" class="line-input" required>
                    <label>Square Meters:</label>
                    <input id="squaremeters" hx-preserve type="number" name="squaremeters" class="line-input" required>
                    <label>Parking spots:</label>
                    <input id="parkingspots" hx-preserve type="number" name="parkingspots" class="line-input" required>
                    <label>Kitchens:</label>
                    <input id="kitchens" hx-preserve type="number" name="kitchens" class="line-input" required>
                </div class="fields">

                <h2><b>Price:</b></h2>
                <p><i>Per</i> night</p>
                 <form oninput="outputNumber.value = price.value ? (parseFloat(price.value * 0.95).toFixed(2)) : ''">
                <p>        
                    <label class="left" for="price">Enter price:</label>
                    <input type="text" hx-preserve id="price" name="price" maxlength="7" pattern="\d{1,7}" inputmode="numeric" required>
                    <span class="right">NOK per night</span>
                </p>
                <p>
                    <span class="middle">After the price of our services (5%), you're</span>
                </p>
                <p>
                    <span class="left">left with:</span>
                    <output id="outputNumber" name="outputNumber"> </output>
                    <span class="right">NOK per night</span>
                </p>
            </form>



               

                <button
                    hx-post=""
                    hx-target="body"
                    hx-include="input,textarea"
                    hx-encoding="multipart/form-data"
                    class="create-listing-button"
                    >Create Listing</button>
            </div>
        </div>
        """,
        prev="page5",
    )


@post("/new-listing/summary")
@requires_user_session()
def new_listing_summary():
    cnx = db.cnx()
    cur = cnx.cursor()

    session_token = get_session_token()

    finn_token = """SELECT Email
                     FROM Session
                     WHERE Token = %s"""

    cur.execute(finn_token, (session_token,))

    email = cur.fetchone()[0]
    address = request.forms["address"]
    postal_code = request.forms["postalcode"]
    description = request.forms["description"]
    price = request.forms["price"]
    bedrooms = request.forms["bedrooms"]
    beds = request.forms["beds"]
    bathrooms = request.forms["bathrooms"]
    square_meters = request.forms["squaremeters"]
    parking_spots = request.forms["parkingspots"]
    kitchens = request.forms["kitchens"]

    cur.execute(
        """
        INSERT INTO PropertyListing (Email, Address, PostalCode, Description, Price, Bedrooms, Beds, Bathrooms, SquareMeters, ParkingSpots, Kitchens) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (
            email,
            address,
            postal_code,
            description,
            price,
            bedrooms,
            beds,
            bathrooms,
            square_meters,
            parking_spots,
            kitchens,
        ),
    )

    for file in request.files.getall("image-files"):
        print(file)
        file.save("static/uploads")

    response.status = 303
    response.add_header("Location", "/user-profile")

    cnx.commit()
    cur.close()
