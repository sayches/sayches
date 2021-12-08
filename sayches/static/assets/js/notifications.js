function markAllAsRead(e){
  $('.notification-dropdown .box-header .mark-p a').addClass('click');
  $.ajax({
          url: $('.mark_all_read_view').attr("href"),
          type: 'GET',
          success: function(){
              customNotificationEffect();
      }});
      function customNotificationEffect(){
        $('.noti-box .num-noti').text('0');

          $('.notification-dropdown .box-item').removeClass('custom-unread');
      }
}