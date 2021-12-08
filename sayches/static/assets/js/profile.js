function reportAUser(event) {

	var form = $("#reportuserForm");

	$.ajax({
		url: '/report_user',
		type: 'POST',
		data: form.serialize(),
		success: function() {
			$('.option-popup-box').removeClass('d-flex')
			alert('Thanks for letting us know');
			location.reload();
		}
	});
	event.preventDefault();
	return false;
}

var page_number = 1
$(function() {
	$.ajax({
		url: uINum + "?sortby=" + type + "&page=" + page_number,
		success: function(data) {
			$.getScript(STATIC_URL + 'assets/js/script-ajax.js', function() {
				getPost(data);
				customCall();
				loadReacton();
			});
		}
	}).done(function() {
		$.getScript(STATIC_URL + 'assets/js/post.js');
	});
});

let page = 1,
	type;
var loadingBarFlag = true;

function loadPosts(sortBy = "Recent", page_number) {
	if (type !== sortBy) {
		loadingBarFlag = true;
	}
	type = sortBy;
	document.getElementById("current-sort-type").innerText = type.charAt(0).toUpperCase() + type.slice(1);
	window.removeEventListener('scroll', loadCallFuntion);
	if (loadingBarFlag) {
		var loadingBar = $("#loadPostIconId");
		loadingBar.show();
		$.ajax({
			url: uINum + "?sortby=" + type + "&page=" + page_number,
			success: function(data) {
				$.getScript(STATIC_URL + 'assets/js/script-ajax.js', function() {
					if (page_number == 1) {
						$('.main-post-box').empty()
					}
					if (data.length == 0) {
						loadingBarFlag = false;
					}
					getPost(data);
					customCall();
					loadReacton();
				});
			}
		}).done(function() {
			$.getScript(STATIC_URL + 'assets/js/post.js');
			loadingBar.hide();
			window.addEventListener('scroll', loadCallFuntion);
		});
	}

}

function loadCallFuntion() {
	if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
		page = page + 1;
		loadPosts(type, page);
		loadReacton();
	}
}
window.addEventListener('scroll', loadCallFuntion)

function updateBellNotificaion() {
	const Url = setOrRemoveBell
	$.ajax({
		url: Url,
		type: "POST",
		success: function(data) {
			if (data.message) {
				$('#bell_notification').show();
				$('#unbell_notification').hide();
			} else {
				$('#unbell_notification').show();
				$('#bell_notification').hide();
			}

		},
		error: function(error) {}

	})
}

$("#ping").click(function() {
	$('#ping').css({
		'color': 'grey'
	});
	const Url = pingUsername
	$.ajax({
		url: Url,
		type: "POST",
		success: function(data) {},
		error: function(error) {}

	})

});

const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");

$('[data-toggle="popover"]').popover();
$('body').on('click', function(e) {
	$('[data-toggle=popover]').each(function() {
		if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
			$(this).popover('hide');
		}
	});
});
