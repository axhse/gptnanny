$(document).on('keypress', function(e) {
    if (e.which == 13) {
        $('#submit').click();
    }
});

async function loginByToken(successUrl) {
    const animationDuration = 400;
    let token = document.getElementById('tokenInput').value;
    if (token === null || token === '') {
        return;
    }
    removeMessage('tokenForm');
    startWaiting('submit', 'loaderBlock');
    await $.ajax({
        url: '/check_token',
        type: 'POST',
        headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
        data: {
            token: token,
        },
        timeout: 20000,  // 20 seconds
        success: function() {
            let urlParams = new URLSearchParams(location.search);
            let returnUrl = urlParams.get('next');
            if (returnUrl === null || returnUrl == '') {
                returnUrl = successUrl;
            }
            location.replace(returnUrl);
        },
        error: function() {
            stopWaiting('submit', 'loaderBlock');
            addMessage('tokenForm', 'Invalid token');
        },
    });
}
