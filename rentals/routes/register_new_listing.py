from bottle import route, response, post, get, request

from ..components import html, with_navbar


@route("/new-listing")
def new_listing():
    response.status = 307
    response.add_header("Location", "/new-listing/page1")


@route("/new-listing/page1")
def new_listing_page1():
    return html(
        "Register New Listing Page 1",
        with_navbar(new_listing_page1_content()),
    )


def new_listing_page1_content():
    return """
    <main id="register_new_listing">
        <div id="page1">
            <div class="maintext">
                <h1>
                    We are so happy that you've decided to<br> 
                    rent out your home!
                </h1>
                <br>
                <br>
                <br>
                <br>
                <p>Follow these steps, this is <i>easy</i>!</p>
            </div>
            <p class="page-counter"><b>1/5</b></p>
            <button class="button">Continue</button>
        </div>
    </main>
    """


@route("/new-listing/page2")
def new_listing_page2():
    return html(
        "Register New Listing Page 2",
        with_navbar(new_listing_page2_content()),
    )


def new_listing_page2_content():
    return """
    <main id="register_new_listing">
        <div id="page2">
            <div class="maintext">
                <h1>Show us what your beautiful<br> home looks like!</h1>
                <div class="pictures">
                    <input type="file" accept="image/*">
                    <input type="file" accept="image/*">
                    <input type="file" accept="image/*">
                    <input type="file" accept="image/*">
                </div>
            </div>
            <p class="page-counter"><b>2/5</b></p>
            <button class="button">Continue</button>
        </div>
    </main>
    """


@route("/new-listing/page3")
def new_listing_page3():
    return html(
        "Register New Listing Page 3",
        with_navbar(new_listing_page3_content()),
    )


def new_listing_page3_content():
    return """
    <main id="register_new_listing">
        <div id="page3">
            <div class="maintext">
                <h1>Enter a description of your home!</h1>
                <br><br>
                <p>Is it a peaceful retreat, a great place to gather with friends<br> or is it something truly unique?</p>
            </div>
            <div class="textarea">
                <textarea id="description" hx-preserve name="description" placeholder="Enter your description here"></textarea>
            </div>
            <p class="page-counter"><b>3/5</b></p>
            <div class="back-button">
                <button><u><b>Back</b></u></button>
            </div>
            <button
                hx-get="page4/content"
                hx-push-url="page4"
                hx-target="#register_new_listing"
                class="button"
            >Continue</button>
        </div>
    </main>
    """


@route("/new-listing/page4")
def new_listing_page4():
    return html("Register New Listing Page 4", with_navbar(new_listing_page4_content()))


@route("/new-listing/page4/content")
def new_listing_page4_content(summary=False):
    hidden_elems = ""
    if not summary:
        hidden_elems = """
        <div style="display: none">
            <textarea id="description" hx-preserve name="description" placeholder="Enter your description here"></textarea>
        </div>
        """
    return f"""
    <main id="register_new_listing">
        <div id="page4">
            <div class="maintext">
                    <h1>Where exactly is your home?</h1>
                    <br>
                    <br>
                    <p>
                        <label for="address">Address:</label>
                        <input id="address" hx-preserve type="text" name="address" class="line-input" required><br>
                        <label for="postalcode">Postal code:</label>
                        <input id="postalcode" hx-preserve type="text" name="postalcode" class="line-input" required>
                        <br>
                        <br>
                    </p>
            </div>
            <p class="page-counter"><b>4/5</b></p>
            <div class="back-button">
                <button><u><b>Back</b></u></button>
            </div>
            <button
                hx-get="page5/content"
                hx-push-url="page5"
                hx-target="#register_new_listing"
                class="button"
            >Continue</button>
            {hidden_elems}
        </div>
    </main>
    """


@route("/new-listing/page5")
def new_listing_page5():
    return html("Register New Listing Page 5", with_navbar(new_listing_page5_content()))


@route("/new-listing/page5/content")
def new_listing_page5_content(summary=False):
    hidden_elems = ""
    if not summary:
        hidden_elems = """
            <div style="display: none">
                <textarea id="description" hx-preserve name="description" placeholder="Enter your description here"></textarea>
                <input id="address" hx-preserve type="text" name="address" class="line-input" required>
                <input id="postalcode" hx-preserve type="text" name="postalcode" class="line-input" required>
            </div>
        """
    return f"""
    <main id="register_new_listing">
        <div id="page5">
            <div class="maintext">
                <div class="page5">
                    <h1>How much does it cost to rent your home <i>per</i> night?</h1>
                    <br>
                    <br>
                    <form oninput="outputNumber.value = price.value ? (parseFloat(price.value * 0.95).toFixed(2)) : ''">
                        <p>        
                            <label class="left" for="price">Enter price:</label>
                            <input type="text" hx-preserve id="price" name="price" maxlength="7" pattern="\d{1,7}" inputmode="numeric" required>
                            <span class="right">NOK per night</span>
                        </p>
                        <p>
                            <span class="middle">After the price of our services (5%), you're</span>
                        </p>
                        <p>
                            <span class="left">left with:</span>
                            <output id="outputNumber" name="outputNumber"> </output>
                            <span class="right">NOK per night</span>
                        </p>
                    </form>
                </div>
            </div>
            <button
                hx-get="summary/content"
                hx-push-url="summary"
                hx-target="#register_new_listing"
                class="button"
            >Continue</button>
            <p class="page-counter"><b>5/5</b></p>
            <div class="back-button">
                <button><u><b>Back</b></u></button>
            </div>
            {hidden_elems}
        </div>
    </main>
    """


@get("/new-listing/summary")
def new_listing_summary():
    return html(
        "Summary",
        with_navbar(new_listing_summary_content()),
    )


@route("/new-listing/summary/content")
def new_listing_summary_content():
    return f"""
        <main id="register_new_listing">
            <div id="summary" method="post">
                <div class="maintext">
                    <h1>Your summary!</h1>
                </div>
                {new_listing_page2_content()}
                {new_listing_page3_content()}
                {new_listing_page4_content(summary=True)}
                {new_listing_page5_content(summary=True)}
                <button
                    hx-post=""
                    hx-target="body"
                    hx-include="input,textarea"
                    >SUBMIT DAMMIT</button>
            </div>
        </main>
    """


@post("/new-listing/summary")
def new_listing_summary():
    return [
        request.forms["description"],
        request.forms["address"],
        request.forms["postalcode"],
        request.forms["price"],
    ]
