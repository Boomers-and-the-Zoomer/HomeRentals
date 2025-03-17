document.addEventListener("DOMContentLoaded", () => {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return;

  console.log("Søkesiden lastet, aktiverer søkefunksjoner...");

  window.addEventListener("load", adjustDropdownPosition);

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
    let label = box.querySelector("label");
    if (label && dropdown) {
      let labelHeight = label.offsetHeight;
      dropdown.style.top = labelHeight + "px";
    }
  });
}

function selectOption(element, target, text) {
  let elem = document.getElementById(target);
  elem.value = text;
  let list_elem = element.parentNode;
  list_elem.parentNode.removeChild(list_elem);
}

function handleSearch() {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return;

  let locationInput = document.getElementById("location-input");
  let checkInInput = document.getElementById("checkin-input");
  let checkOutInput = document.getElementById("checkout-input");
  let guestsInput = document.getElementById("guests-input");
  let searchResults = document.getElementById("searchResults");

  if (!searchResults) {
    console.error("Elementet #searchResults finnes ikke.");
    return;
  }

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
    .then(response => {
      if (!response.ok) throw new Error("Feil ved henting av søkeresultater");
      return response.text();
    })
    .then(data => {
      searchResults.innerHTML = data;
    })
    .catch(error => {
      console.error("Feil ved henting av søkeresultater:", error);
      searchResults.innerHTML = "<p>En feil oppstod under søket.</p>";
    });
}
