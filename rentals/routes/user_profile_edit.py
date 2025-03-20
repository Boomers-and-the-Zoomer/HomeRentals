from bottle import route

from ..components import html, with_navbar


@route("/user-profile/edit")
def user_profile_edit():
    return html(
        "User Profile edit",
        with_navbar("""
            <main id="user-profile">
                <div class="user_profile_edit">
                    <a href="http://localhost:8080/user-profile" class="button_cancel">Cancel</a>
                    <a href="http://localhost:8080/user-profile" class="button_confirm">Confirm</a>
                        <div class="profile_pic">
                            <div class="circle_edit">
                                <img src="https://cdn.europosters.eu/image/750/83398.jpg" class="profile_picture" alt="Profile picture">
                            </div>
                            <a href="http://localhost:8080/user-profile" class="button_picture">Update picture</a>
                            <p class="item"><b>Name:</b><p>
                             <textarea>Morty</textarea>
                        </div>
                    <div class="info">
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
