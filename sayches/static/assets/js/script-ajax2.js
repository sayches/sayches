function addClassToDiv() {
    var pr = document.getElementById('profile-dropdownID')
    if (pr.className != 'profile-dropdown') {
        $('#profile-dropdownID').addClass('profile-dropdown');
    }
};

function checkBox_Ticked_OR_Not() {
    var term_condition_Container = document.querySelectorAll('.termCheck');
    if ($(`#${term_condition_Container[0].id}`).prop("checked") && $(`#${term_condition_Container[1].id}`).prop("checked")) {
        $('#reportButton').removeClass('post-btn');
        $('#profile-dropdownID').removeClass('profile-dropdown');
        $('#reportButton').removeAttr('disabled')
    } else {
        var pr = document.getElementById('profile-dropdownID')
        if (pr != null) {
            if (pr.className != 'profile-dropdown') {
                $('#profile-dropdownID').addClass('profile-dropdown');
                $('#reportButton').addClass('post-btn');
                $('#reportButton').attr('disabled', 'disabled')
            }
        } else {
            $('#reportButton').addClass('post-btn');
            $('#reportButton').attr('disabled', 'disabled')
        }
    }
};

function preview_image(event) {
    var reader = new FileReader();
    reader.onload = function () {
        var output = document.getElementById('Avtar-image');
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
};

function DeleteAPost(event) {
    $('#deleteMyPost').attr('href', `/delete/post/${event}`);
    $('#ModalCenter6').modal('show');
};

function PinAPost(event) {
    $.ajax({
        url: '/pin/post',
        type: 'POST',
        data: {'id': event},
        success: function (args) {
            if (args.pinned) {
                
                $('#' + event).addClass("pin-post");
                $('#text' + event).html("Unpin post");
            } else {
                
                $('#' + event).removeClass("pin-post");
                $('#text' + event).html("Pin post");
            }
        }
    });
};

$(document).ready(function () {


    $("#search").on('keyup', () => {
        var search_val = $('#search').val();
        if (search_val.length < 2) {
            $("#search_ops").removeClass('show');
            return 0;
        }
        $.ajax({
            url: '/search/user',
            type: 'GET',
            data: {username: search_val, format: 'json'},
            dataType: 'json',
            success: updateSearchOption
        })

        function updateSearchOption(data) {
            if (data.length != 0) {
                list = $("#search_ops")
                list.empty();
                data.forEach(element => {
                    list_item = $("<a href='#'></a>").text(element.username);
                    list_item.attr('href', '/u/' + element.username);
                    list_item.click((e) => {
                        $('#search').val(e.target.innerHTML);
                    });
                    list_item.addClass('dropdown-item search-ops-item')
                    list.append(list_item);
                });
                if (!list.hasClass('show'))
                    list.addClass('show');
            } else {
                list.removeClass('show');
            }
        }
    });
});
