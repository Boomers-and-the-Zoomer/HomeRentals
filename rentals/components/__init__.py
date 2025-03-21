from .. import icons
from ..auth import validate_session_or_refresh
from ..util import dict_to_attr_string


def html(title: str, content: str, html={"lang": "en"}, body={}) -> str:
    """
    Top-level HTML boilerplate.

    Do not use this in HTMX-only routes.
    """

    return f"""
    <!DOCTYPE html>
    <html {dict_to_attr_string(html)}>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
            <link rel="stylesheet" href="/static/fonts/inter/inter.css">
            <link rel="stylesheet" href="/static/style.css">
            <script src="/static/htmx.min.js"></script>
            <script src="/static/script.js"></script>
            <meta name="htmx-config" content='{{"defaultSwapStyle": "outerHTML"}}'>
            <title>{title}</title>
        </head>
        <body {dict_to_attr_string(body)}>
            {content}
        </body>
    </html>
    """


def with_navbar(content: str) -> str:
    """ """

    logged_in = validate_session_or_refresh()

    def if_logged_in_else(logged_in_content: str, logged_out_content: str):
        if logged_in:
            return logged_in_content
        else:
            return logged_out_content

    account_menu = if_logged_in_else(
        f"""
        <a href="/user-profile">
            {icons.user()}
            <span>Profile</span>
            {icons.chevron_right()}
        </a>
        <a href="/bookings/active">
            {icons.calendar_clock()}
            <span>Active bookings</span>
            {icons.chevron_right()}
        </a>
        <button form="log-out-form" type="submit">
            {icons.log_out()}<span>Log out</span>{icons.chevron_right()}
        </button>
        """,
        f"""
        <a href="/log-in">
            {icons.log_in()}
            <span>Log in</span>
            {icons.chevron_right()}
        </a>
        <a href="/sign-up">
            {icons.user_plus()}
            <span>Sign up</span>
            {icons.chevron_right()}
        </a>
        """,
    )

    return f"""
        <div id="navigated">
            <nav id="top-nav">
                <ul>
                    <li id="nav-homerentals"><a href="/">HomeRentals</a></li>
                    <li id="nav-rent-cta"><a href="/new-listing">Rent out your property</a></li>
                    <li id="nav-user">
                        <button popovertarget="top-nav-user-popover">
                            {icons.user()}
                        </button>
                    </li>
                </ul>
            </nav>
            <div popover id="top-nav-user-popover">
                <h1>Account</h1>
                {account_menu}
                <form id="log-out-form" action="/log-out" method="post"></form>
            </div>
            <div id="nav-dummy" aria-hidden="true"></div>
            {content}
        </div>
    """


def simple_account_form_position(content: str) -> str:
    return f"""
        <div class="simple-account-form-position">
            <div>
                {content}
            </div>
        </div>
    """


def simple_account_form(name: str, content: str) -> str:
    return f"""
        <form class="simple-account-form" name="{name}" action="" method="post">
            {content}
        </form>
    """


def image_input():
    """
    An image output. As currently implemented, it only supports being instaniated once on a given page.
    """

    return f"""
    <div class="image-upload">
        <div class="image-upload-gallery">
        {_single_image()}
        {_single_image()}
        {_single_image()}
        {_single_image()}
        {_single_image()}
        </div>
            <button type="none">
                <label for="image-upload-input">
                    Add picture(s)
                </label>
            </button>
        <input id="image-upload-input" name="empty" type="file" accept="image/*" multiple>
        {image_input_carrier()}
    </div>
    """


def _single_image():
    return """
    <div class="image">
        <img class="img" width=200 height=200>
        <button type="none" class="overlay">
            <img src="/static/icons/x.svg">
        </button>
    </div>
    """


def image_input_carrier():
    return """<input id="image-upload-carrier" hx-preserve name="image-files" type="file" accept="image/*" multiple>"""
