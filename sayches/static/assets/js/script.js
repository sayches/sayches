$(document).ready(function(){
    var requiredText = '@';
    $('.custom-at').on('input', function() {
    if (String($(this).val()).indexOf(requiredText) == -1) {
        var sec_text = requiredText + '' + $(this).val();
        $(this).val(sec_text);
    }
    });

    var hashtag_limit = 4;
    $('.hashtag-input').keydown(function(e) {
        if(e.which == 32){
            e.preventDefault();
        }
        else if($(this).val().length == 0){
            if ((e.shiftKey == true && e.which == 51) || ( e.ctrlKey == true && e.which == 86 )){
            }else{
                e.preventDefault();
            }
        }else{
            var hash_arr = $(this).val().split('#');
            if((e.shiftKey == true && e.which == 51)){
                if(hash_arr.length > hashtag_limit){
                    e.preventDefault();
                }
            }
        }
    });
    $('.hashtag-input').on("paste",function(event){

        var clipboarddata =  event.clipboardData ||window.clipboardData || event.originalEvent.clipboardData;
        var onlytext = clipboarddata.getData('text/plain');
        var len_past = onlytext.substring(1).split('#');
        var hash_arr = $(this).val().split('#');
        if(onlytext.startsWith("#") === false){
            event.preventDefault();
        }
        else if (len_past.length +  hash_arr.length > hashtag_limit) {
            event.preventDefault();
            for (var i = 0; i <= (hashtag_limit - hash_arr.length) ; i++) {
                $(this).val( $(this).val() +'#'+ len_past[i]);
            }
        }
    });

    $(".toggle-password").click(function() {
        $(this).toggleClass("fa-eye fa-eye-slash");
        var input = $($(this).attr("toggle"));
        if (input.attr("type") == "password") {
          input.attr("type", "text");
        } else {
          input.attr("type", "password");
        }
    });

    $('#multi-form').smartWizard({
        selected: 0,
        useURLhash: false,
        transitionEffect: 'fade',
        toolbarSettings: {
            showPreviousButton: false,
        }
    });

     $('.nav.nav-tabs.step-anchor , .sw-container.tab-content').wrapAll('<div class="parent-form"></div>');
    $('.default-select').select2({ minimumResultsForSearch: -1 });

    $(".img-code").select2({
        templateResult: formatState,
        templateSelection: function (data, container) {
            $(data.element).attr('data-custom-attribute', data.customValue);
            return data.text;
        }
    });

    function formatState (state) {
        if (!state.id) { return state.text; }
        if(state.element.value == 'none'){
        }else{
            var $state = $(
            '<span ><img class="imgFlag" sytle="display: inline-block;" src="'+ STATIC_URL+'assets/images/flags/'+ state.element.value.toLowerCase() +'.png" /> ' + state.text + '</span>'
            );
            return $state;
        }
    }
    $('.img-code').each(function(){
        if($(this).find('option:selected').val() == ""){

        }else{
            $(this).siblings(".select2-container").find(".select2-selection--single").prepend("<img class='imgFlag' src='"+ STATIC_URL+"assets/images/flags/"+ $(this).find('option:selected').val().toLowerCase() +".png'/>");
        }
    });
    $(".img-code").change(function() {
        if($(this).find('option:selected').val() == ""){
            $(this).siblings(".select2-container").find('.imgFlag').css({"display":"none"})
        }
        else 
        {
            if($(this).siblings(".select2-container").find('.imgFlag').length){
            $(this).siblings(".select2-container").find('.imgFlag').attr('src' ,STATIC_URL+'assets/images/flags/'+ $(this).find('option:selected').val().toLowerCase() +'.png');
        }
        else{
            $(this).siblings(".select2-container").find(".select2-selection--single").prepend("<img class='imgFlag' src='"+ STATIC_URL+"assets/images/flags/"+ $(this).find('option:selected').val().toLowerCase() +".png'/>");
        }
    }
    });

    $('.select2-selection__arrow').html('<i class="ri-arrow-down-s-line font-weight-bold primary-colour"></i>');

    $(".profile-image , .edit-pro-img").click(function(e) {
        $(".custom-upload").click();
    });

    function fasterPreview( uploader ) {
        if ( uploader.files && uploader.files[0] ){
              $('.profile-image , .edit-pro-img').attr('src',
                 window.URL.createObjectURL(uploader.files[0]) );
        }
    }

    $(".custom-upload").change(function(){
        fasterPreview( this );
    });

    $(window).load(function(){
        $(".multi-form-content").addClass('custom-opacity');
    });

    $('.more-option').click(function(){
        $(this).parents('.option-box').toggleClass('custom-hide');
        $(this).toggleClass('custom-open');
    });

    $(document).click(function(e){
        if( $(e.target).closest('.postForm-box , .option-popup-box').length > 0 ) {
        }
        else{
            $('.option-box').addClass('custom-hide');
            $('.more-option').removeClass('custom-open');
        }

    });

    $('.option-p').click(function(){
        var conn = $(this).attr('data-toggle');
        $('.option-popup-box[data-id='+conn+']').addClass('d-flex');
    });
    $('.option-popup-box .popup-exit').click(function(){
        $(this).parents('.option-popup-box').removeClass('d-flex');
    });

    $(document).click(function(e){
        if( $(e.target).closest('.newPost , .option-popup-box').length > 0 ) {
            var conn = $(e.target).parents('.newPost').attr('data-form');
            $('.main-type-box[data-conn='+conn+']').addClass('d-flex');
            $('.option-box[data-conn='+conn+']').show();

        }else{
            $('.main-type-box').removeClass('d-flex');
            $('.option-box').hide();
        }
    });

    $('.post-btn').attr('disabled', true);
    $('.postInput').on('keyup',function() {

        var textarea_value = $(this).val();
        var textarea_p = textarea_value.trim();

        if(textarea_p != '') {
            $('.post-btn[data-id='+$(this).attr('data-attr')+']').attr('disabled', false);
            $('.custom-counter[data-count='+$(this).attr('data-attr')+']').css('display', 'inline-block');
            $('.post-btn[data-id='+$(this).attr('data-attr')+']').addClass('focus-btn');
        } else {
            $('.post-btn[data-id='+$(this).attr('data-attr')+']').attr('disabled', true);
            $('.custom-counter[data-count='+$(this).attr('data-attr')+']').css('display', 'none');
            $('.post-btn[data-id='+$(this).attr('data-attr')+']').removeClass('focus-btn');
        }
    });

    $(document).click(function(e){
        if( $(e.target).closest('.noti-click').length > 0 ) {
            $('.notification-dropdown').toggle();
            return false;
        }
        if( $(e.target).closest('.notification-dropdown').length > 0 ) {

        }else{
            $('.notification-dropdown').hide();
        }
    });

    $(document).click(function(e){
        if( $(e.target).closest('.noti2-click').length > 0 ) {
            $('.notification-dropdown2').toggle();
            return false;
        }
        if( $(e.target).closest('.notification-dropdown2').length > 0 ) {

        }else{
            $('.notification-dropdown2').hide();
        }
    });

    $('.qr-code').click(function(){
        $(this).parents('.notification-dropdown2').css({ display: "none" });
    })

    $('.post-header .dots-post').click(function(){
        var x = $(this).parents('.post-box').attr('post-id');
        $('.unFollow-popup .btn-unFollow a , .delete-popup .btn-unFollow a , .pinned-popup .btn-unFollow a').attr('post-id' , x);
    });

    $('.post-header .dots-post').click(function(){
        $('.details-drop').hide();
        $(this).siblings('.details-drop').toggle();
    });

    $(document).click(function(e){
        if( $(e.target).closest('.dots-post , .details-drop').length > 0 ) {
            return false;
        }else{
            $('.details-drop').hide();
        }

    });

    $('.open-popup').click(function(){
        var conn = $(this).attr('pop-attr');
        $('[pop-target='+conn+']').show();
        $('.overlay-box').show();
        $(this).parents('.details-drop').hide();
    });
    $('[pop-target] .custom-ex , [pop-target] .btn-cancel').click(function(){
        $('.overlay-box').hide();
        $('[pop-target]').hide();
    });

    $('.custom-link').click(function(e){
        e.preventDefault();
        $('.overlay-box').show();
        $('.link-popup').show();
        var href_link = $(this).attr('href');
        var link_text ;
        if(href_link.startsWith("https") === true){
            link_text = 'you are about to open another link browser tab and visit :';
        }else{
            link_text = 'The link you are trying to get is not (https), which means that your connection via it will not be encrypted and secure.';
        }
        $('.link-popup .popup-p .main-txt-pop').text(link_text);
        $('.link-popup .popup-p .msg-link').text(href_link);
        $('.link-popup .btn-continue a').attr('href' , href_link );
    });

    $('.link-modal').click(function(e){
    e.preventDefault();
    $('.overlay-box').hide();
    $('.link-popup').hide();
    });

    $('.img-upload').click(function(){
        $('.replay-img[data-upload='+$(this).attr('data-toggle')+']').click();
    });

    $('.main-react').hover(function(){
        $(this).find('.reaction-box').addClass('d-flex');
        $(this).find('.reaction-box img').addClass('img-animation');
    }, function() {
        $(this).find('.reaction-box').removeClass('d-flex');
    });
    $('.box-reaction').click(function(){
        $(this).parents('.reaction-box').removeClass('d-flex');
    });

    $('.select-flair').click(function(){
        var conn = $(this).attr('data-target');
        $('.flair-list[data-id="'+ conn +'"]').toggle();
    });
    $(document).click(function(e){
        if  ( $(e.target).closest('.flair-list .flair-exit').length > 0 ){
            $('.flair-list').hide();
        }
        else if( $(e.target).closest('.flair-list , .select-flair').length > 0 ) {
        }else{
            $('.flair-list').hide();
        }

    });

    $( window ).scroll(function() {
        if($(window).scrollTop() > 200){
            $('.up-btn').fadeIn(500);
        }else{
            $('.up-btn').fadeOut(500);
        }
    });
    $(".up-btn").click(function() {
        $('html, body').animate({
            scrollTop: $("body").offset().top
        }, 800);
    });

   $('.search-result-box .custom-more a').click(function(e){
       e.preventDefault();
       var text = $(this).text();
       if( text == 'More...'){
           $(this).html('Less...');
       }else{
           $(this).html('More...');
       }
       $(this).parents('.search-result-box').toggleClass('devo-open');
   });


   $('.dots-follow').click(function(){
       $('.follow-option-list').hide();
        $(this).siblings('.follow-option-list').toggle();
    });
    $('.follow-option-list .ex-btn').click(function(){
        $(this).parents('.follow-option-list').hide();
    });
    $(document).click(function(e){
        if( $(e.target).closest('.follow-option-list , .dots-follow').length > 0 ) {
        }
        else{
            $('.follow-option-list').hide();
        }
    });

$('.select-sort-type').click(function(){
    document.getElementById("sort-type-list").classList.toggle("show-sort-types");
});

window.onclick = function(e) {
    if (!e.target.closest('.select-sort-type')) {
    var myDropdown = document.getElementById("sort-type-list");
    if(myDropdown !=undefined) {
        if (myDropdown.classList.contains('show-sort-types')) {
        myDropdown.classList.remove('show-sort-types');
    }}
    }
}

        $('.box-item').click(function(e){
            var element = $(this);
            var element_id = element.attr('notify-id');
            $.ajax({
                url: $('.notify_read_view').attr("href"),
                type: 'POST',
                data: { id: element_id } ,
                success: function(){
                    customNotificationEffect();
            }});
            function customNotificationEffect(){
                $('.box-item[notify-id='+element_id+']').removeClass('custom-unread');
            }
    });

      $('.box-item').click(function(e){
            var element = $(this);
            var element_id = element.attr('admin-notify-id');
            $.ajax({
                url: $('.admin_notify_read_view').attr("href"),
                type: 'POST',
                data: { id: element_id } ,
                success: function(){
                    customNotificationEffect();
            }});
            function customNotificationEffect(){
                $('.box-item[admin-notify-id='+element_id+']').removeClass('custom-unread');
            }
    });


});