from bottle import route, run, template, request, HTTPError, redirect
from datetime import datetime

from ..components import html, with_navbar
from .. import db


@route("/view-rental/<PropertyListingID>")
def view_rental(PropertyListingID):
    print("Accessing view-rental", PropertyListingID)
    cnx = db.db_cnx()
    cursor = cnx.cursor()

    cursor.execute(
        """
        SELECT * FROM PropertyListing WHERE PropertyListingID = %s
        """,
        (PropertyListingID,),
    )
    rental = cursor.fetchone()
    print("Rental:", rental)

    if not rental:
        raise HTTPError(404, "Property listing not found")

    return view_rental_template(rental)


def view_rental_template(rental):
    return html(
        f"Rental Unit {rental[2]}",
        with_navbar(f"""
                <main id="book-calendar">
                
                    <h1>Address: {rental[2]}</h1>
                    <ul>Information</ul>
                        <li>Bedrooms: {rental[4]}</li>
                        <li>Bathrooms: {rental[5]}</li>
                        <li>{rental[6]} m2</li>
                        <li>Parking spots: {rental[7]}</li>
                        <li>Kitchens: {rental[8]}</li>
                    <form action="/book-rental" method="post">
                        <label for="from_date">From Date:</label>
                        <input type="datetime-local" id="from_date" name="from_date" required><br>
                        <label for="to_date">To Date:</label>
                        <input type="datetime-local" id="to_date" name="to_date" required><br>
                        <input type="hidden" name="PropertyListingID" value="{rental[0]}">
                        <button type="submit">Book Now</button>
                    </form>
                </main>
        """),
    )


@route("/book-rental", method="POST")
def book_rental():
    PropertyListingID = request.forms.get("PropertyListingID")
    Email = "test.testerson@example.com"  # Dette er en placeholder for email, slik at jeg får booket noe inn i DB
    raw_from_date = request.forms.get("from_date")
    raw_to_date = request.forms.get("to_date")

    try:
        from_date = datetime.strptime(raw_from_date, "%Y-%m-%dT%H:%M")
        to_date = datetime.strptime(raw_to_date, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise HTTPError(400, "Invalid date format provided.")

    if from_date >= to_date:
        raise HTTPError(400, "Invalid booking: Start date must be before end date")

    cnx = db.db_cnx()
    cursor = cnx.cursor()

    overlappingSjekk = """
        SELECT * FROM Booking
        WHERE PropertyListingID=%s
            AND (StartTime<%s AND EndTime >%s)
    """
    parameterForBooking = (PropertyListingID, to_date, from_date)

    cursor.execute(overlappingSjekk, parameterForBooking)

    if cursor.fetchone() is not None:
        raise HTTPError(400, "Booking dates overlap with an existing booking.")

    print(
        "Booking rental: PropertyListingID={}, Email={}, from_date={}, to_date={}".format(
            PropertyListingID, Email, from_date, to_date
        )
    )

    cursor.execute(
        """
        INSERT INTO Booking (PropertyListingID, Email, StartTime, EndTime)
        VALUES (%s, %s, %s, %s)
        """,
        (PropertyListingID, Email, from_date, to_date),
    )
    cnx.commit()
    cnx.close()

    redirect("/view-rental/{}".format(PropertyListingID))
