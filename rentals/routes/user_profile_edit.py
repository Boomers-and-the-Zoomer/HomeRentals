import mysql.connector

from bottle import get, post, request, response
import os

from ..auth import requires_user_session, get_session_token
from ..components import html, with_navbar
from .. import db
from ..util import error


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
                        <p class="item"><b>Name:</b>{first_name}</p>
                    </div>
                    <div class="info">
                        <div class="fieldset">
                            <form id="update_info" enctype="multipart/form-data" action="" method="POST" hx-boost="true">
                                <h2>About</h2>
                                <fieldset>
                                    <legend><b>Lives in:</b></legend>
                                    <textarea id="lives_form" name="lives_form" rows="2" cols="40"style="resize: none;" placeholder="Hønefoss, Norway">{lives}</textarea>
                                    <div id="error-target-lives"></div>
                                </fieldset>
                                <br>
                                <fieldset>
                                    <legend><b>Languages:</b></legend>
                                    <textarea id="languages_form" name="languages_form" rows="2" cols="40"style="resize: none;" placeholder="Norwegian">{languages}</textarea>
                                    <div id="error-target-languages"></div>
                                </fieldset>
                                <br>
                                <fieldset>
                                    <legend><b>Age:</b></legend>
                                    <textarea id="age_form" name="age_form" rows="1" cols="40"style="resize: none;" placeholder="25">{age}</textarea>
                                    <div id="error-target-age"></div>
                                </fieldset>
                                <br>
                                <fieldset>
                                    <legend><b>Fun fact:</b></legend>
                                    <label for="fun_fact_form"></label>
                                    <textarea id="fun_fact_form" name="fun_fact_form" rows="3" cols="40"style="resize: none;" placeholder="Something fun">{fun_fact}</textarea>
                                    <div id="error-target-funfact"></div>
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

    try:
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
    except mysql.connector.errors.DataError as e:
        if "Data too long for column 'Lives'" in str(e):
            return error("'Lives in' field only allows Up to 40 symbols.", target_id="error-target-lives")

        if "Data too long for column 'Languages'" in str(e):
            return error("'Languages' field only allows Up to 50 symbols.", target_id="error-target-languages")
        if "Data too long for column 'Age'" in str(e):
            return error("'Age' field only allows Up to 6 symbols.", target_id="error-target-age" )
        if "Data too long for column 'FunFact'" in str(e):
            return error("'Fun Fact' field only allows Up to 50 symbols.", target_id="error-target-funfact")  
        return error("Unexpected server error", target_id="error-target-funfact")

    cnx.commit()
    cur.close()

    response.status = 303
    response.add_header("Location", "/user-profile")
