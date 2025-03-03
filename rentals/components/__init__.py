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
            <link rel="stylesheet" href="/static/style.css">
            <script src="/static/htmx.min.js"></script>
            <meta name="htmx-config" content='{{"defaultSwapStyle": "outerHTML"}}'>
            <title>{title}</title>
        </head>
        <body {dict_to_attr_string(body)}>
            {content}
        </body>
    </html>
    """
