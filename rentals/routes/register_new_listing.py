from bottle import route

from ..components import html, with_navbar


@route("/new-listing")
def new_listing():
    return html(
        "Register New Property Listing",
        with_navbar("""
            <main id="register_new_listing">
                <div id="page1">
                    <div class="maintext">
                        <h1>
                            We are so happy that you've decided to<br> 
                            rent out your home!
                        </h1>
                        <br>
                        <h2>
                        <br>
                            Follow these steps, this is <i>easy</i>!
                        </br>
                        </h2>
                    </div>
                    <div class="container">
                        <p class="bottom-left">
                            1/5
                        </p>
                    </div>
                </div>
            </main>
        """),
    )
