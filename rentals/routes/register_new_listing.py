from bottle import route, response, post, get, request

from ..components import html, with_navbar, image_input, image_input_carrier


@route("/new-listing")
def new_listing():
    response.status = 307
    response.add_header("Location", "/new-listing/page1")


def page_frame(content: str, n: int = None, prev: str = None, next: str = None) -> str:
    if prev == None and n > 1:
        prev = f"page{n - 1}"

    back_button = ""
    if prev != None:
        back_button = f"""
            <div class="back-button">
                <button
                    hx-get="{prev}/content"
                    hx-push-url="{prev}"
                    hx-target="#register_new_listing"
                ><u><b>Back</b></u></button>
            </div>
        """

    if n != None and next == None:
        next = f"page{n + 1}"

    next_button = ""
    if next != None:
        next_button = f"""
            <button
                hx-get="{next}/content"
                hx-push-url="{next}"
                hx-target="#register_new_listing"
                class="button"
            >Continue</button>
        """

    id = ""
    if n != None:
        id = f"page{n}"

    counter = ""
    carriers = ""
    if n != None:
        counter = f"""<p class="page-counter"><b>{n}/5</b></p>"""
        carriers = f"""
        <!-- These hidden inputs preserve the user's data across pages -->
        <div style="display: none">
            {n != 2 and image_input_carrier() or ""}
            {n != 3 and '<textarea id="description" hx-preserve name="description" placeholder="Enter your description here"></textarea>' or ""}
            {n != 4 and '<input id="address" hx-preserve type="text" name="address" class="line-input" required>' or ""}
            {n != 4 and '<input id="postalcode" hx-preserve type="text" name="postalcode" class="line-input" required>' or ""}
            {n != 5 and '<input type="text" hx-preserve id="price" name="price" required>' or ""}
        </div>
        """

    return f"""
    <main id="register_new_listing">
        <div id="{id}">
            {content}
            {counter}
            {back_button}
            {next_button}
        </div>
        {carriers}
    </main>
    """


@route("/new-listing/page1")
def new_listing_page1():
    return html(
        "Register New Listing Page 1",
        with_navbar(new_listing_page1_content_framed()),
    )


@route("/new-listing/page1/content")
def new_listing_page1_content_framed():
    return page_frame(
        """
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
        """,
        1,
    )


@route("/new-listing/page2")
def new_listing_page2():
    return html(
        "Register New Listing Page 2",
        with_navbar(new_listing_page2_content_framed()),
    )


@route("/new-listing/page2/content")
def new_listing_page2_content_framed():
    return page_frame(new_listing_page2_content(), 2)


def new_listing_page2_content():
    return f"""
    <div></div>
    <div class="maintext">
        <h1>Show us what your beautiful<br> home looks like!</h1>
    </div>
    <div class="image-upload-container">
        {image_input()}
    </div>
    """


@route("/new-listing/page3")
def new_listing_page3():
    return html(
        "Register New Listing Page 3",
        with_navbar(new_listing_page3_content_framed()),
    )


@route("/new-listing/page3/content")
def new_listing_page3_content_framed():
    return page_frame(
        f"""
        {new_listing_page3_content()}
        <div style="display: none">
            {image_input_carrier()}
        </div>
        """,
        3,
    )


def new_listing_page3_content():
    return """
        <div class="maintext">
            <h1>Enter a description of your home!</h1>
            <br><br>
            <p>Is it a peaceful retreat, a great place to gather with friends<br> or is it something truly unique?</p>
        </div>
        <div class="textarea">
            <textarea id="description" hx-preserve name="description" placeholder="Enter your description here"></textarea>
        </div>
    """


@route("/new-listing/page4")
def new_listing_page4():
    return html(
        "Register New Listing Page 4", with_navbar(new_listing_page4_content_framed())
    )


@route("/new-listing/page4/content")
def new_listing_page4_content_framed():
    return page_frame(
        f"""
        {new_listing_page4_content()}
        <div style="display: none">
            {image_input_carrier()}
            <textarea id="description" hx-preserve name="description" placeholder="Enter your description here"></textarea>
        </div>
        """,
        4,
    )


def new_listing_page4_content():
    return """
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
    """


@route("/new-listing/page5")
def new_listing_page5():
    return html(
        "Register New Listing Page 5", with_navbar(new_listing_page5_content_framed())
    )


@route("/new-listing/page5/content")
def new_listing_page5_content_framed():
    return page_frame(
        f"""
        {new_listing_page5_content()}
        """,
        5,
        next="summary",
    )


def new_listing_page5_content():
    return """
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
    """


@get("/new-listing/summary")
def new_listing_summary():
    return html(
        "Summary",
        with_navbar(new_listing_summary_content()),
    )


@route("/new-listing/summary/content")
def new_listing_summary_content():
    return page_frame(
        f"""
        <div id="summary" method="post">
            <div class="maintext">
                <h1>Your summary!</h1>
                {new_listing_page2_content()}
                <br>
                <br>
                <br>
                <br>
                <br>
                <hr style="width: 750px; margin-left: auto; margin-right: auto;">
                <br>
                {new_listing_page3_content()}
                <br>
                <br>
                <br>
                <br>
                <br>
                <hr style="width: 750px; margin-left: auto; margin-right: auto;">
                <br>
                {new_listing_page4_content()}
                <br>
                <br>
                <br>
                <br>
                <br>
                <hr style="width: 750px; margin-left: auto; margin-right: auto;">
                <br>
                <br>
                <br>
                <br>
                {new_listing_page5_content()}
            </div>
            <button
                hx-post=""
                hx-target="body"
                hx-include="input,textarea"
                hx-encoding="multipart/form-data"
                class="create-listing-button"
                >Create Listing</button>
        </div>
        """,
        prev="page5",
    )


@post("/new-listing/summary")
def new_listing_summary():
    for file in request.files.getall("image-files"):
        print(file)
        file.save("user-uploads")
    return "<br>".join(
        [
            request.forms["description"],
            request.forms["address"],
            request.forms["postalcode"],
            request.forms["price"],
        ]
    )
