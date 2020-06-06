$(document).ready(function () {

  $('#email').change(function () {
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
  });

  $('#password').keyup(function () {
    $('#check_pass').html(checkStrengthPass($('#password').val()));
  });

  function checkStrengthPass(pass) {
    let strength = 0;
    if (pass.length > 0 && pass.length < 6) {
      $('#check_pass').removeClass();
      $('#check_pass').addClass('Short');
      $('#signup').prop('disabled', true);
      return 'Too short';
    }
    if (pass.length > 7) { strength += 1 }
    // If password contains both lower and uppercase characters, increase strength value.
    if (pass.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) { strength += 1 }
    // If it has numbers and characters, increase strength value.
    if (pass.match(/([a-zA-Z])/) && pass.match(/([0-9])/)) { strength += 1 }
    // If it has one special character, increase strength value.
    if (pass.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) { strength += 1 }
    // If it has two special characters, increase strength value.
    if (pass.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) {strength += 1}

    if (strength === 0) {
      $('#check_pass').removeClass();
      return '';
    } else if (strength < 2) {
      $('#check_pass').removeClass();
      $('#check_pass').addClass('Weak');
      $('#signup').prop('disabled', false);
      return 'Weak';
    } else if (strength == 2) {
      $('#check_pass').removeClass();
      $('#check_pass').addClass('Good');
      $('#signup').prop('disabled', false);
      return 'Good';
    } else {
      $('#check_pass').removeClass();
      $('#check_pass').addClass('Strong');
      $('#signup').prop('disabled', false);
      return 'Strong';
    }
  }

  $('#confirm').change(function () {
    const pass1 = $('#password').val();
    const pass2 = $('#confirm').val();
    $('#confirm + p').remove();
    $('#confirm').css('border-color', 'initial');
    if (pass1 !== pass2) {
      $('#confirm').css('border-color', '#F00');
      $('#password').css('border-color', '#F00');
      $('#confirm').after('<p class="red">No coinciden las contraseñas</p>');
    } else {
      $('#confirm + p').remove();
      $('#confirm').css('border-color', 'initial');
      $('#password').css('border-color', 'initial');
    }
  });
  $('.menu-list').click(() => $('#menu').animate({'margin-left': '0'}, 'slow'));
  $('.close').click(() => $('#menu').animate({'margin-left': '-=100vw'}, 'slow'));
});

