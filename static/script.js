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

// =============== Image upload ===============

document.addEventListener("DOMContentLoaded", () => {
  // `from` is either the user-interactable input element, or the "carrier" input element
  function UpdateFilesFrom(from, move_to_carrier) {
    let parent = from.parentNode;
    const gallery = parent.querySelector(".image-upload-gallery");
    if (parent.my_files === undefined) {
      parent.my_files = new Map();
      parent.my_file_reader = new FileReader();
    }

    const total_files_allowed = 5;
    let total_files = parent.my_files.size;

    for (const file of Array.from(from.files)) {
      if (total_files == total_files_allowed) {
        console.error("Too many files");
        break;
      }
      total_files += 1;

      // Sadly, maps do not compare objects by value.
      const identity = `name: ${file.name}, size: ${file.size}, type=${file.type}`;
      if (!parent.my_files.has(identity)) {
        parent.my_files.set(identity, file);
      }
    }

    UpdateImageDisplay(parent, gallery, parent.my_files);

    if (move_to_carrier === true) {
      UpdateCarrierFiles(parent);
    }
  }

  function UpdateImageDisplayWithFile(parent, gallery, identity, file) {
    console.log(file);
    const url = URL.createObjectURL(file);
    const img = Array.from(gallery.children).map((elem) => {
      return elem.querySelector(".img");
    }).find((elem) => {
      return elem.src === undefined || elem.src === "";
    });
    img.src = url;
    img.addEventListener("click", HandleImageRemoval(parent, gallery, img, identity, parent.my_files));
  }

  function UpdateImageDisplay(parent, gallery, my_files) {
    for (
      let child_img of Array.from(gallery.children).map((child) => {
        return child.querySelector(".img");
      })
    ) {
      child_img.removeAttribute("src");
      child_img.removeEventListener("click", HandleImageRemoval);
    }

    UpdateCarrierFiles(parent);

    for ([identity, file] of my_files) {
      UpdateImageDisplayWithFile(parent, gallery, identity, file);
    }
  }

  function UpdateCarrierFiles(parent) {
    let carrier = document.getElementById("image-upload-carrier");
    let dtransfer = new DataTransfer();
    for (const file of parent.my_files.values()) {
      dtransfer.items.add(file);
    }
    carrier.files = dtransfer.files;
  }

  function HandleImageRemoval(parent, gallery, img, identity, my_files) {
    return () => {
      img.removeEventListener("click", HandleImageRemoval);
      my_files.delete(identity);
      UpdateImageDisplay(parent, gallery, my_files);
    };
  }

  function InitImageUpload() {
    // Initialization logic
    let containers = Array.from(document.querySelectorAll(".image-upload"));
    for (let container of containers) {
      let input = container.querySelector("#image-upload-input");
      if (input === null) {
        console.error("Invalid image upload component", container);
        return;
      }
      let carrier = container.querySelector("#image-upload-carrier");
      UpdateFilesFrom(carrier, false);
      input.addEventListener("change", (ev) => {
        const user_input = ev.target;
        UpdateFilesFrom(user_input, true);
        user_input.value = "";
      }, false);
    }
  }

  document.addEventListener("htmx:afterSettle", () => {
    InitImageUpload();
  });

  InitImageUpload();
});
