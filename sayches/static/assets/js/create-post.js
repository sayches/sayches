document.getElementById('media-upload').onchange = function () {
  var imgSrc = URL.createObjectURL(this.files[0])
  document.getElementById('media-image-image').src = imgSrc
}
const mediaFileBtn = document.getElementById("media-upload");
const mediaBtn = document.getElementById("media-upload-button");
const mediaImageThumbnail = document.getElementById("media-image-image");
mediaBtn.addEventListener("click", function () {
  mediaFileBtn.click();
});
mediaFileBtn.addEventListener("change", function () {
  if (mediaFileBtn.value) {
    mediaImageThumbnail.style.display = "block";
  } else {
    mediaImageThumbnail.style.display = "none";
  }
});