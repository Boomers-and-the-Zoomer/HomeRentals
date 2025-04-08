from bottle import get, post, request, response

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
                            <img src="https://cdn.europosters.eu/image/750/83398.jpg" class="profile_picture" alt="Profile picture">
                        </div>
                        <label for="picture" class="button_picture">Update Picture</label>
                        <input form="update_info", id="picture_form", name="picture"" style=" display: none;" type="file">
                        <p class="item"><b>Name:</b><p>
                         <textarea>{first_name}</textarea>
                    </div>
                    <div class="info">
                        <div class="fieldset">
                            <form id="update_info" action="" method="POST">
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
    cur = cnx.cursor()

    session_token = get_session_token()

    lives = request.forms["lives_form"]
    languages = request.forms["languages_form"]
    age = request.forms["age_form"]
    fun_fact = request.forms["fun_fact_form"]

    cur.execute(
        """
        UPDATE User
        SET Lives = %s, Languages = %s, Age = %s, FunFact = %s
        WHERE User.Email=(
            SELECT Email
            FROM Session
            WHERE Session.Token=_binary %s
            )
        """,
        (lives, languages, age, fun_fact, session_token),
    )
    cnx.commit()
    cur.close()

    response.status = 303
    response.add_header("Location", "/user-profile")
