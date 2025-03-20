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
        SELECT FirstName,Lives,Languages,Age,FunFact
        FROM User, Session
        WHERE User.Email=Session.Email
            AND Session.Token=_binary %s
        """,
        (session_token,),
    )
    (first_name, lives, languages, age, fun_fact) = cur.fetchone()
    if lives == None:
        lives = ""
    if languages == None:
        languages = ""
    if age == None:
        age = ""
    if fun_fact == None:
        fun_fact = ""
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
                            <p><u>Host since XXXX</u></p>
                        </div>
                        <div class="name">
                            <p><b>{first_name}</b><p>
                            <p>Host<p>
                        </div>
                    </div>
                    <div class="about">
                        <div class="fieldset">
                            <fieldset>
                                <legend><b>About:</b></legend>
                                <p><b>Lives in:</b> {lives}</p>
                                <br><br>
                                <p><b>Languages:</b> {languages}</p>
                                <br><br>
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
                    <img src="https://a0.muscache.com/im/pictures/miso/Hosting-756540177431085322/original/a89fcae1-05d1-469a-9b86-a8065abc22c2.jpeg?im_w=720" class="ad_picture" alt="Property listing">
                    <img src="https://a0.muscache.com/im/pictures/074f8383-2194-4a3d-8f3d-ca8dce154cdb.jpg?im_w=720" class="ad_picture" alt="Property listing">
                </div>
            </main>
       """,
        ),
    )
