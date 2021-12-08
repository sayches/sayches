var mobileSearchIcon = document.querySelector(".mob-search img");
var searchClose = document.querySelector(".custom-search .custom-ex");
var searchInput = document.querySelector(".custom-search");
mobileSearchIcon.addEventListener("click", function () {
    on("open");
});
searchClose.addEventListener("click", function () {
    on("close");
});
function on(type) {
    if (type === "open") {
        searchInput.classList.add("d-flex");
    } else if (type === "close") {
        searchInput.classList.remove("d-flex");
    }
}