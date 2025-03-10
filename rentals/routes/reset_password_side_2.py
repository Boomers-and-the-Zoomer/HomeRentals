from bottle import route
from ..components import (
    html,
    with_navbar,
    simple_account_form,
    simple_account_form_position,
)


@route("/reset-password-side-2")
def reset_password_side_2():
    form = simple_account_form_position(
        simple_account_form(
            "Reset Password-2",
            """
            <h1>Reset Password</h1>
            <br>
            <p>Type in your new password twice</p>        
            <label>New password:</label>
            <input type="password" name="password1" id="password1" placeholder="Password">
            <label>Confirm new password:</label>
            <input type="password" name="password2" id="password2" placeholder="Password">
            <button>Reset Password</button>
            """,
        )
    )

    return html(
        "Reset Password",
        with_navbar(f"""
            <main id="reset-password-side-2">
                <div>
                {form}
                </div>
            </main>
            """),
    )
