async function login(successUrl) {
    $('#usernameMessage').addClass('concealed');
    $('#passwordMessage').addClass('concealed');
    beginWait('requestButton', ['requestButton', 'usernameInput', 'passwordInput']);
    const params = {
        username: $('#usernameInput').val(),
        password: $('#passwordInput').val(),
    };
    await $.ajax({
        url: '/login',
        type: 'POST',
        headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
        data: params,
        timeout: 20000,  // 20 seconds
        success: function() {
            let returnUrl = new URLSearchParams(location.search).get('next');
            if (returnUrl === null || returnUrl === '') {
                returnUrl = successUrl;
            }
            location.replace(returnUrl);
        },
        statusCode: {
            403: function() {
                endWait('requestButton', ['requestButton', 'usernameInput', 'passwordInput']);
                $('#passwordMessage').text('Неправильный пароль');
                $('#passwordMessage').removeClass('concealed');
            },
            404: function() {
                endWait('requestButton', ['requestButton', 'usernameInput', 'passwordInput']);
                $('#usernameMessage').text('Пользователь не найден');
                $('#usernameMessage').removeClass('concealed');
            },
        },
    });
}

$(document).on('keypress', function(event) {
    if (event.which == 13) {
        $('#requestButton').click();
    }
});
