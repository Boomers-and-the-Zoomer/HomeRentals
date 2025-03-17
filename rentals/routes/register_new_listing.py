from bottle import route

from ..components import html, with_navbar


@route("/new-listing/page1")
def new_listing():
    return html(
        "Register New Listing Page 1",
        with_navbar("""
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
        """),
    )


@route("/new-listing/page2")
def new_listing_page2():
    return html(
        "Register New Listing Page 2",
        with_navbar("""
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
    """),
    )


@route("/new-listing/page3")
def new_listing_page3():
    return html(
        "Register New Listing Page 3",
        with_navbar("""
        <main id="register_new_listing">
            <div id="page3">
                <div class="maintext">
                    <h1>Enter a description of your home!</h1>
                    <br><br>
                    <p>Is it a peaceful retreat, a great place to gather with friends<br> or is it something truly unique?</p>
                 </div>
                <div class="textarea">
                    <textarea placeholder="Enter your description here"></textarea>
                </div>
                <p class="page-counter"><b>3/5</b></p>
                <div class="back-button">
                    <button><u><b>Back</b></u></button>
                </div>
                <button class="button">Continue</button>
            </div>
        </main>
    """),
    )


@route("/new-listing/page4")
def new_listing_page4():
    return html(
        "Register New Listing Page 4",
        with_navbar("""
        <main id="register_new_listing">
            <div id="page4">
                <div class="maintext">
                        <h1>Where exactly is your home?</h1>
                        <br>
                        <br>
                        <p>
                            <label for="address">Address:</label>
                            <input id="address" type="text" name="address" class="line-input" required><br>
                            <label for="postalcode">Postal code:</label>
                            <input id="postalcode" type="text" name="postalcode" class="line-input" required>
                            <br>
                            <br>
                        </p>
                </div>
                <p class="page-counter"><b>4/5</b></p>
                <div class="back-button">
                    <button><u><b>Back</b></u></button>
                </div>
                <button class="button">Continue</button>
            </div>
        </main>
    """),
    )


@route("/new-listing/page5")
def new_listing_page5():
    return html(
        "Register New Listing Page 5",
        with_navbar("""
        <main id="register_new_listing">
            <div id="page5">
                <div class="maintext">
                    <div class="page5">
                        <h1>How much does it cost to rent your home <i>per</i> night?</h1>
                        <br>
                        <br>
                        <form oninput="outputNumber.value = inputNumber.value ? (parseFloat(inputNumber.value * 0.95).toFixed(2)) : ''">
                            <p>        
                                <label class="left" for="inputNumber">Enter price:</label>
                                <input type="text" id="inputNumber" name="inputNumber" maxlength="7" pattern="\d{1,7}" inputmode="numeric" required>
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
                <button class="button">Continue to summary</button>
                <p class="page-counter"><b>5/5</b></p>
                <div class="back-button">
                    <button><u><b>Back</b></u></button>
                </div>
            </div>
        </main>
    """),
    )


@route("/new-listing/summary")
def new_listing_summary():
    return html(
        "Summary",
        with_navbar("""
        <main id="register_new_listing">
            <div id="summary">
                <div class="maintext">
                    <h1>Your summary<br> home looks like!</h1>
                </div>
            </div>
        </main>
    """),
    )
