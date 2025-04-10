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
  setupPopover("button[popovertarget=\"search-popover\"]", "#search-popover");
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

document.addEventListener("DOMContentLoaded", function() {
  const select = document.getElementById("sort_by");

  function updateSortIcon(value) {
    if (!icon) return;
    if (value.endsWith("_asc")) {
      icon.textContent = "↑";
    } else if (value.endsWith("_desc")) {
      icon.textContent = "↓";
    } else {
      icon.textContent = "↕";
    }
  }

  if (select) {
    updateSortIcon(select.value);

    select.addEventListener("change", function() {
      updateSortIcon(this.value);
    });
  }
});

document.body.addEventListener("htmx:afterSwap", (e) => {
  if (e.target.id === "search-bar") {
    const popoverButton = document.querySelector("[popovertarget=\"search-popover\"]");
    const popover = document.querySelector("#search-popover");

    if (popoverButton && popover && popover.matches(":popover-open")) {
      popover.hidePopover(); // Lukker midlertidig
      popover.showPopover(); // Åpner igjen for å få riktig CSS
    }
  }
});
document.querySelector("#sort_by")?.addEventListener("change", () => {
  const selected = document.querySelector("#sort_by").value;
  const iconButton = document.querySelector(".icon-button svg");

  if (!iconButton) return;

  // Bytt ut SVG basert på sortering
  if (selected.endsWith("asc")) {
    iconButton.innerHTML = `<path d="M4 6h16M4 12h8m-8 6h4" stroke="currentColor" stroke-width="2" fill="none"/>`; // eksempel
  } else if (selected.endsWith("desc")) {
    iconButton.innerHTML = `<path d="M4 6h4m-4 6h8m-8 6h16" stroke="currentColor" stroke-width="2" fill="none"/>`; // eksempel
  } else {
    iconButton.innerHTML = `<path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2" fill="none"/>`; // fallback
  }
});
