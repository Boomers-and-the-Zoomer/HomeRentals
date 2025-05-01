from bottle import route, response
from ..auth import requires_user_session, get_session_token
from ..components import html, with_navbar
from .. import db


@route("/user-profile")
@requires_user_session()
def user_profile():
    cnx = db.cnx()
    cur = cnx.cursor()
    session_token = get_session_token()
    cur.execute(
        """
        SELECT UserAccount.Email
        FROM UserAccount, Session
        WHERE UserAccount.Email=Session.Email
            AND Session.Token=_binary %s
            AND UserAccount.Email IN (
                SELECT Email
                FROM User
                )
        """,
        (session_token,),
    )
    row = cur.fetchone()
    if row == None:
        response.status = 303
        response.add_header("Location", "/user-information")
        cur.close()
        return

    cur.execute(
        """
        SELECT FirstName,Lives,Languages,Age,FunFact,ProfilePicture,Session.Email
        FROM User, Session
        WHERE User.Email=Session.Email
            AND Session.Token=_binary %s
        """,
        (session_token,),
    )
    (first_name, lives, languages, age, fun_fact, profile_picture, email) = (
        cur.fetchone()
    )
    if lives == None:
        lives = ""
    if languages == None:
        languages = ""
    if age == None:
        age = ""
    if fun_fact == None:
        fun_fact = ""
    if profile_picture == None or profile_picture == '':
        profile_picture = "default.jpg"

    cur.execute(
        """
        SELECT PropertyListing.PropertyListingID, PropertyListing.Address, Filename, RegistrationDate
        FROM PropertyListing, PropertyPicture, Picture
        WHERE PropertyListing.PropertyListingID=PropertyPicture.PropertyListingID
            AND PropertyPicture.PictureID=Picture.PictureID
            AND PropertyListing.Email=%s
        ORDER BY RegistrationDate ASC
        """,
        (email,),
    )

    pictures = cur.fetchall()
        
    # noe rart kommer til å skje hvis man fjerner den tidligste listingen. variablet vil få ny verdi, slev om tidligere dato fortsatt er riktig
    cur.close()

    properties = {}
    for listing_id, address, picture_filename, RegistrationDate in pictures:
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
    is_host = "Guest"
    if len(properties) != 0:
        regDate = pictures[0][3]
        host_since = f"""<p><u>Host since {regDate.year}</u></p>"""
        is_host = """<p>Host<p>"""

    return html(
        "User Profile",
        with_navbar(
            f"""
            <main id="user-profile">
                <div class="top_page">
                    <div class="buttons">
                        <a href="http://localhost:8080/user-profile/edit" class="button">Edit profile</a>
                        <a href="http://localhost:8080/user-information/edit" class="button">Update account details</a>
                    </div>
                    <div class="profile_box">
                        <div class="circle">
                            <img src="/static/profilepicture/{profile_picture}" class="profile_picture" alt="Profile picture">
                        </div>
                        <div class="profile_box_info">
                            <p><u></u></p>
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
                            <h2><b>About:</b></h2>
                            <fieldset>
                                <legend><b>Lives in</b></legend>
                                <p>{lives}</p>
                            </fieldset>
                            <br>
                            <fieldset>
                                <legend><b>Languages</b></legend>
                                <p>{languages}</p>
                            </fieldset>
                            <br>
                            <fieldset>
                                <legend><b>Age:</b></legend>
                                <p>{age}</p>
                            </fieldset>
                            <br>
                            <fieldset>
                                <legend><b>Fun fact:</b></legend>
                                <p>{fun_fact}</p>
                            </fieldset>
                        </div>
                    </div>
                </div>
                <div class="ad_preview">
                    <h3>Listings:</h3>
                    <div>
                        {listings}
                    </div>
                </div>
            </main>
       """,
        ),
    )
