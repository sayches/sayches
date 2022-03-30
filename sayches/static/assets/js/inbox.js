function chatValidations(obj) {
  var chatText = $('#textarea-msg').val().trimStart();
  $('#textarea-msg').val(chatText);
  var content = ($('#textarea-msg').val()).length;
  var num_words = chatText.split(/\s+/g).length
  var max_limit=30;
  if (content > 500 || num_words>max_limit) {
      document.getElementById('textarea-box').style.boxShadow = 'rgb(237 25 95 / 10%) 1px 2px 5px 5px inset';
      $('#textarea-msg').removeClass('textareaMsg');
  }else{
      document.getElementById('textarea-box').style.boxShadow = 'inset 0px 4px 8px 2px rgb(88 108 138 / 10%)';
      $('#textarea-msg').addClass('textareaMsg');
  }
}

$(function() {
  $.ajax({
      url: messageChatData,
      type: "GET",
      success: function(data){
          $.getScript(STATIC_URL + 'assets/js/script-ajax.js', function(){
            var mate_user_dict;
           if ($('#chatUserFromProfile').attr('value')){
            urlMade = "/messages/user/json/" + $('#chatUserFromProfile').attr('value') + "/"
            $.getJSON(urlMade, function (userDict) {
              mate_user_dict = userDict;
              var exists = false;
              data.forEach(element => {
                if (element["mate_user_id"] == userDict["mate_user_id"]){
                exists = true;
                }
              });
            if (!exists){
              data.push(userDict)
            }
              getUsers(data);
              funChat();
              clickSpecificChat(mate_user_dict["mate_user_id"]);
            })
            }
             else{
              getUsers(data);
              funChat();
             }
          });
      }
});
});

function getUsers(data){
  function limitWords(str , limitNum , appendText){
      var res = str.split(' ');
      var output = '';
      var num ;
      if(res.length <= limitNum){
          num = res.length;
      }else{
          num = limitNum;
      }
      for (var i = 0; i < num; i++) {
          output += res[i] + ' ';
      }
      return output + appendText;
  }
$.each(data, function(i, f) {
  var nOfUnreadMsg;
  if(data[i].num_of_unread_msgs > 0){
      nOfUnreadMsg ='<sapn class="msg-counter">'+data[i].num_of_unread_msgs+'</sapn>';
  }else{
      nOfUnreadMsg = "";
  }
  var name_of_user= data[i].admin ? '<h3 class="heading msg-h">'+data[i].name+'</h3>' : '<a href="/u/'+ data[i].username +'"' +'><h3 class="heading msg-h">'+data[i].name+'</h3></a>'
  var single_user =
  '<div class="user-chat" chat-id="'+data[i].chat_id+'" mate-user-id="'+data[i].mate_user_id+'" admin-attr="'+data[i].admin+'">'+
      '<div class="chat-img">'+
          '<img src="'+data[i].user_img+'">'+
      '</div>'+
      '<div class="chat-text">'+
          '<div class="msg-heading">'+
              name_of_user +
              '<p class="parag msg-p">'+data[i].time_ago+'</p>'+
          '</div>'+
          '<div class="content-msg-counter">'+
          '<p class="parag msg-p">'+limitWords(data[i].last_msg , 5 , '...')+'</p class="parag msg-p">'+
          nOfUnreadMsg+
          '</div>'+
      '</div>'+
      '</div>'+
  '</div>';
  $(single_user).appendTo(".user-chat-box");
});
}

function funChat(){
  $('.user-chat').click(function(){
  $(this).find(".msg-counter").css({ display: "none" });
  var element = $(this);
  var admin_user = element.attr('admin-attr');
  var mate_user = element.attr('mate-user-id');
  $('.message-form-box').remove();
  $.ajax({
    url: "/messages/chat_header_data/",
    type: "GET",
    data: {mate_user_id: mate_user} ,
    success: function(data){
        $('.empty-box').hide();
        $('.chat-box').remove();
        getChatHeader(data);
        $('.user-chat').removeClass('custom-active');
        element.addClass('custom-active');
        $.getScript('assets/js/post.js');
        $("<p class='box-p chat-msg-window text-justify text-center'>🔒 Messages you send to this chat are ephemeral and protected by encryption. Enjoy the flow!</p>").insertAfter(".chat-heading");

  }});
  if(admin_user == 0){
      $.ajax({
      url: "/messages/chat_content_data/",
      data: { mate_user_id: mate_user } ,
      success: function(data){
          $('.main-chat').removeClass('custom-admin-chat');
              getChatContent(data);
              $('.main-chat').scrollTop($('.main-chat').prop('scrollHeight'));
              getChatForm(mate_user);
              msgFunc();
      }});
  }
  else{
      $.ajax({
          url: "/messages/ad_chat_content_data/",
          success: function(data){
              getChatContent(data);
              $('.main-chat').scrollTop($('.main-chat').prop('scrollHeight'));
      }});
  }
  scrollTime = setInterval(function(){
  }, 1000);

});

}

function getChatHeader(data){
  $.each(data, function(i, f) {
    var chat_delete_link = $('.delete_chat_view').attr("href").replace(/12345/, data[i].id.toString());
    var name_of_user= data[i].admin ? '<h4 class="heading name-h">'+data[i].name+'</h4>' : '<a href="/u/'+ data[i].username+'"' +'><h3 class="heading msg-h">'+data[i].name+'</h3></a>'
    var chatHeader =
    '<div class="chat-box" chat-id="'+data[i].id+'" mate_user_id="'+data[i].mate_user_id+'">'+
        '<div class="chat-heading">'+
            '<div class="first-box">'+
                '<div class="user-img">'+
                    '<img src="'+data[i].user_img+'">'+
                '</div>'+
              name_of_user +
            '</div>'+
            '<div class="sec-box">'+
                '<div class="option-list">'+
                    '<img src="assets/images/icons/svgIcons/close_100x100.svg" class="custom-ex">'+
                '</div>'+
            '</div>'+
        '</div>'+
        '<div class="main-chat custom-admin-chat">'+
          '</div>'+
    '</div>';
    $(chatHeader).appendTo(".single-chat");
});
}

function getChatContent(data){

  $.each(data, function(i, f) {
     if ( data[i].msg_p != ' '){
      if ( data[i].msg_type == 'send'){
          var chatContent = '<div class="custom-send box-msg">';
      }else{
          var chatContent = '<div class="custom-receive box-msg">';
      }

      chatContent +=
          '<p class="parag msg-p">'+data[i].msg_p+'</p>';
          chatContent +=
          '<p class="custom-time">'+data[i].msg_time+'</p>'+
      '</div>' ;
      $(chatContent).appendTo(".main-chat");
    }
  });
}

function getChatForm(mate_user_id){
  var chatForm = '<div class="message-form-box">'+
      '<form action="" class="message-form">'+
          '<div class="textarea-box" id="textarea-box" title="Be yourself in every message.">'+
              '<textarea id="textarea-msg" name="textarea-msg" onkeyup="chatValidations(this)" mate-user-id="'+ mate_user_id +'" class="textarea-msg reply-textarea textareaMsg"  placeholder="Start new message"></textarea>'+
              '<input data-upload="msg-file" type="file" id="replay-img" class="replay-img" hidden>'+
          '</div>'+
      '</form>'+
  '</div>';
  $(chatForm).appendTo(".chat-content");
}

function msgFunc(){
  var wordLen = 50,
  len;
  $('.textareaMsg').keypress(function (e) {


      if (e.which == 13) {
          if(!($('#textarea-msg').hasClass('textareaMsg'))){
              $('#textarea-msg').val(($('#textarea-msg').val()).replace(/\r?\n|\r/g, ""));
              return
          }
          e.preventDefault();
          var msg_content = $(this).val();
          var msg_p = msg_content.trim();
          if(msg_p.length > 0){
              var mate_user = $(this).attr('mate-user-id');
              $.ajax({
                  url: "/messages/create_message/",
                  type: "POST",
                  data: { mate_user_id : mate_user , msg_content: msg_p } ,
                  success: function(data){
                      $('.textarea-msg').val('');
                      var dt = new Date();
                      var h =  dt.getHours(), m = dt.getMinutes();
                      var _time = (h > 12) ? (h-12 + ':' + m +' PM') : (h + ':' + m +' AM');
                      var data = [{msg_p, msg_time: _time, msg_type: "send"}]
                      getChatContent(data);
                  }
              });
          }
      }


      len = $(this).val().split(/[\s]+/);
      if (len.length > wordLen) {
          if (event.keyCode < 48 || event.keyCode > 57  ) {
              event.preventDefault();
          }
      }

  });
  $('.textarea-msg').on("paste",function(event){

          var clipboarddata =  event.clipboardData ||window.clipboardData || event.originalEvent.clipboardData;
          var onlytext = clipboarddata.getData('text/plain');
          var len_past = onlytext.split(/[\s]+/);
          if (len_past.length +  len.length > wordLen) {
              event.preventDefault();
              for (var i = 0; i <= (wordLen - len.length) ; i++) {
                  $(this).val( $(this).val() + len_past[i] + ' ');
              }
      }
      });

}

function clickSpecificChat(mate_user_id){
  $('.user-chat').each(function() {
      if ($(this).attr('mate-user-id') == mate_user_id){
          $(this).click();
      }
    });

}

var $input = $('#search-chat');
$input.on('keyup', function () {
    var searchField = $("#search-chat").val();
    $.ajax({
      url: "/messages/search-users-and-chats/",
      data: { key: searchField } ,
        success: function(data){
            $("#box-msg").html('');
            doneTyping(data);
        }
    });
});

function limitWords(str , limitNum , appendText){
  var res = str.split(' ');
  var output = '';
  var num ;
  if(res.length <= limitNum){
      num = res.length;
  }else{
      num = limitNum;
  }
  for (var i = 0; i < num; i++) {
      output += res[i] + ' ';
  }
  return output + appendText;
}

function doneTyping (data) {
  var searchField = $("#search-chat").val();
  var expression = new RegExp(searchField, "i");
  $.each(data, function (i) {
      if (
          data[i].name.search(expression) != -1 && searchField != ''
      ) {
          var nOfUnreadMsg;
          if(data[i].num_of_unread_msgs > 0){
              nOfUnreadMsg ='<sapn class="msg-counter">'+data[i].num_of_unread_msgs+'</sapn>';
          }else{
              nOfUnreadMsg = "";
          }
          var name_of_user= data[i].admin ? '<h3 class="heading msg-h">'+data[i].name+'</h3>' : '<a href="/u/'+ data[i].username +'"'  + '><h3 class="heading msg-h">'+data[i].name+'</h3></a>'
          var single_user =
          '<div class="user-chat" chat-id="'+data[i].chat_id+'" mate-user-id="'+data[i].mate_user_id+'" admin-attr="'+data[i].admin+'">'+
              '<div class="chat-img">'+
                  '<img src="'+data[i].user_img+'">'+
              '</div>'+
              '<div class="chat-text">'+
                  '<div class="msg-heading">'+
                      name_of_user +
                      '<p class="parag msg-p">'+data[i].time_ago+'</p>'+
                  '</div>'+
                  '<div class="content-msg-counter">'+
                  '<p class="parag msg-p">'+limitWords(data[i].last_msg , 5 , '...')+'</p class="parag msg-p">'+
                  nOfUnreadMsg+
                  '</div>'+
              '</div>'+
              '</div>'+
          '</div>';
          $(single_user).appendTo(".user-chat-box");
      }
      });
      funChat();
}