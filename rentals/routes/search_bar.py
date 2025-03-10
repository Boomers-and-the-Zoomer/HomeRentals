from bottle import route

from ..components import html, with_navbar


@route("/searchbar")
def search_bar():
    return html(
        "Searchbar",
        with_navbar("""
            <main id="search-bar">
                <div class="search-container">
                    <div class="input-box" onclick="toggleDropdown('location-box')">
                        <label>Where</label>
                        <input type="text" placeholder="search destination" readonly>
                        <div id="location-box" class="dropdown">
                            <ul>
                                <li>Hønefoss</li>
                                <li>Trondheim</li>
                                <li>Bergen</li>
                                <li>Hamar</li>
                                <li>Oslo</li>
                            </ul>
                        </div>
                    </div>
                    <div class="input-box" onclick="toggleDropdown('checkin-box')">
                        <label>Check in</label>
                        <input type="text" placeholder="Add dates" readonly>
                        <div id="checkin-box" class="dropdown">
                            <input type="date">
                        </div>
                    </div>
                    <div class="input-box" onclick="toggleDropdown('checkout-box')">
                        <label>Check out</label>
                        <input type="text" placeholder="Add dates" readonly>
                        <div id="checkout-box" class="dropdown">
                            <input type="date">
                        </div>
                    </div>
                    <div class="input-box" onclick="toggleDropdown('guests-box')">
                        <label>Who</label>
                        <input type="text" placeholder="Add guest" readonly>
                        <div id="guests-box" class="dropdown">
                            <p>Adults (13+ years): <button>-</button> 0 <button>+</button></p>
                            <p>Children (2-12 years): <button>-</button> 0 <button>+</button></p>
                            <p>Infant (Under 2 years): <button>-</button> 0 <button>+</button></p>
                            <p>Pet: <button>-</button> 0 <button>+</button></p>
                        </div>
                    </div>
                    <button class="search-btn">🔍 Søk</button>
                </div>
            </main>

       """),
    )
