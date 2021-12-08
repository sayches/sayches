setTimeout(function() {
	var post_arr = [];
	window.slide_it = true;
	var scrollTime = null;
	$('.main-post-box .main-box').each(function() {
		post_arr.push($(this));
	});

	if (post_arr.length > 0) {
		post_arr[post_arr.length - 1].removeClass('animation-post');
		post_arr.splice(post_arr.length - 1, 1);
	}

	slide_it();
	$('.main-post-box').on({

		mouseenter: function() {
			window.slide_it = false;
			slide_it();
		},

		mouseleave: function() {
			window.slide_it = true;
			slide_it();
		}

	});

	function slide_it() {

		if (!window.slide_it) {
			clearInterval(scrollTime);
		} else {

			scrollTime = setInterval(function() {
				if (post_arr.length > 0) {
					post_arr[post_arr.length - 1].removeClass('animation-post');
					post_arr.splice(post_arr.length - 1, 1);

				} else {
					clearInterval(scrollTime);
				}
			}, 3000);
		}
	}
}, 500);


var wordLen = 30,
	len,
	txt;

$('.custom-counter').html(wordLen);

$(".postInput").bind("paste", function(e) {
	var _this = this;
	setTimeout(function() {
		var text = $(_this).val();
		maxLengthCheck(text);
	}, 100);
});

$(".postInput").keypress(function(e) {
	if (e.shiftKey && (e.which == 60 || e.which == 62)) {
		e.preventDefault();
	}
	checkText()
});

function checkText() {
	var content = $('.postInput').val();
	maxLengthCheck(content);

}

function checklenghtAndChangeColor(content) {
	var con = (content.value).trimStart()
	$(`#${content.id}`).val((content.value).trimStart());
	var num_Word = con.split(/\s+/g).length
	var max_lenght = 30;
	if (con.length < 1 || con.length > 700 || num_Word > max_lenght) {
		document.getElementById('postForm-box').style.boxShadow = 'rgb(237 25 95 / 10%) 1px 2px 5px 5px inset';
		$('#makePostSubmit').removeClass('focus-btn');
		$('#makePostSubmit').attr('disabled', true);
	} else {
		document.getElementById('postForm-box').style.boxShadow = 'inset 0px 4px 8px 2px rgb(88 108 138 / 10%)';
		$('#makePostSubmit').addClass('focus-btn');
		$('#makePostSubmit').attr('disabled', false);
	}
}


function maxLengthCheck(text) {

	var content = text;
	var num_words = content.split(/\s+/g).length
	var max_limit = 30;
	if (num_words > max_limit) {
		$('.custom-counter').text('0');
		return false;
	} else {
		$('.custom-counter').text(max_limit - num_words);
		return true
	}
}


$('.post-header .dots-post').click(function() {
	var x = $(this).parents('.post-box').attr('post-id');
	$('.unFollow-popup .btn-unFollow a , .delete-popup .btn-unFollow a , .pinned-popup .btn-unFollow a').attr('post-id', x);
});


$('.post-header .dots-post').click(function() {
	$('.details-drop').hide();
	$(this).siblings('.details-drop').toggle();
});

$(document).click(function(e) {
	if ($(e.target).closest('.dots-post , .details-drop').length > 0) {
		return false;
	} else {
		$('.details-drop').hide();
	}

});




$('.open-popup').click(function() {
	var conn = $(this).attr('pop-attr');
	$('[pop-target=' + conn + ']').show();
	$('.overlay-box').show();
	$(this).parents('.details-drop').hide();
});
$('[pop-target] .custom-ex , [pop-target] .btn-cancel').click(function() {
	$('.overlay-box').hide();
	$('[pop-target]').hide();
});




$(document).on('click', 'a[class^="custom-link"]', function(e) {
	e.preventDefault();
	$('.overlay-box').show();
	$('.link-popup').show();
	var href_link = $(this).attr('href');
	var link_text;
	if (href_link.startsWith("https") === true) {
		link_text = ' You are about to open another website. ';
	} else {
		link_text = ' You are about to open an unsecure website. Look for the “S” in https. ';
	}
	$('.link-popup .popup-p .main-txt-pop').text(link_text);
	$('.link-popup .popup-p .msg-link').text(href_link);
	$('.link-popup .btn-continue a').attr({
		target: "_blank",
		'href': href_link
	});
	var confirm_txt = $(this).attr('confirm-msg');
	$('.link-popup .popup-p .msg-txt').text(confirm_txt);
	var confirm_txt2 = $(this).attr('confirm-msg2');
	$('.link-popup .popup-p .msg-txt2').text(confirm_txt2);
});


$('.link-modal').click(function(e) {
	e.preventDefault();
	$('.overlay-box').hide();
	$('.link-popup').hide();
});


$('.img-upload').click(function() {
	$('.replay-img[data-upload=' + $(this).attr('data-toggle') + ']').click();
});



$('.post-btn').attr('disabled', true);

$('.postInput').on('keyup', function() {

	var textarea_value = $(this).val();
	var textarea_p = textarea_value.trim();

	if (textarea_p != '') {
		$('.post-btn[data-id=' + $(this).attr('data-attr') + ']').attr('disabled', false);
		$('.custom-counter[data-count=' + $(this).attr('data-attr') + ']').css('display', 'inline-block');
		$('.post-btn[data-id=' + $(this).attr('data-attr') + ']').addClass('focus-btn');
	} else {
		$('.post-btn[data-id=' + $(this).attr('data-attr') + ']').attr('disabled', true);
		$('.custom-counter[data-count=' + $(this).attr('data-attr') + ']').css('display', 'none');
		$('.post-btn[data-id=' + $(this).attr('data-attr') + ']').removeClass('focus-btn');
	}
});




$('.option-icon').click(function() {
	$(this).siblings('.option-list').toggle();
});
$('.option-list .custom-ex , .option-list .ex-btn').click(function() {
	$(this).parents('.option-list').hide();
});
$(document).click(function(e) {
	if ($(e.target).closest('.option-list , .option-icon').length > 0) {} else {
		$('.option-list').hide();
	}

});


$('.overlay-box').click(function() {
	$('.overlay-box').hide();
	$('.main-popup').hide();
	$('[pop-target]').hide();
});
$('.option-popup-box').click(function(evt) {
	if (evt.target.className.indexOf("option-popup-box") >= 0)
		$(this).removeClass('d-flex');
});