from bottle import route
from ..components import html, with_navbar
from .. import db


@route("/temp-view-rental/<listing>")
def view_rental(listing: int):
    cnx = db.db_cnx()
    cur = cnx.cursor()

    cur.execute(
        """
        SELECT Address,Description,Bedrooms,Beds,Bathrooms
        FROM PropertyListing
        WHERE PropertyListingID=%s
        """,
        (listing,),
    )

    address, description, bedrooms, beds, bathrooms = cur.fetchone()

    var = f"""
    <h1>{address}</h1>
    <div class="left">
        <div class="main-gallery">
            <img width=485 height=270>
            
            <div class="sub-gallery">
                <img width=230 height=130>
                <img width=230 height=130>
                <img width=230 height=130>
                <img width=230 height=130>
            </div>
        </div>
        
        <p>{bedrooms} bedrooms · {beds} beds · {bathrooms} bathrooms</p>
        <p class="description">{description}</p>
    </div>
    <div class="calendar">
    
    </div>
    """

    return html(
        "View Rental",
        with_navbar(
            f"""
            <main id="view-rental">
            {var}
            </main>
            """
        ),
    )
