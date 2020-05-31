function email_validation() {
  $.ajax({
    type: 'POST',
    url: '/emails',
    data: '{}',
    dataType: 'json',
    contentType: 'application/json',
    success: function (emails) {
      for (const email of emails) {
        if (email === $('#email').val()) {
          $('#email').css('border-color', 'red');
          $('#email').after('<p>email ya usado</p>');
        } else {
          $('#email + p').remove();
          $('#email').css('border-color', 'initial');
        }
      }
    }
  });
}

