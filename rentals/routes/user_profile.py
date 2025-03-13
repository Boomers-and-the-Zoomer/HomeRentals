from bottle import route

from ..components import html, with_navbar


@route("/user-profile")
def user_profile():
    return html(
        "User Profile",
        with_navbar("""
            <main id="user-profile">
                <div class="profile_box">
                    <img src="https://cdn.europosters.eu/image/750/83398.jpg" class="profile_picture" alt="Profile picture">
                    <p>Rating 2.4</p>
                    <p>Host since XXXX</p>
                </div>
                <div>
                    <fieldset>
                        <legend>About:</legend>
                        <th><b>Lives in:</b></th>
                        <tr>Toronto, Canada</tr>
                        <br><br>
                        <th><b>Languages:</b></th>
                        <tr>Norwegian, English, Urdu</tr>
                        <br><br>
                        <th><b>Age:</b></th>
                        <tr>Old</tr>
                    </fieldset>
                    <fieldset>
                        <legend>Fun fact:</legend>
                        <tr>Knows Rick</tr>
                    </fieldset>
                    <br><br>
                </div>
                <div>
                    <h3>Listings</h3>
                </div>
            </main>
        """),
    )
