$('.prevent_multiple').click(function() {
    $(this).prop('disabled', true);
    $(this).parents('form:first').submit();
});