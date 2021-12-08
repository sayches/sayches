function reportAPost(event) {
  var form = $("#reportForm");
  $.ajax({
      url: '/report',
      type: 'POST',
      data: form.serialize(),
      success: function () {
          $('.option-popup-box').removeClass('d-flex')
          alert('Thanks for letting us know');
          location.reload();
      }
  });
  event.preventDefault();
  return false;
};