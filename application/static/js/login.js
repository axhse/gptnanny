async function loginByToken(successUrl) {
    $('#errorMessage').addClass('concealed');
    beginWait('requestButton', ['requestButton', 'tokenInput']);
    await $.ajax({
        url: '/check_token',
        type: 'POST',
        headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
        data: { token: $('#tokenInput').val() },
        timeout: 20000,  // 20 seconds
        success: function() {
            let returnUrl = new URLSearchParams(location.search).get('next');
            if (returnUrl === null || returnUrl === '') {
                returnUrl = successUrl;
            }
            location.replace(returnUrl);
        },
        error: function() {
            endWait('requestButton', ['requestButton', 'tokenInput']);
            $('#errorMessage').text('Invalid token');
            $('#errorMessage').removeClass('concealed');
        },
    });
}

$(document).on('keypress', function(event) {
    if (event.which == 13) {
        $('#requestButton').click();
    }
});
