$('.main-react').hover(function () {
    if ($(this).attr("reaction_status") == "action") {
        $(this).find('.reaction-box').addClass('d-flex');
        $(this).find('.reaction-box img').addClass('img-animation');
    }
    }, function() {
    $(this).find('.reaction-box').removeClass('d-flex');
    });
$('.box-reaction').click(function(){
    $(this).parents('.reaction-box').removeClass('d-flex');
});

$('.main-react').click(function () {
    if ($(this).attr("reaction_status") == "action"){
        if (!$('.reaction-box').hasClass('d-flex')){
            $(this).find('.reaction-box').addClass('d-flex');
            $(this).find('.reaction-box img').addClass('img-animation');
        }else if ($('.reaction-box').hasClass('d-flex')){
            $('.reaction-box').removeClass('d-flex');
        }
    }
});
