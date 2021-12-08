$(function() {
$.ajax({
    cache:false,
    url: postDetail,
    success: function(data){
        $.getScript(STATIC_URL + 'assets/js/script-ajax.js', function(){
            getDetailsPost(data);
            customCall();
            loadReacton();
        }).done(function() {
            requestComment()
        });
}}).done(function(){
    $.getScript(STATIC_URL + 'assets/js/post.js');
});

function requestComment(){
    $.ajax({
        cache:false,
        url: commentsDetailForDetailPost,
        success: function(data){
            $('#comment-section').html(data);
        }}).done(function(){

    });
}
});

$("#deletePost").click(function(){
$('#deletePostForm').submit();
}
);
$(".li-unpinned").click(function(){

$('#pinPostForm').submit();

}
);