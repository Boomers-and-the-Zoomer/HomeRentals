document.addEventListener("DOMContentLoaded", () => {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return;

  console.log("Søkesiden lastet, aktiverer søkefunksjoner...");

  window.addEventListener("load", adjustDropdownPosition);
});

function setGuestEventListeners() {
  let adultCount = document.getElementById("adult-count");
  let childrenCount = document.getElementById("children-count");

  let increaseAdults = document.getElementById("increase-adults");
  let decreaseAdults = document.getElementById("decrease-adults");

  let increaseChildren = document.getElementById("increase-children");
  let decreaseChildren = document.getElementById("decrease-children");

  if (increaseAdults && decreaseAdults && adultCount) {
    let adultGuests = 0;
    let childGuests = 0;

    increaseAdults.addEventListener("click", () => {
      adultGuests++;
      adultCount.innerText = adultGuests;
      adultCount.value = adultGuests;
      adultCount.setAttribute("value", adultGuests);
    });

    decreaseAdults.addEventListener("click", () => {
      if (adultGuests > 0) {
        adultGuests--;
        adultCount.innerText = adultGuests;
        adultCount.value = adultGuests;
        adultCount.setAttribute("value", adultGuests);
      }
    });

    increaseChildren.addEventListener("click", () => {
      childGuests++;
      childrenCount.innerText = childGuests;
      childrenCount.setAttribute("value", childGuests);
    });

    decreaseChildren.addEventListener("click", () => {
      if (childGuests > 0) {
        childGuests--;
        childrenCount.innerText = childGuests;
        childrenCount.setAttribute("value", childGuests);
      }
    });
  }
}

function updateGuestsInput(adults, children) {
  let guestsInput = document.getElementById("guests-input");
  if (guestsInput) {
    guestsInput.value = `${adults} Adults, ${children} Children`;
    guestsInput.setAttribute("value", guestsInput.value);
  }
}

function toggleDropdown(id) {
  let searchBar = document.querySelector("main#search-bar");
  if (!searchBar) return;

  let dropdown = searchBar.querySelector(`#${id}`);
  let allDropdowns = searchBar.querySelectorAll(".dropdown");

  allDropdowns.forEach(box => {
    if (box.id !== dropdown) {
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
  let inputField = document.getElementById(target);
  if (inputField) {
    inputField.value = text;
    inputField.setAttribute("value", text);
  }

  let dropdownItem = element.closest(".dropdown");
  if (dropdownItem) {
    dropdownItem.style.display = "none";
  }

  console.log(`Valgt: ${text} for ${target}`);
}

function loadGuests() {
  fetch("/get_guests")
    .then(response => response.text())
    .then(data => {
      let guestsBox = document.getElementById("guests-box");
      if (guestsBox) {
        guestsBox.innerHTML = data;
        setGuestEventListeners();
      }
    })
    .catch(error => console.error("Feil ved lasting av guests:", error));
}
