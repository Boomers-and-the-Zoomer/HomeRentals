from bottle import route

from ..components import html, with_navbar


@route("/user-profile")
def user_profile():
    return html(
        "User Profile",
        with_navbar("""
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
                            <p><b>Morty</b><p>
                            <p>Host<p>
                        </div>
                    </div>
                    <div class="about">
                        <div class="fieldset">
                            <fieldset>
                                <legend><b>About:</b></legend>
                                <p><b>Lives in:</b> Toronto, Canada</p>
                                <br><br>
                                <p><b>Languages:</b> Norwegian, English, Urdu</p>
                                <br><br>
                                <p><b>Age:</b> Old</p>

                            </fieldset>
                        </div>
                        <div class="fieldset">
                            <fieldset>
                                <legend><b>Fun fact:</b></legend>
                                <p>Knows Rick</p>
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
        """),
    )
