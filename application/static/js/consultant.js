async function ask() {
    let button = document.getElementById('searchButton');
    button.disabled = true;
    const loaderAnimationDuration = 1000;
    const answerAnimationDuration = 600;
    let loaderBlock = document.getElementById('loaderBlock');
    let answerBlock = document.getElementById('answerBlock');
    let sourceBlock = document.getElementById('sourceBlock');
    answerBlock.hidden = true;
    sourceBlock.hidden = true;
    addLoader(loaderBlock);
    showSlowly(loaderBlock, loaderAnimationDuration);
    let question = document.getElementById('questionInput').value;
    csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    await $.ajax({
        url: '/ask',
        type: 'POST',
        data: {
            question: question,
            csrfmiddlewaretoken: csrfToken,
        },
        timeout: 40000,  // 40 seconds
        success: function(answer) {
            loaderBlock.hidden = true;
            removeLoader(loaderBlock);
            answerBlock.innerHTML = answer['message'];
            showSlowly(answerBlock, answerAnimationDuration);
            if (answer['sources'].length > 0) {
                let sourceLink = document.getElementById('sourceLink');
                sourceLink.innerHTML = answer['sources'][0]['title'];
                sourceLink.href = answer['sources'][0]['href'];
                showSlowly(sourceBlock, answerAnimationDuration);
            }
            button.disabled = false;
        },
        error: function() {
            loaderBlock.hidden = true;
            removeLoader(loaderBlock);
            button.disabled = false;
        },
        complete: function() {
            loaderBlock.hidden = true;
            removeLoader(loaderBlock);
            button.disabled = false;
        },
    });
}
