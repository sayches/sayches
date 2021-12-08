$('#profile_update_time').change(function () {
  $.ajax({
    url: profileProfileUpdateTime,
    type: 'POST',
    data:{'profile_update_time':this.value},
    success: function () {
    }
  });
});

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

$('#auto_account_delete').change(function () {
  $.ajax({
    url: usersAutoAccountDeleteTime,
    type: 'POST',
    data:{'auto_account_delete_time':this.value},
    success: function () {
    }
  });
});