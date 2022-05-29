$('input[type=radio][name=user_nickname]').change(function () {
  $.ajax({
    url: usersProfileNickname,
    type: 'POST',
    data:{'nickname':this.value},
    success: function () {
    }
  });

});

$('#user_nickname').change(function () {
  $.ajax({
    url: profileProfileNickname,
    type: 'POST',
    data:{'nickname':this.value},
    success: function () {
    }
  });
  });


$('.toggles').click(function(evt) {

  evt.preventDefault();

  var toggleId = this.id;
  var dataString={};

  dataString["toggleKey"]= toggleId;
  dataString[toggleId]= document.getElementById(toggleId).checked;
  $.ajax({
    url: usersProfileToggles,
    type: 'POST',
    data:dataString,
    success: function () {
      document.getElementById(toggleId).checked = dataString[toggleId];
    }
  });

});
