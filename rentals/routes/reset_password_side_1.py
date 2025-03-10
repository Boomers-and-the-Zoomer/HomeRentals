from bottle import route

from ..components import (
    html,
    with_navbar,
    simple_account_form,
    simple_account_form_position,
)


@route("/reset-password-side-1")
def reset_password_side_1():
    form = simple_account_form_position(
        simple_account_form(
            "Reset Password-1",
            """
            <h1>Reset Password</h1>
            <br>
            <p>Enter your e-mail and we will send you an email with a
            password-reset link</p>
            <br>
            <label>E-mail:</label>
            <input type="email" name="email" id="email" placeholder="Enter your e-mail here">
            <button>Send link</button>
            """,
        )
    )
    return html(
        "Reset Password",
        with_navbar(f"""
                    <main id="reset-password">
                        <div>
                        {form}
                        </div>
                    </main>
                    """),
    )
