$('.post-btn').attr('disabled', true);

function checklenghtAndChangeColor(content){
    var con = (content.value).trimStart()
    $(`#${content.id}`).val((content.value).trimStart());
    var num_Word = con.split(/\s+/g).length
    var max_lenght = 30;
    if (con.length<1 ||  con.length > 700 || num_Word >max_lenght){
        $('#reply-btn').removeClass('focus-btn');
        $('#reply-btn').attr('disabled', true);
    }else{
        $('#reply-btn').addClass('focus-btn');
        $('#reply-btn').attr('disabled', false);
    }
}

$('.reply-textarea').on("keydown", function(e){
    if (e.shiftKey && (e.which == 188 || e.which == 190)) {
        e.preventDefault();
    }
});

$('#reply-area').on('focus', function (e) {
$('#reply-btn').addClass('focus-btn').attr('disabled', false);
})


function requestCommentInner() {
$.ajax({
    url: commentsDetailForDetailPost + "?inner-section=true",
    success: function (data) {
    $('#comment-sec').html(data);
    }
}).done(function () {

});
}

$(".reply-textarea").bind("paste", function(e){
maxLengthCheck()
})

$(document).ready(function(){
    maxLengthCheck()
});

function maxLengthCheck() {
var content = $('.reply-textarea').val();
var num_words = content.split(" ").length
var max_limit=30;
if(num_words>max_limit){
    $('.reply-textarea').val(content.split(" ",30).join(" "));

    $('#remainingChars').text('0');
    return false;
}
else
{
$('#remainingChars').text(max_limit+1-num_words);
return true
}
}


$('.ReplyForm-comment').on('submit', function (e) {
e.preventDefault()
$.ajax({
    url: createComment,
    type: 'POST',
    data: $(this).serialize(),
    success: function (data) {
    nextPage = true;
    loadComments(1);
    $('#reply-area').val('')
    $('.ReplyForm-comment').find('.post-btn').removeClass('focus-btn').attr('disabled', true);
    }
});
})

$( "#reply-area" ).focus(function() {
    if($('#reply-area').val() == ''){
        $('.ReplyForm-comment').find('.post-btn').removeClass('focus-btn').attr('disabled', true);
    }
  });

let page = 1;
var nextPage = true, stopSendingRequest = false;

function loadComments(page_number=1) {
    if (nextPage) {

        $.ajax({
            url: commentsDetailForDetailPost + "?inner-section=true&page=" + page_number,
            success: function (data) {
            if (page_number == 1) {
                $('#comment-sec').empty();
            }
            $('#comment-sec').append(data);
            if (data.length < 10) {
                nextPage = false;
            }
            }
        }).done(function () {
            stopSendingRequest = false;
        });
    }
}

$(window).bind('scroll', function(e) {
    if(!stopSendingRequest && $(window).scrollTop() >= $('#comment-sec').offset().top + $('#comment-sec').outerHeight() - window.innerHeight) {
    page = page + 1;
    stopSendingRequest = true;
    loadComments(page);
    }
});


function replyUser(e){
$('#reply-area').val(e+' ');
$('.up-btn').click()
}

$('.delete-click').on('click', function (e) {
var commentId = $(this).attr('id')

$.ajax({
    url: deleteComment,
    type: 'POST',
    data: {"comment_id": commentId},
    success: function (data) {
    loadComments()
    }
});
})