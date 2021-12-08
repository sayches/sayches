$('.remove-space').on({
    keydown: function(e) {
      if (e.which === 32)
        return false;
    },
    change: function() {
      this.value = this.value.replace(/\s/g, "");
    }
});

$('#generate_password').on('click', function (e) {
  let random_password = Math.random().toString(36).substr(2, 10);
  random_password;
  $('#reg-pass').val(random_password);
})

$('#generate_username').on('click', function (e) {
  let random_username = Math.random().toString(36).substr(2, 10);
  random_username = '@' + random_username;
  $('#reg-name').val(random_username);
})