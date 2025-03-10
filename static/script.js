function toggleDropdown(id) {
  let dropdown = document.getElementById(id);
  let allDropdowns = document.querySelectorAll(".dropdown");

  allDropdowns.forEach(box => {
    if (box.id !== id) {
      box.classList.remove("active");
    }
  });

  dropdown.classList.toggle("active");
}

function adjustDropdownPosition() {
  document.querySelectorAll(".input-box").forEach(box => {
    let dropdown = box.querySelector(".dropdown");
    if (dropdown) {
      let labelHeight = box.querySelector("label").offsetHeight;
      dropdown.style.top = labelHeight + "px";
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector("main#search-bar")) {
    window.onload = adjustDropdownPosition;
  }
});
