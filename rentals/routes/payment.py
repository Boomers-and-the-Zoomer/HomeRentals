from ..components import html, with_navbar
from .. import db
from ..auth import requires_user_session, get_session_token
from bottle import route, request, response, post, get
from datetime import date


# Mottar nok info til å finne bookingen
@get("/payment")
@requires_user_session()
def payment():
    pass
    booking_data = request.get_cookie("BookingData")
    property_listing_id, start_time, email = booking_data.split(",")

    cnx = db.cnx()
    cursor = cnx.cursor()

    cursor.execute(
        """
        SELECT Address,Price
        FROM PropertyListing
        WHERE PropertyListingID=%s
        """,
        (property_listing_id,),
    )
    title, price = cursor.fetchone()

    cursor.execute(
        """
        SELECT Filename
        FROM Picture, PropertyPicture
        WHERE PropertyPicture.PictureID=Picture.PictureID
            AND PropertyListingID=%s
        LIMIT 4
        """,
        (property_listing_id,),
    )
    pics = cursor.fetchall()

    cursor.execute(
        """
        SELECT EndTime
        FROM Booking
        WHERE StartTime=%s AND PropertyListingID=%s AND Email=%s
        """,
        (start_time, property_listing_id, email),
    )
    end_time = cursor.fetchone()[0]
    # Fixing start_time
    start_time = date.fromisoformat(start_time)

    total_nights = (end_time - start_time).days

    total_sum = total_nights * price

    # Todo:
    # Lag HTML-formen for betalingsinformasjon
    # Lag HTML av bookingen som blir reserved
    # Sett opp siden med HTML og CSS

    pics = [f'src="/static/uploads/{pic[0]}"' for pic in pics]
    while len(pics) <= 4:
        pics += [""]

    show_ad_html = f"""
        <div class="show_ad">
            <h2>{title}</h2>
            <div>
                <div class="info">
                    <p>{start_time} - {end_time}</p>
                    <p class="total">Total sum for your stay: {total_sum} NOK</p>
                </div>
                <div class="pics">
                    <img {pics[0]} width=230 height=130>
                    <img {pics[1]} width=230 height=130>
                    <img {pics[2]} width=230 height=130>
                    <img {pics[3]} width=230 height=130>
                </div>
            </div>
        </div>
    """

    payment_html = f"""
    <main id="payment">
        <div class="payment">
            <form action="" method="POST">
                <h1>Payment Method</h1>
                <fieldset class="radio_buttons">
                    <label>
                        <input type="radio" name="payment" value="vipps" required>
                        <img src="https://media.snl.no/media/147159/standard_vipps_logo_rgb.png" alt="Vipps" height="25">
                    </label>
                    <label>
                        <input type="radio" name="payment" value="visa" required>
                        <img src="https://upload.wikimedia.org/wikipedia/commons/4/41/Visa_Logo.png" alt="Visa" height="25">
                    </label>
                    <label>
                        <input type="radio" name="payment" value="mastercard">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/0/04/Mastercard-logo.png" alt="Mastercard" height="25">
                    </label>
                </fieldset>
                <fieldset class="vipps_info">
                    <label for="phone">Enter your phone number:</label>
                    <input type="tel" id="phone" placeholder="+47 123 456 78" required>
                </fieldset>
                <fieldset class="visa_info">
                    <label for="name">Name:</label>
                    <input type="text" id="name" required>
                    <label for="card">Payment card number here:</label>
                    <input type="tel" id="card" placeholder="xxxx xxxx xxxx xxxx" maxlength="16" required>
                    <label for="expmonth">Expiry date:</label>
                    <div class="dates">
                        <input type="tel" id="expmonth" placeholder="mm" size="1" required>
                        /
                        <input type="tel" id="expyear" placeholder="yy" size="1" required>
                    </div>
                    <label for="cvv">Security code:</label>
                    <input id="cvv" name="cvv" type="password" size="2" required>
                </fieldset>
                <button type="submit" class="submit-btn">Confirm and Pay</button>
            </form>
        </div>
        {show_ad_html}
    </main>

        """
    return html("Payment", with_navbar(payment_html))


@post("/payment")
@requires_user_session()
def payment():
    # FIXME: Insert shit into database
    response.status = 303
    response.add_header("Location", "/bookings/active")
