from bottle import get, post, request, response
import os

from ..auth import requires_user_session, get_session_token
from ..components import html, with_navbar
from .. import db


@get("/user-profile/edit")
@requires_user_session()
def user_profile_edit():
    cnx = db.cnx()
    cur = cnx.cursor()

    session_token = get_session_token()

    cur.execute(
        """
        SELECT FirstName,Lives,Languages,Age,FunFact,ProfilePicture
        FROM User, Session
        WHERE User.Email=Session.Email
            AND Session.Token=_binary %s
        """,
        (session_token,),
    )
    (first_name, lives, languages, age, fun_fact, profile_picture) = cur.fetchone()
    if lives == None:
        lives = ""
    if languages == None:
        languages = ""
    if age == None:
        age = ""
    if fun_fact == None:
        fun_fact = ""
    if profile_picture == None or profile_picture == "":
        profile_picture = "default.jpg"

    cur.close()

    return html(
        "User Profile edit",
        with_navbar(
            f"""
            <main id="user-profile">
                <div class="user_profile_edit">
                    <div class="buttons">
                        <a href="http://localhost:8080/user-profile" class="button_cancel">Cancel</a>
                        <button class="button_confirm" type="submit" form="update_info">Confirm</button>
                    </div>
                    <div class="profile_pic">
                        <div class="circle_edit">
                            <img src="/static/profilepicture/{profile_picture}" class="profile_picture" alt="Profile picture">
                        </div>
                        <label for="picture_form" class="button_picture">Update Picture</label>
                        <input form="update_info" id="picture_form" name="picture_form" style=" display: none;" type="file">
                        <p class="item"><b>Name:</b> {first_name}<p>
                    </div>
                    <div class="info">
                        <div class="fieldset">
                            <form id="update_info" enctype="multipart/form-data" action="" method="POST">
                                <h2>About</h2>
                                <fieldset>
                                    <legend><b>Lives:</b></legend>
                                    <textarea id="lives_form" name="lives_form" rows="3" cols="40"style="resize: none;">{lives}</textarea>
                                </fieldset>
                                <br>
                                <fieldset>
                                    <legend><b>Languages:</b></legend>
                                    <textarea id="languages_form" name="languages_form" rows="3" cols="40"style="resize: none;">{languages}</textarea>
                                </fieldset>
                                <br>
                                <fieldset>
                                    <legend><b>Age:</b></legend>
                                    <textarea id="age_form" name="age_form" rows="3" cols="40"style="resize: none;">{age}</textarea>
                                </fieldset>
                                <br>
                                <fieldset>
                                    <legend><b>Fun fact:</b></legend>
                                    <label for="fun_fact_form"></label>
                                    <textarea id="fun_fact_form" name="fun_fact_form" rows="3" cols="40"style="resize: none;">{fun_fact}</textarea>
                                </fieldset>
                            </form>
                        </div>
                    </div>
                </div>
            </main>
        """
        ),
    )


@post("/user-profile/edit")
@requires_user_session()
def user_profile_edit():
    cnx = db.cnx()

    session_token = get_session_token()

    cur = cnx.cursor()
    cur.execute(
        """
        SELECT ProfilePicture, ExternalID
        FROM User, Session
        WHERE User.Email=Session.Email
            AND Session.Token=_binary %s
        """,
        (session_token,),
    )
    (old_profile_picture,externalID) = cur.fetchone()
    print('DEBUGGER')
    print(old_profile_picture)

    cur.close()

    cur = cnx.cursor()

    lives = request.forms["lives_form"]
    languages = request.forms["languages_form"]
    age = request.forms["age_form"]
    fun_fact = request.forms["fun_fact_form"]
    file = request.files.get("picture_form")

    profile_picture_name = "profile-pic-" + str(externalID)
    if file != None:
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = profile_picture_name + file_extension
        save_path = os.path.join("static", "profilepicture", new_filename)
        file.save(save_path, overwrite=True)

    query_params = [lives, languages, age, fun_fact]
    update_picture = ""
    if file != None:
        update_picture = ", ProfilePicture = %s"
        query_params.append(new_filename)
    query_params.append(session_token)
    cur.execute(
        f"""
        UPDATE User
        SET Lives = %s, Languages = %s, Age = %s, FunFact = %s{update_picture}
        WHERE User.Email=(
            SELECT Email
            FROM Session
            WHERE Session.Token=_binary %s
            )
        """,
        tuple(query_params),
    )

    cnx.commit()
    cur.close()

    response.status = 303
    response.add_header("Location", "/user-profile")
