$(function () {
$.ajax({
    url: "",
    success: function (data) {
    $.getScript(STATIC_URL + 'assets/js/script-ajax.js', function () {
        getPost(data);
        customCall();
        loadReacton();
    });
    }
}).done(function () {
    $.getScript(STATIC_URL + 'assets/js/post.js');
});
});

let page = 1, type;
var loadingBarFlag = true;

function loadPosts(sortBy = "", page_number) {
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
    url: flairPosts + "?search=" + query + "&sortby=" + type + "&page=" + page_number,
    success: function (data) {
        $.getScript(STATIC_URL + 'assets/js/script-ajax.js', function () {
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
    }).done(function () {
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

window.addEventListener('scroll', loadCallFuntion);