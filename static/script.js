document.addEventListener("DOMContentLoaded", () => {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return;

  console.log("Søkesiden lastet, aktiverer søkefunksjoner...");

  window.onload = adjustDropdownPosition;
  loadDropdownData();

  let searchButton = searchBar.querySelector(".search-btn");
  if (searchButton) {
    searchButton.addEventListener("click", handleSearch);
  }
});

function toggleDropdown(id) {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return;

  let dropdown = searchBar.querySelector(`#${id}`);
  let allDropdowns = searchBar.querySelectorAll(".dropdown");

  allDropdowns.forEach(box => {
    if (box.id !== id) {
      box.classList.remove("active");
    }
  });

  if (dropdown) {
    dropdown.classList.toggle("active");
  }
}

function adjustDropdownPosition() {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return;

  searchBar.querySelectorAll(".input-box").forEach(box => {
    let dropdown = box.querySelector(".dropdown");
    if (dropdown) {
      let labelHeight = box.querySelector("label").offsetHeight;
      dropdown.style.top = labelHeight + "px";
    }
  });
}

async function loadDropdownData() {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return;

  try {
    let locationResponse = await fetch("/get_locations");
    let locationData = await locationResponse.json();
    let locationBox = searchBar.querySelector("#location-box ul");
    let locationInput = document.getElementById("location-input");

    if (locationBox) {
      locationBox.innerHTML = locationData.map(loc => `<li data-value="${loc}">${loc}</li>`).join("");
    }

    let dateResponse = await fetch("/get_dates");
    let dateData = await dateResponse.json();
    let checkinBox = searchBar.querySelector("#checkin-box ul");
    let checkoutBox = searchBar.querySelector("#checkout-box ul");
    let checkinInput = document.getElementById("checkin-input");
    let checkoutInput = document.getElementById("checkout-input");

    if (checkinBox) {
      checkinBox.innerHTML = dateData.check_in.map(date => `<li data-value="${date}">${date}</li>`).join("");
    }
    if (checkoutBox) {
      checkoutBox.innerHTML = dateData.check_out.map(date => `<li data-value="${date}">${date}</li>`).join("");
    }

    let guestResponse = await fetch("/get_guests");
    let guestData = await guestResponse.json();
    let guestBox = searchBar.querySelector("#guests-box ul");
    let guestsInput = document.getElementById("guests-input");

    if (guestBox) {
      guestBox.innerHTML = guestData.guests.map(num => `<li data-value="${num} guests">${num} guests</li>`).join("");
    }

    document.querySelectorAll(".dropdown li").forEach(item => {
      item.addEventListener("click", function() {
        let inputBox = this.closest(".input-box").querySelector("input");
        if (inputBox) {
          inputBox.value = this.dataset.value;
        }
        this.closest(".dropdown").classList.remove("active");
      });
    });
  } catch (error) {
    console.error("Feil ved henting av dropdown-data:", error);
  }
}

function handleSearch() {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return;

  let locationInput = document.getElementById("location-input");
  let checkInInput = document.getElementById("checkin-input");
  let checkOutInput = document.getElementById("checkout-input");
  let guestsInput = document.getElementById("guests-input");
  let searchResults = document.getElementById("searchResults");

  let location = locationInput ? locationInput.value.trim() : "";
  let checkIn = checkInInput ? checkInInput.value.trim() : "";
  let checkOut = checkOutInput ? checkOutInput.value.trim() : "";
  let guests = guestsInput ? guestsInput.value.trim() : "";

  if (!location || !checkIn || !checkOut || !guests) {
    alert("Vennligst fyll ut alle feltene før du søker.");
    return;
  }

  fetch(
    `/search_results?location=${
      encodeURIComponent(location)
    }&check_in=${checkIn}&check_out=${checkOut}&guests=${guests}`,
  )
    .then(response => response.text())
    .then(data => {
      searchResults.innerHTML = data;
    })
    .catch(error => console.error("Feil ved henting av søkeresultater:", error));
}
