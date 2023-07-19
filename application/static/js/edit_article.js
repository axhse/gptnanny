function isValidInput(elementSelector) {
    return $(elementSelector).val() !== '';
}

$(document).ready(function() {
    const activeElements = [
        'buttonSave',
        'buttonDelete',
        'titleInput',
        'hrefInput',
        'contentInput',
    ];

    $('#buttonSave').click(async function() {
        const animationDuration = 300;
        const body = {
            id: $('#idInput').val(),
            title: $('#titleInput').val(),
            href: $('#hrefInput').val(),
            content: $('#contentInput').val(),
        };
        beginWait('buttonSave', activeElements);
        await $.ajax({
            url: '/article/update',
            type: 'POST',
            headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
            data: JSON.stringify(body),
            contentType: 'application/json; charset=utf-8',
            timeout: 40000,  // 40 seconds
            success: function(savedData) {
                endWait('buttonSave', activeElements.slice(1), true);
                if (savedData !== null && savedData !== '') {
                    $('#idInput').val(savedData['id']);
                }
            },
            error: function() {
                endWait('buttonSave', activeElements);
            },
        });
    });

    $('#buttonDelete').click(async function() {
        beginWait('buttonDelete', activeElements);
        await $.ajax({
            url: '/article/delete',
            type: 'POST',
            headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
            data: { id: $('#idInput').val() },
            timeout: 30000,  // 30 seconds
            success: function() {
                location.replace('/articles');
            },
            error: function() {
                stopWaiting('buttonDelete', activeElements);
            },
        });
    });

    var isInitial = true;
    $('input, textarea').on('input', function() {
        $(this).each(function() {
            if ($(this).prop('id') === 'idInput') {
                return;
            }
            if (isValidInput(this)) {
                $(this).removeClass('input-error');
            } else {
                $(this).addClass('input-error');
            }
        });
        const isValid = $('.input-error').length === 0;
        if (!isInitial) {
            $('#buttonSave').prop('disabled', isValid);
            updateRequestButton($('#buttonSave'), isValid);
        }
    });
    $('input, textarea').trigger('input');
    isInitial = false;
});
