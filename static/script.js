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
