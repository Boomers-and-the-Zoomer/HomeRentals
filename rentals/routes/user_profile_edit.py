from bottle import route

from ..components import html, with_navbar


@route("/user-profile/edit")
def user_profile_edit():
    return html(
        "User Profile edit",
        with_navbar("""
            <main id="user-profile" class="user_profile_edit">
                <div class="top_page">
                    <a href="http://localhost:8080/user-profile" class="button">Cancel</a>
                        <div class="circle">
                            <img src="https://cdn.europosters.eu/image/750/83398.jpg" class="profile_picture" alt="Profile picture">
                        </div>
                            <p><b>Morty</b><p>
                        </div>
                    <div class="about">
                        <div class="fieldset">
                            <form>
                                <fieldset>
                                    <legend><b>About:</b></legend>
                                    <p><b>Lives in:</b></p>
                                    <textarea>Toronto, Canada</textarea>
                                    <br><br>
                                    <p><b>Languages:</b></p>
                                    <textarea>Norwegian, English, Urdu</textarea>
                                    <br><br>
                                    <p><b>Age:</b></p>
                                    <textarea>Old</textarea>         
                                </fieldset>
                                <fieldset>
                                    <legend><b>Fun fact:</b></legend>
                                    <textarea>Knows Rick</textarea>
                                </fieldset>
                            </form>
                        </div>
                    </div>
                </div>
            </main>
        """),
    )
