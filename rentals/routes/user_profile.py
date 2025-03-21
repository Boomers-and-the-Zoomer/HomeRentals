from bottle import route
from ..auth import requires_user_session, get_session_token
from ..components import html, with_navbar
from .. import db


@route("/user-profile")
@requires_user_session()
def user_profile():
    cnx = db.db_cnx()
    cur = cnx.cursor()

    session_token = get_session_token()

    cur.execute(
        """
        SELECT FirstName,Lives,Languages,Age,FunFact,Session.Email
        FROM User, Session
        WHERE User.Email=Session.Email
            AND Session.Token=_binary %s
        """,
        (session_token,),
    )
    (first_name, lives, languages, age, fun_fact, email) = cur.fetchone()
    if lives == None:
        lives = ""
    if languages == None:
        languages = ""
    if age == None:
        age = ""
    if fun_fact == None:
        fun_fact = ""

    cur.execute(
        """
        SELECT PropertyListing.PropertyListingID, PropertyListing.Address, Filename
        FROM PropertyListing, PropertyPicture, Picture
        WHERE PropertyListing.PropertyListingID=PropertyPicture.PropertyListingID
            AND PropertyPicture.PictureID=Picture.PictureID
            AND PropertyListing.Email=%s
        """,
        (email,),
    )
    pictures = cur.fetchall()
    cur.close()

    properties = {}
    for listing_id, address, picture_filename in pictures:
        if listing_id not in properties:
            properties[listing_id] = [address, picture_filename]

    print(f"{properties=}")
    listings = ""
    for property, o in properties.items():
        address, filename = o
        listings += f"""
            <a href="/view-rental/{property}" class="ad_picture">
                <p>{address}</p>
                <img src="/static/uploads/{filename}" alt="Property listing">
            </a>\n"""

    host_since = ""
    is_host = ""
    if len(properties) != 0:
        host_since = """<p><u>Host since XXXX</u></p>"""
        is_host = """<p>Host<p>"""

    return html(
        "User Profile",
        with_navbar(
            f"""
            <main id="user-profile">
                <div class="top_page">
                    <a href="http://localhost:8080/user-profile/edit" class="button">Edit profile</a>
                    <div class="profile_box">
                        <div class="circle">
                            <img src="https://cdn.europosters.eu/image/750/83398.jpg" class="profile_picture" alt="Profile picture">
                        </div>
                        <div class="profile_box_info">
                            <p><u>Rating 2.4</u></p>
                            <br>
                            {host_since}
                        </div>
                        <div class="name">
                            <p><b>{first_name}</b><p>
                            {is_host}
                        </div>
                    </div>
                    <div class="about">
                        <div class="fieldset">
                            <fieldset>
                                <legend><b>About:</b></legend>
                                <p><b>Lives in:</b> {lives}</p>
                                <p><b>Languages:</b> {languages}</p>
                                <p><b>Age:</b> {age}</p>
                            </fieldset>
                        </div>
                        <div class="fieldset">
                            <fieldset>
                                <legend><b>Fun fact:</b></legend>
                                <p> {fun_fact}</p>
                            </fieldset>

                        </div>
                    </div>
                </div>
                <div class="ad_preview">
                    <h3>Listings:</h3>
                    {listings}
                </div>
            </main>
       """,
        ),
    )
