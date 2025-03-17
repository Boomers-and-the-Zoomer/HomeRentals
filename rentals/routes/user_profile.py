from bottle import route

from ..components import html, with_navbar


@route("/user-profile")
def user_profile():
    return html(
        "User Profile",
        with_navbar("""
            <main id="user-profile">
                <div class="top_page">
                    <div class="profile_box">
                        <div class="circle">
                            <img src="https://cdn.europosters.eu/image/750/83398.jpg" class="profile_picture" alt="Profile picture">
                        </div>
                        <div>
                            <p>Rating 2.4</p>
                            <br><br>
                            <p>Host since XXXX</p>
                        </div>
                    </div>
                    <div>
                        <div class="fieldset">
                            <fieldset>
                                <legend>About:</legend>
                                <p><b>Lives in:</b></p>
                                <p>Toronto, Canada</p>
                                <br><br>
                                <p><b>Languages:</b></p>
                                <p>Norwegian, English, Urdu</p>
                                <br><br>
                                <p><b>Age:</b></p>
                                <p>Old</p>
                            </fieldset>
                        </div>
                        <fieldset class="fieldset">
                            <legend>Fun fact:</legend>
                            <p>Knows Rick</p>
                        </fieldset>
                    </div>
                    <br><br>
                </div>
                <div class="ad_preview">
                    <h3>Listings</h3>
                </div>
            </main>
        """),
    )
