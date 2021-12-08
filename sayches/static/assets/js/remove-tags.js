const removeTag = document.querySelector(".removehtmltags");

removeTag.addEventListener("keydown", function(e) {
    if (e.which === 188 || e.which === 190) return false;
});

removeTag.addEventListener("change", function() {
    this.value = this.value.replaceAll("<", "");
    this.value = this.value.replaceAll(">", "");
});

function removeHtmlTags(obj) {
    obj.value = obj.value.replaceAll("<", "");
    obj.value = obj.value.replaceAll(">", "");
}