$(document).ready(function() {
    $('#requestButton').click(async function() {
        const fadingSpeed = 600;
        beginWait('requestButton', ['requestButton', 'questionInput']);
        const body = { question: $('#questionInput').val() };
        $('#answerBlock').stop().fadeTo(0, 0);
        await $.ajax({
            url: '/ask',
            type: 'POST',
            headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
            data: JSON.stringify(body),
            contentType: 'application/json; charset=utf-8',
            timeout: 40000,  // 40 seconds
            success: function(answer) {
                endWait('requestButton', 'questionInput', true);
                $('#messageBlock').text(answer['message']);
                if (answer['articles'].length > 0) {
                    $('#sourceLink').text(answer['articles'][0]['title']);
                    $('#sourceLink').prop('href', answer['articles'][0]['href']);
                }
                $('#answerBlock').stop().fadeTo(fadingSpeed, 1);
            },
            error: function() {
                endWait('requestButton', ['requestButton', 'questionInput']);
            },
        });
    });
});
