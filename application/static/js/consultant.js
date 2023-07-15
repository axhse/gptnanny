async function ask() {
    const animationDuration = 600;
    let body = {
        question: document.getElementById('questionInput').value,
    }
    startWaiting('searchButton', 'loaderBlock');
    let answerBlock = document.getElementById('answerBlock');
    let sourceBlock = document.getElementById('sourceBlock');
    answerBlock.hidden = true;
    sourceBlock.hidden = true;
    await $.ajax({
        url: '/ask',
        type: 'POST',
        headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
        data: JSON.stringify(body),
        contentType: 'application/json; charset=utf-8',
        timeout: 40000,  // 40 seconds
        success: function(answer) {
            stopWaiting('searchButton', 'loaderBlock');
            answerBlock.innerHTML = answer['message'];
            showSlowly(answerBlock, animationDuration);
            if (answer['articles'].length > 0) {
                let sourceLink = document.getElementById('sourceLink');
                sourceLink.innerHTML = answer['articles'][0]['title'];
                sourceLink.href = answer['articles'][0]['href'];
                showSlowly(sourceBlock, animationDuration);
            }
        },
        error: function() {
            stopWaiting('searchButton', 'loaderBlock');
        },
    });
}
