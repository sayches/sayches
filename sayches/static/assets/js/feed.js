let page = 1, type, last_post_created_at=null;
var loadingBarFlag = true;
function loadPosts(sortBy="", page_number) {
    if(type !== sortBy) {
        loadingBarFlag = true;
    }
    type = sortBy;
    document.getElementById("current-sort-type").innerText = type.charAt(0).toUpperCase() + type.slice(1);
    window.removeEventListener('scroll', loadCallFuntion);
    if (loadingBarFlag) {
        var loadingBar = $("#loadPostIconId");
        loadingBar.show();
        $.ajax({
            url: postsData + "?sortby=" + type + "&page=" + page_number,
            async: false,
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
                    if (data && data[0])
                    {
                      last_post_created_at = data[0].created_at
                    }
                });
            }
        }).done(function () {
            $.getScript(STATIC_URL + 'assets/js/post.js');
            loadingBar.hide();
            window.addEventListener('scroll', loadCallFuntion);
        });
    }

}
loadPosts(type, page);
function loadCallFuntion() {
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
        page = page + 1;
        loadPosts(type, page);
    }
}
window.addEventListener('scroll', loadCallFuntion);

function loadNewPosts(){
    $.ajax({
        url: newPostsData + "?datetime=" + last_post_created_at,
        success: function(data){
            $.getScript(STATIC_URL + 'assets/js/script-ajax.js', function(){
                getNewPost(data);
                customCall();
                loadReacton();
              if (data && data[0])
                    {
                      last_post_created_at = data[0].created_at
                    }
            });
    }}).done(function(){
        $.getScript(STATIC_URL + 'assets/js/post.js');
    });
}

setInterval(function () {
  loadPosts(type, 1);
}, 30 * 1000);