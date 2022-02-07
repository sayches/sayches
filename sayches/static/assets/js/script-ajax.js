var eggIcon = '🥚';

function structurePost(data) {
    var url = "/p/1".replace(/1/, data.id);
    var single_post =
        '<div class="main-box">';
            if(data.flag == 'read'){
                if(data.pinned === true){
                    single_post +=
                    '<div class="post-box pin-post" post-id ="'+data.id+'">' ;
                }else{
                    single_post +=
                    '<div class="post-box" post-id ="'+data.id+'">' ;
                }
            }else{
                if(data.pinned === true){
                    single_post +=
                    '<div class="post-box custom-unread pin-post" post-id ="'+data.id+'">' ;
                }else{
                    single_post +=
                    '<div class="post-box custom-unread" post-id ="'+data.id+'">' ;
                }
            }
            single_post +=
                '<div class="post-header">'+
                    '<div class="first-box"> ' ;
                        if(data.post_type == 'anonymous'){
                            single_post +=
                            '<div class="user-img">'+
                                '<a href="#"><img src="'+ STATIC_URL+'assets/images/avatars/incognitoAvatar/incognitoAvatar_360x360.png"></a>'+
                            '</div> ' +
                            '<div class="user-name-box">'+
                                '<h4 class="heading name-h"><a href="#" class="text-truncate-100-media">'+data.user_nickname+'</a></h4>'+
                            '</div>';
                        }else{
                            single_post +=
                            '<div class="user-img">'+
                                '<a href="'+data.user_page+'"><img src="'+data.user_img+'"></a>'+
                            '</div> ' +
                            '<div class="user-name-box">'+
                                '<h4 class="heading name-h"><a href="'+data.user_page+'" class="text-truncate-100-media">'+data.name+'</a></h4>'+
                            '</div>'+
                            '<div class="post-popup">'+
                                '<div class="popup-header">'+
                                    '<div class="first-box">'+
                                        '<div class="user-img">'+
                                            '<a href="'+data.user_page+'">'+
                                                '<img src="'+data.user_img+'">'+
                                            '</a>'+
                                        '</div>'+
                                        '<div class="user-name-box">'+
                                            '<a href="'+data.user_page+'">'+
                                                '<h4 class="heading name-h">'+data.name+'</h4>'+
                                                '<p class="parag profile-p">'+data.user_name+'</p>'+
                                            '</a>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                                '<div class="follower-box">'+
                                '</div>'+
                                '<p class="description-pop heading">'+data.bio+'</p>'+

                            '</div>';
                            }
                single_post +=
                    '</div>' +
                    '<div class="sec-box">'+
                        '<p class="view-box parag">'+'<i class="ri-eye-fill"></i>'+data.post_count+'</p>'+
                        '<p class="parag custom-time">'+data.remaining_time+' hours'+'<i class="ri-timer-fill"></i>'+'</p>'+

                        '<p class="parag custom-time" comm-post-id="'+data.id+'" data-attr = "post_'+data.id+'">'+ '<a href= url target="_blank" >'.replace('url', url )+ '<i class="ri-external-link-fill"></i>'+ '</a>'+ '</p>'+
                        
                        '<ul class="details-drop">'+
                            '<li class="parag li-delete open-popup" pop-attr="delete-popup">delete</li>';
                            if (data.login_user === data.user_name && (data.post_option === 'normal')){
                                if(data.pinned === true){
                                    single_post += '<li class="parag li-unpinned">unpinned</li>';
                                }else{
                                    single_post += '<li class="parag li-pinned">pinned</li>';
                                }
                            }
                        single_post +=
                        '</ul>'+
                    '</div>'+
                '</div>'+
                '<div class="post-body">';
                if(data.post_flair == 'No Flair'){
                }
                else{
                    single_post +=
                    '<div class="post-flair-box">'+

                        '<p class="parag post-flair custom-'+data.post_flair.replace(/\s/g, '')+'">'+'<a href="/f/'+data.post_flair+'">'+data.post_flair+'</a></p>'+
                    '</div>';
                }

                    if(data.post_option == 'normal'){
                        single_post +=
                        '<p class="parag post-p" dir="auto">'+data.post_p+'</p>';
                        if(data.post_media != 'null'){
                            single_post +=
                            '<a class="link-container width-unset h-unset" arget="_blank" href="'+data.post_media+'"><img class="rounded mx-auto d-block" src="'+data.post_media+'" alt="Download" /></a>';
                        }
                    }


    single_post +=
        '</div>' +
        '<div class="post-footer">';
    if(data.user_reaction === 'guest'){
                            single_post += '<div class="main-react">';

                        }
    else if (data.user_reaction != null) {
                            single_post += '<div class="main-react" reaction_status="' + data.user_reaction + '" reaction-count="' + data.reaction_number + '" like-post-id="' + data.id + '"  do_status="' + data.do_status + '">';
                        }

                        else {
                            single_post += '<div class="main-react" reaction_status="' + data.reaction_status + '"  reaction-count="' + data.reaction_number + '"  like-post-id="' + data.id + '"  do_status="' + data.do_status + '">';

                        }

    single_post += 
                             '<div title="Egging is a well-known form of protest." data-react='+eggIcon+' class="box-reaction">'+
                        '<div data-react="like" class="box heart-box">';
                            if( data.reaction_status == eggIcon ){
                                single_post += data.reaction_status+
                                '<p class="box-p parag"> <span class="txt-like">Eggs('+data.reaction_status+')</span></p>';
                                
                            }
                            
                            else{
                                if(data.user_reaction === 'guest'){
                                 single_post += '<p class="box-p parag mr-2"><i class="ri-thumb-down-line primary-colour"></i>' + data.reaction_number +'</p> <p class="box-p parag addreaction-box"> <span class="txt-like"> Eggs</span></p>';


                        }
                                else if (data.user_reaction != null) {
                                    single_post += '<p class="box-p parag mr-2">' + data.reaction_number + data.user_reaction;

                                }
                                else {
                                    single_post += '<i class="ri-thumb-down-line primary-colour"></i><p class="box-p parag addreaction-box mr-2">'+data.reaction_number+'<span class="txt-like"> Eggs</span></p>';
                                      }
                            }
                            single_post +=
                            '</div>'+
                                '</div>'+
                    '</div>'+

                '</div>'+
            '</div>'+
        '</div>';

        return single_post;
}

function getPost(data){
    if(!data.length){
        emptyState();
    }else{
        $.each(data, function(i, f) {
            var single_post = structurePost(data[i]);
            $(single_post).appendTo(".main-post-box");
        });
    }
}

function getNewPost(data){
    if(!data.length){
        emptyState();
    }else{
        $.each(data, function(i, f) {
            var single_post = structurePost(data[i]);
            $(single_post).prependTo(".main-post-box");
        });
    }
}

function addNewPost(data){
    if($('.main-box.main-empty-box').length){
        $('.main-box.main-empty-box').remove();
    }
    $.each(data, function(i, f) {
        var single_post = structurePost(data[i]);
        $(single_post).prependTo(".main-post-box");
        $('#no_flair').click();
    });
}

function emptyState(){
    $(".main-box.main-empty-box").remove();
    var empty_state = '<div class="main-box main-empty-box">'+
        '<img src="'+ STATIC_URL+'assets/images/icons/svgIcons/fish_2404x1338.svg" class="fish-icon">'+
        '<p class="parag box-p">There are no fish in the sea!</p>'+
    '</div>';
    $(empty_state).appendTo(".main-post-box");
}

function customCall(){


        $('.main-box > .post-box').click(function(){

            var element = $(this);
            var element_id = element.attr('post-id');
            var element_count = element.find('.view-box .view-num').text();
            $.ajax({
                url: $('.post_read_view').attr("href"),
                type: 'POST',
                data: { id: element_id } ,
                success: function(){
                    customCommEffect();
            }});
            function customCommEffect(){
                if(element.hasClass('custom-unread')){
                    element.find('.view-box .view-num').html(parseInt(element_count) + 1);
                }
                element.removeClass('custom-unread');
            }
        });
    $('.main-react').off("click").on("click", ".box-reaction", function () {
        var main_element = $(this);
        var reaction_status = main_element.parents('.main-react').attr('reaction_status');
        var status_2 = main_element.attr('data-react');
        var element_id = main_element.parents('.main-react').attr('like-post-id');
        var do_status = main_element.parents('.main-react').attr('do_status');
        var element_count = $('.main-react[like-post-id="'+element_id+'"]').find('.heart-box .box-p .num-like').text();
        var new_do_status = 'undo';
        var reaction_count = main_element.parents('.main-react').attr('reaction-count');
        var new_reaction_status;
        if(reaction_status !== status_2){
            new_reaction_status = status_2 ;
            customReaction( reaction_count,new_do_status , do_status , reaction_status , new_reaction_status , element_id , element_count);
        }
    });

    function customReaction(reaction_count,new_do_status, do_status, reaction_status, new_reaction_status, element_id, element_count) {
        $.ajax({
            url: $('.like_post_view').attr("href"),
            type: 'POST',
            data: { id: element_id , action: new_reaction_status , do_action : new_do_status } ,
            success: function () {
                customLikeEffect(reaction_count);
        }});
        function customLikeEffect(reaction_count){

            var num_new_reaction_status = $('.reaction-details[like-post-id="'+element_id+'"] .box-'+new_reaction_status+' .num-reaction').text();
            var num_reaction_status = $('.reaction-details[like-post-id="'+element_id+'"] .box-'+reaction_status+' .num-reaction').text();


            if(do_status !==  new_do_status){
                if (new_do_status == 'undo') {
                    $('.main-react[like-post-id="'+element_id+'"]').find('.heart-box .box-p .num-like').html(parseInt(element_count) + 1);

                    $('.reaction-details[like-post-id="'+element_id+'"] .box-'+new_reaction_status+' .num-reaction').html(parseInt(num_new_reaction_status) + 1);

                }else{
                    $('.main-react[like-post-id="'+element_id+'"]').find('.heart-box .box-p .num-like').html(parseInt(element_count) - 1);

                    $('.reaction-details[like-post-id="'+element_id+'"] .box-'+reaction_status+' .num-reaction').html(parseInt(num_reaction_status) - 1);
                }
                $('.main-react[like-post-id="'+element_id+'"]').attr('do_status' , new_do_status );
            }else{

                $('.reaction-details[like-post-id="'+element_id+'"] .box-'+new_reaction_status+' .num-reaction').html(parseInt(num_new_reaction_status) + 1);

                $('.reaction-details[like-post-id="'+element_id+'"] .box-'+reaction_status+' .num-reaction').html(parseInt(num_reaction_status) - 1);
            }
            $('.main-react[like-post-id="'+element_id+'"]').attr('reaction_status' , new_reaction_status);

            $('.main-react[like-post-id='+element_id+'] .heart-box img , .main-react[like-post-id='+element_id+'] .heart-box i').remove();

            if( new_reaction_status == 'unlike'){

                $('.main-react[like-post-id='+element_id+']').find('.heart-box').prepend('<i class="ri-heart-line primary-colour"></i>');
                $('.main-react[like-post-id='+element_id+']').find('.heart-box .box-p .txt-like').html('like');

            }else if(new_reaction_status == 'like'){
                $('.main-react[like-post-id='+element_id+']').find('.heart-box').prepend('<i class="ri-heart-line"></i>');
                $('.main-react[like-post-id='+element_id+']').find('.heart-box .box-p .txt-like').html('Reaction');
            } else{
                $('.main-react[like-post-id=' + element_id + ']').find('.heart-box').prepend('<p class="box-p parag">' + (parseInt(reaction_count) + 1) + new_reaction_status);

                $('.main-react[like-post-id=' + element_id + ']').find('.heart-box').find(".addreaction-box").remove();
            }
        }
    }


    $('.li-unpinned').unbind('click').bind('click' , (function(){
        var post_li = $(this);
        var post_id = post_li.parents('.post-box').attr('post-id');
        $.ajax({
            url: $('.pin-post-view').attr("href"),
            type: 'post',
            data: { id: post_id } ,
            success: function(){
                customUnpinnedPost();
                customCall();
        }});
        function customUnpinnedPost(){
            post_li.parents('.post-box').removeClass('pin-post');
            post_li.removeClass('li-unpinned').addClass('li-pinned').text('pinned');
            post_li.parents('.details-drop').hide();
        }
    }));

    $('.details-drop .li-pinned').unbind('click').bind('click' , (function(){
        $('.overlay-box').show();
        $('.pinned-popup').show();
        $(this).parents('.details-drop').hide();
    }));

    $('.pinned-popup .custom-ex , .pinned-popup .btn-cancel').unbind('click').bind('click' , (function(){
        $('.overlay-box').hide();
        $('.pinned-popup').hide();
    }));

    $('.pinned-popup .btn-unFollow a').unbind('click').bind('click' , (function(e){
        e.preventDefault();
        var post_id = $(this).attr('post-id');
        $.ajax({
            url: $('.pin-post-view').attr("href"),
            type: 'post',
            data: { id: post_id } ,
            success: function(data){
                customPinnedPost();
                customCall();
        }});
        function customPinnedPost(){
            $('.overlay-box').hide();
            $('.pinned-popup').hide();
            $('.post-box').removeClass('pin-post');
            $('.post-box[post-id='+post_id+']').addClass('pin-post');
            $('.post-box').find('.li-unpinned').removeClass('li-unpinned').addClass('li-pinned').text('pinned');
            $('.post-box[post-id='+post_id+']').find('.li-pinned').removeClass('li-pinned').addClass('li-unpinned').text('unpinned');
        }
    }));

}

$(".newPost").unbind('submit').bind('submit',function(event){
    event.preventDefault();
    var Form = $(this);
    var form_txt = Form.find('.post-textarea').val().trim();
    var form_type = Form.find('[name="type-post"]').prop('checked');
    var media_thumbnail_image = $("#media-image-image")
    var media_thumbnail_image_src = media_thumbnail_image[0].src;
    var form_image = ""
    if (media_thumbnail_image_src !== window.location.href){
        form_image = $("#media-upload")[0].files[0];
    }
    var form_flair = Form.find('[name="flair-post"]:checked').val();
    var formData = new FormData();
        formData.append('type', form_type)
       formData.append('text', form_txt)
       formData.append('flair', form_flair)
        formData.append('media',  form_image)
    $.ajax({
        url: $('.create_post_view').attr("href"),
        type: 'POST',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        enctype: 'multipart/form-data',
        success: function(data){
            var no_flair = 'No Flair'
            $('input:radio[name=flair-post]').filter('[value="'+no_flair+'"]').prop('checked', true);
            $("#my_radio_box").html("No Flair")
            addNewPost(data);
            customPost();
            $.getScript(STATIC_URL+'assets/js/post.js');
            customCall();
            $('#my_radio_box').text("Select Flair");
            media_thumbnail_image[0].style.display = "none";
            document.getElementById('media-image-image').src = "";
    }});
    function customPost(){
        if($('.main-post-box .main-empty-box').length){
            $('.main-post-box .main-empty-box').hide();
        }
        Form.find('.post-textarea').val('');
        Form.find('.post-btn').removeClass('focus-btn').attr('disabled', true);
        Form.find('.custom-counter').hide();
    }
});

function structureDetailsPost(data){
    var single_post =
            '<div class="main-box">';
                if(data.flag == 'read'){
                    if(data.pinned === true){
                        single_post +=
                        '<div class="post-box pin-post" id= "'+data.id+'" post-id ="'+data.id+'">' ;
                    }else{
                        single_post +=
                        '<div class="post-box" id= "'+data.id+'" post-id ="'+data.id+'">' ;
                    }
                }else{
                    if(data.pinned == 'true'){
                        single_post +=
                        '<div class="post-box custom-unread pin-post" id= "'+data.id+'" post-id ="'+data.id+'">' ;
                    }else{
                        single_post +=
                        '<div class="post-box custom-unread" id= "'+data.id+'" post-id ="'+data.id+'">' ;
                    }
                }
                single_post +=
                    '<div class="post-header">'+
                        '<div class="first-box"> ' ;
                            if(data.post_type == 'anonymous'){
                                single_post +=
                                '<div class="user-img">'+
                                    '<a href="#"><img src="'+ STATIC_URL+'assets/images/avatars/incognitoAvatar/incognitoAvatar_360x360.png"></a>'+
                                '</div> ' +
                                '<div class="user-name-box">'+
                                    '<h4 class="heading name-h"><a href="#" class="text-truncate-100-media">'+data.user_nickname+'</a></h4>'+
                                '</div>';
                            }else{
                                single_post +=
                                '<div class="user-img">'+
                                    '<a href="'+data.user_page+'"><img src="'+data.user_img+'"></a>'+
                                '</div> ' +
                                '<div class="user-name-box">'+
                                    '<h4 class="heading name-h"><a href="'+data.user_page+'" class="text-truncate-100-media">'+data.name+'</a></h4>'+
                                '</div>'+
                                '<div class="post-popup">'+
                                    '<div class="popup-header">'+
                                        '<div class="first-box">'+
                                            '<div class="user-img">'+
                                                '<a href="'+data.user_page+'">'+
                                                    '<img src="'+data.user_img+'">'+
                                                '</a>'+
                                            '</div>'+
                                            '<div class="user-name-box">'+
                                                '<a href="'+data.user_page+'">'+
                                                    '<h4 class="heading name-h">'+data.name+'</h4>'+
                                                    '<p class="parag profile-p">'+data.user_name+'</p>'+
                                                '</a>'+
                                            '</div>'+
                                        '</div>'+
                                    '</div>' +
                                    '<div class="follower-box">'+
                                    '</div>'+
                                    '<p class="description-pop heading">'+data.bio+'</p>'+

                                '</div>';
                             }
                             var delet_post_popup = data.is_his_post ? '<li class="parag li-delete open-popup" pop-attr="delete-popup">delete</li>' : "";
                             single_post +=
                             '</div>' +
                                 '<div class="sec-box">'+
                                     '<p class="parag custom-time mt-2">'+data.date+'</p>'+
                                     '<div class="profile-dropdown " id="profile-dropdownID">'
                                    if (data.login_user){
                                        single_post +=
                                        '<button  class="btn dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+
                                         '<i class="ri-more-2-fill" pop-attr=""></i>'+
                                         '</button>'
                                    }else{
                                        single_post +=
                                        '<button  class="btn" type="button" >'+
                                         '<i class="ri-more-2-fill" pop-attr=""></i>'+
                                         '</button>'
                                    }
                                    single_post +=
                                         '<div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">'
                                         if (data.login_user !=data.user_name ){
                                             single_post +=
                                                 '<a class="dropdown-item" data-toggle="quote-popup" onclick="$(\'.option-popup-box\').addClass(\'d-flex\')">Report</a>'
                                             }
                                         else{
                                            if (data.is_pin_post){
                                                single_post +=
                                                '<a title="Prevent your profile from being blank after 24 hours and make sure users know your profile is active. Pinning is a great way to promote your most important posts." class="dropdown-item" onclick="PinAPost(\''+data.id+'\')" id= "text'+data.id+'">Unpin Post</a>'
                                            }else{
                                                single_post +=
                                                '<a title="Prevent your profile from being blank after 24 hours and make sure users know your profile is active. Pinning is a great way to promote your most important posts." class="dropdown-item" onclick="PinAPost(\''+data.id+'\')" id= "text'+data.id+'" onclick="PinAPost(\''+data.id+'\')" >Pin Post</a>'
                                            }
                                            single_post +='<a class="dropdown-item custom-curor primary-red" onclick="DeleteAPost(\'' + data.id + '\')" id= "text' + data.id + '" onclick="PinAPost(\'' + data.id + '\')" >Delete Post</a>'
                                         }
                                single_post +=
                                '</div>'+
                            '</div>'+
                        '</div>'+
                            '<ul class="details-drop">'+
                                delet_post_popup
                                if (data.login_user === data.user_name &&(data.post_option === 'normal' )){
                                    if(data.pinned == true){
                                        single_post += '<li class="parag li-unpinned">unpinned</li>';
                                    }else{
                                        single_post += '<li class="parag li-pinned">pinned</li>';
                                    }
                                }
                                single_post +=
                            '</ul>'+
                        '</div>'+
                    '</div>'+
                    '<div class="post-body">'+
                                (data.post_flair == 'No Flair' ? "" : '<div class="post-flair-box">' +
                            '<p class="parag post-flair custom-'+data.post_flair.replace(/\s/g, '')+'">'+'<a href="/f/'+data.post_flair+'">'+data.post_flair+'</a></p>'+
                        '</div>');

                        if(data.post_option == 'normal'){
                            single_post +=
                                '<p class="parag post-p" dir="auto">'+data.post_p+'</p>';
                            if(data.post_media != 'null'){
                                single_post +=
                                '<a class="link-container width-unset h-unset" arget="_blank" href="'+data.post_media+'"><img class="rounded mx-auto d-block" src="'+data.post_media+'" alt="Download" /></a>';
                            }
                        }


    single_post +=
        '</div>' +
        '<div class="post-footer">';
                        if(data.user_reaction === 'guest'){
                                 single_post += '<div class="main-react">';

                        }
                             else if (data.user_reaction != null) {
                                single_post += '<div class="main-react" reaction_status="' + data.user_reaction + '" reaction-count="' + data.reaction_number + '" like-post-id="' + data.id + '"  do_status="' + data.do_status + '">';

                                }
                             else {
                                single_post += '<div class="main-react" reaction_status="' + data.reaction_status + '"  reaction-count="' + data.reaction_number + '"  like-post-id="' + data.id + '"  do_status="' + data.do_status + '">';

                                }
    single_post +=  
                                '<div title="Egging is a well-known form of protest." data-react='+eggIcon+' class="box-reaction">'+

                            '<div data-react="like" class="box heart-box">';
                                if( data.reaction_status == eggIcon ){
                                    single_post += data.reaction_status+
                                    '<p class="box-p parag"> <span class="txt-like">Eggs('+data.reaction_status+')</span></p>';
                                    
                                }
                                else{
                                    if(data.user_reaction === 'guest'){
                                        single_post += '<div class="main-react">';

                                    }
                                    else if (data.user_reaction != null) {
                                        single_post += '<p class="box-p parag">' + data.reaction_number + data.user_reaction;

                                    }
                                    else {
                                        single_post += '<i class="ri-thumb-down-line primary-colour"></i><p class="box-p parag addreaction-box mr-2">'+data.reaction_number+'<span class="txt-like"> Eggs</span></p>';
                                     }
                                }
                                single_post +=
                                '</div>'+
                            '</div>'+
                        '</div>'+

                '</div>'+
            '</div>';
        return single_post;
}

function loadReactions(data){

    $.each(data, function(i, f) {
        var single_post = structureDetailsPost(data[i]);
        $(".main-post-box").empty();
        $(single_post).appendTo(".main-post-box");
    });

}

function getDetailsPost(data){
    $.each(data, function (i, f) {
        var single_post = structureDetailsPost(data[i]);
        $(single_post).appendTo(".main-post-box");
    });
}

$(function(){
    $("#myForm input").on("change", function () {
        var l = $("input[name='flair-post']:checked").data("name");
        $('#my_radio_box').text(l);
        document.getElementById('flair-div').style.display = 'none'
    });

});

$(".img-code").change(function() {
    if($(this).siblings(".select2-container").find('.imgFlag').length){
        $(this).siblings(".select2-container").find('.imgFlag').attr('src' , +STATIC_URL+'assets/images/icons/svgIcons/'+ $(this).find('option:selected').val() +'.svg');
    }else{
        $(this).siblings(".select2-container").find(".select2-selection--single").prepend("<img class='imgFlag' src='"+ STATIC_URL +"assets/images/icons/svgIcons/"+ $(this).find('option:selected').val() +".svg'/>");
    }
});
