document.addEventListener("DOMContentLoaded", () => {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return; // Stopp skriptet hvis vi ikke er på søkesiden

  console.log("Søkesiden lastet, aktiverer søkefunksjoner...");

  window.onload = adjustDropdownPosition;
  loadDropdownData();

  let searchButton = searchBar.querySelector(".search-btn");
  if (searchButton) {
    searchButton.addEventListener("click", handleSearch);
  }
});

// 🔹 Funksjon for å vise/skjule dropdown-meny
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

// 🔹 Justerer posisjon for dropdown-menyer
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

// 🔹 Henter data fra backend og fyller dropdown-menyer
async function loadDropdownData() {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return;

  try {
    // 📍 Hent adresser ("Where")
    let locationResponse = await fetch("/get_locations");
    let locationData = await locationResponse.json();
    let locationBox = searchBar.querySelector("#location-box ul");

    if (locationBox) {
      locationBox.innerHTML = locationData.map(loc =>
        `<li onclick="selectOption('location-input', '${loc}')">${loc}</li>`
      ).join("");
    }

    // 📍 Hent datoer ("Check in" og "Check out")
    let dateResponse = await fetch("/get_dates");
    let dateData = await dateResponse.json();
    let checkinBox = searchBar.querySelector("#checkin-box");
    let checkoutBox = searchBar.querySelector("#checkout-box");

    if (checkinBox) {
      checkinBox.innerHTML = dateData.check_in.map(date =>
        `<li onclick="selectOption('checkin-input', '${date}')">${date}</li>`
      ).join("");
    }
    if (checkoutBox) {
      checkoutBox.innerHTML = dateData.check_out.map(date =>
        `<li onclick="selectOption('checkout-input', '${date}')">${date}</li>`
      ).join("");
    }

    // 📍 Hent antall gjester ("Who")
    let guestResponse = await fetch("/get_guests");
    let guestData = await guestResponse.json();
    let guestBox = searchBar.querySelector("#guests-box");

    if (guestBox) {
      guestBox.innerHTML = guestData.map(num =>
        `<li onclick="selectOption('guests-input', '${num} guests')">${num} guests</li>`
      ).join("");
    }
  } catch (error) {
    console.error("Feil ved henting av dropdown-data:", error);
  }
}

// 🔹 Velg en verdi fra dropdown
function selectOption(inputId, value) {
  let inputField = document.getElementById(inputId);
  if (inputField) {
    inputField.value = value;
  }
}

// 🔹 Håndterer søk når brukeren trykker på søkeknappen
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
