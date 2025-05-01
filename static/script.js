document.addEventListener("DOMContentLoaded", () => {
  if (!document.getElementById("search-page")) {
    return;
  }
  function setupPopover(btn_selector, popover_selector) {
    const toggle_btn = document.querySelector(btn_selector);
    const popover = document.querySelector(popover_selector);
    const updatePopoverPosition = () => {
      const btn_rect = toggle_btn.getBoundingClientRect();
      popover.style.top = `${btn_rect.bottom + 10}px`;
      popover.style.right = `${window.innerWidth - btn_rect.right}px`;
    };
    popover.addEventListener("beforetoggle", (event) => {
      if (event.newState === "open") {
        updatePopoverPosition();
      }
    });
    document.addEventListener("scroll", () => {
      /* Throttle scroll event handling */
      window.requestAnimationFrame(() => {
        updatePopoverPosition();
      });
    });
    window.addEventListener("resize", () => {
      updatePopoverPosition();
    });
  }
  setupPopover("button[popovertarget=\"sort-popover\"]", "#sort-popover");
  setupPopover("button[popovertarget=\"filter-popover\"]", "#filter-popover");
});

// ======== Payment options =========

document.addEventListener("DOMContentLoaded", () => {
  if (!document.querySelector("main#payment")) {
    return;
  }
  const vipps_info = document.querySelector(".vipps_info");
  const card_info = document.querySelector(".visa_info");
  const no_info = document.querySelector(".no_info");
  const parent = vipps_info.parentElement;
  parent.removeChild(vipps_info);
  parent.removeChild(card_info);

  const btn = document.querySelector(".submit-btn");
  btn.disabled = true;

  Array.from(
    document.querySelectorAll("input[name=\"payment\"]"),
  ).forEach((radio, _i, _a) => {
    if (radio.checked) {
      if (radio.getAttribute("value") == "vipps") {
        Array.from(parent.children)[1].insertAdjacentElement("afterend", vipps_info);
      } else {
        Array.from(parent.children)[1].insertAdjacentElement("afterend", card_info);
      }
    }
    // Only fires when the element is selected.
    radio.addEventListener("change", () => {
      if (btn.disabled) {
        parent.removeChild(no_info);
        btn.disabled = false;
      }
      if (radio.getAttribute("value") == "vipps") {
        Array.from(parent.children)[1].insertAdjacentElement("afterend", vipps_info);
        if (card_info.parentElement) {
          parent.removeChild(card_info);
        }
      } else {
        Array.from(parent.children)[1].insertAdjacentElement("afterend", card_info);
        if (vipps_info.parentElement) {
          parent.removeChild(vipps_info);
        }
      }
    });
  });
});

// ======== Profile page image upload =========

document.addEventListener("DOMContentLoaded", () => {
  if (!document.querySelector("#user-profile > .user_profile_edit")) {
    return;
  }
  const img = document.querySelector("img.profile_picture");
  const file_upload = document.querySelector("input[type=\"file\"]#picture_form");
  file_upload.addEventListener("change", () => {
    const file = file_upload.files[0];
    const url = URL.createObjectURL(file);
    img.src = url;
  });
});

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
    return (event) => {
      img.removeEventListener("click", HandleImageRemoval);
      my_files.delete(identity);
      UpdateImageDisplay(parent, gallery, my_files);
      event.stopImmediatePropogation();
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

      for (let img of Array.from(container.querySelectorAll(".img"))) {
        img.addEventListener("click", (e) => {
          input.showPicker();
        });
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

document.addEventListener("DOMContentLoaded", function() {
  // Gjelder bare på søkesiden
  if (!document.querySelector("#search-page")) return;

  const checkInInput = document.getElementById("checkin-input");
  const checkOutInput = document.getElementById("checkout-input");

  if (!checkInInput || !checkOutInput) return;

  checkInInput.addEventListener("change", function() {
    if (!checkInInput.value) return;

    const checkInDate = new Date(checkInInput.value);
    const currentCheckOut = new Date(checkOutInput.value);

    const nextDay = new Date(checkInDate);
    nextDay.setDate(checkInDate.getDate() + 1);

    if (!checkOutInput.value || currentCheckOut <= checkInDate) {
      checkOutInput.value = nextDay.toISOString().split("T")[0];

      checkOutInput.dispatchEvent(new Event("change"));
    }

    checkOutInput.min = nextDay.toISOString().split("T")[0];
  });
});

document.addEventListener("DOMContentLoaded", function() {
  if (!document.querySelector("#search-page")) return;

  document.querySelectorAll(".input-box").forEach(box => {
    const input = box.querySelector("input[type='date']");
    if (input && typeof input.showPicker === "function") {
      box.addEventListener("click", () => {
        input.showPicker();
      });
    }
  });
});

// =============== Active bookings ===============
function confirmCancellation() {
  return confirm("Are you sure you want to cancel this booking?");
}
