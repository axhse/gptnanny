function beginWait(relatedButtonId = null, idsToDisable = null) {
    const fadingSpeed = 1000;
    if (idsToDisable !== null) {
        if (typeof idsToDisable === 'string') {
            idsToDisable = [idsToDisable];
        }
        for (let i = 0; i < idsToDisable.length; i++) {
            $('#' + idsToDisable[i]).prop('disabled', true);
        }
    }
    if (relatedButtonId === null) {
        return;
    }
    $('#' + relatedButtonId).addClass('button-task-wait');
}

function endWait(relatedButtonId = null, idsToEnable = null, hide = false) {
    const fadingSpeed = 300;
    if (idsToEnable !== null) {
        if (typeof idsToEnable === 'string') {
            idsToEnable = [idsToEnable];
        }
        for (let i = 0; i < idsToEnable.length; i++) {
            $('#' + idsToEnable[i]).prop('disabled', false);
        }
    }
    if (relatedButtonId === null) {
        return;
    }
    const relatedButton = $('#' + relatedButtonId);
    function removeLoader() {
        relatedButton.removeClass('button-task-wait');
    }
    if (hide) {
        relatedButton.addClass('button-task-hidden');
        relatedButton.stop().fadeTo(fadingSpeed, 0, removeLoader);
    } else {
        relatedButton.prop('disabled', false);
        removeLoader();
    }
}

function updateRequestButton(button, isVisible) {
    const fadingSpeed = 200;
    if (isVisible) {
        button.removeClass('button-task-hidden');
        button.prop('disabled', false);
        button.stop().fadeTo(fadingSpeed, 1);
    } else {
        button.prop('disabled', true);
        button.stop().fadeTo(fadingSpeed, 0);
    }
}

$(document).ready(function() {
    $('.request-block > input').on('input', function() {
        const hasValue = $(this).val() !== '';
        const requestButton = $(this).parent().find('button');
        updateRequestButton(requestButton, hasValue);
    });

    $('textarea').on('input', function() {
        let newHeight = $(this).val().split('\n').length;
        if (newHeight < 4) {
            newHeight = 4;
        }
        $(this).attr('rows', newHeight);
    });
    $('textarea').trigger('input');
});
