from bottle import route

from ..components import html, with_navbar


@route("/sign-up")
def sign_up():
    return html(
        "Sign up",
        with_navbar("""
            <main id="sign-up">
                <div>
                    <form name="sign-up" id="sign-up" action="sign-up">
                        <h1>Sign up</h1>
                            <label for="email">Email:</label>
                            <input type="email" name="email" id="email" placeholder="ola.nordmann@gmail.com">
                            <label for="password">Password:</label>
                            <input type="password" name="password" id="password" placeholder="********">
                            <label for="confirm-password">Confirm password:</label>
                            <input type="password" name="confirm-password" id="confirm-password" placeholder="********">
                        <button>Sign up</button>
                        <p>Already have an account?</p>
                        <p><a href="login">Log in instead</a></p>
                    </form>
                </div>
            </main>
        """),
    )
