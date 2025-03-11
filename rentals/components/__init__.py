from .. import icons
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
    return f"""
        <div id="navigated">
            <nav id="top-nav">
                <ul>
                    <li id="nav-homerentals"><a href="/">HomeRentals</a></li>
                    <li id="nav-active-bookings"><a href="/bookings/active">View Active Bookings</a></li>
                    <li id="nav-rent-cta"><a href="/listings/create">Rent out your property</a></li>
                    <li id="nav-user">
                        <div>
                            {icons.user()}
                        </div>
                    </li>
                </ul>
            </nav>
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
