async function saveArticle() {
    const animationDuration = 300;
    let body = {
        id: document.getElementById('idInput').value,
        title: document.getElementById('titleInput').value,
        href: document.getElementById('hrefInput').value,
        content: document.getElementById('contentInput').value,
    }
    startWaiting('buttonSave', 'savingLoader');
    let buttonSave = document.getElementById('buttonSave');
    let buttonDelete = document.getElementById('buttonDelete');
    buttonDelete.disabled = true;
    await $.ajax({
        url: '/article/update',
        type: 'POST',
        headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
        data: JSON.stringify(body),
        contentType: 'application/json; charset=utf-8',
        timeout: 40000,  // 40 seconds
        success: function(savedData) {
            stopWaiting('buttonSave', 'savingLoader');
            hideSlowly(buttonSave, animationDuration, false);
            buttonSave.disabled = true;
            buttonDelete.disabled = false;
            if (savedData !== null && savedData != '') {
                document.getElementById('idInput').value = savedData['id'];
            }
        },
        error: function() {
            stopWaiting('buttonSave', 'savingLoader');
            buttonDelete.disabled = false;
        },
    });
}

async function deleteArticle() {
    let id = document.getElementById('idInput').value;
    startWaiting('buttonDelete', 'deletionLoader');
    await $.ajax({
        url: '/article/delete',
        type: 'POST',
        headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
        data: {
            id: id,
        },
        timeout: 30000,  // 30 seconds
        success: function() {
            location.replace('/articles');
        },
        error: function() {
            stopWaiting('buttonDelete', 'deletionLoader');
        },
    });
}

function createArticle() {
    location.assign('/article/create');
}

function updateForm(keepSaveButtonHidden = false) {
    const animationDuration = 300;
    let titleInput = document.getElementById('titleInput');
    let hrefInput = document.getElementById('hrefInput');
    let contentInput = document.getElementById('contentInput');
    updateTextarea(contentInput);
    let hasError = false;
    if (titleInput.value === null || titleInput.value === '') {
        titleInput.classList.add('input-error');
        hasError = true;
    } else {
        titleInput.classList.remove('input-error');
    }
    if (hrefInput.value === null || hrefInput.value === '') {
        hrefInput.classList.add('input-error');
        hasError = true;
    } else {
        hrefInput.classList.remove('input-error');
    }
    if (contentInput.value === null || contentInput.value === '') {
        contentInput.classList.add('input-error');
        hasError = true;
    } else {
        contentInput.classList.remove('input-error');
    }
    buttonSave = document.getElementById('buttonSave');
    if (hasError) {
        hideSlowly(buttonSave, animationDuration, false);
        buttonSave.disabled = true;
    } else {
        if (!keepSaveButtonHidden) {
            showSlowly(buttonSave, animationDuration);
            buttonSave.disabled = false;
        }
    }
}

$( document ).ready(function() {
    updateForm(true);
});
