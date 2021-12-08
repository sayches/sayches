function pong(username) {
  const Url = "/u/ping-user/" + username
  $.ajax({
    url: Url,
    type: "POST",
    success: function (data) {
    },
    error: function (error) {
    }

  })
}

$('.noti-click').click(function(e){
  $.ajax({
      url: $('.notification_number_view').attr("href"),
      type: 'GET',
      success: function(){
          customNotificationEffect();
  }});
  function customNotificationEffect(){
      $('.noti-box .num-noti').text('0');
  }
});

function pong_user(id, obj) {
  const Url = pongUser.replace(9999,id)
  $.ajax({
    url: Url,
    type: "POST",
    success: function (data) {
      document.getElementById(obj.id).style.background ='black';
      document.getElementById(obj.id).style.color ='white';
    },
    error: function (error) {
    }

  })
}