function showSlowly(element, duration) {
    if (!element.hidden && element.style.opacity != '0') {
        return;
    }
    element.style.opacity = 0;
    element.hidden = false;
    let factor = 25;
    if (duration <= 200) {
        factor = 10;
    }
    if (duration <= 50) {
        factor = 4;
    }
    let iterationIndex = 0;
    function nextFrame() {
        let newOpacity = parseFloat(element.style.opacity) + 1 / factor;
        if (newOpacity > 1) {
            newOpacity = 1;
        }
        element.style.opacity = newOpacity;
        ++iterationIndex;
        if (iterationIndex < factor) {
            setTimeout(nextFrame, duration / factor);
        }
    }
    nextFrame();
}

function hideSlowly(element, duration, makeHidden = true) {
    if (element.hidden || element.style.opacity != '1') {
        return;
    }
    element.style.opacity = 1;
    let factor = 25;
    if (duration <= 200) {
        factor = 10;
    }
    if (duration <= 50) {
        factor = 4;
    }
    function nextFrame() {
        if (element.style.opacity == '0') {
            if (makeHidden) {
                element.hidden = true;
            }
            return;
        }
        let newOpacity = parseFloat(element.style.opacity) - 1 / factor;
        if (newOpacity < 0) {
            newOpacity = 0;
        }
        element.style.opacity = newOpacity;
        setTimeout(nextFrame, duration / factor);
    }
    nextFrame();
}

function addLoader(loaderBlock) {
    let loader = document.createElement('div');
    loader.classList.add('loader');
    loaderBlock.appendChild(loader);
}

function removeLoader(loaderBlock) {
	for (let i = loaderBlock.children.length - 1; i >= 0; i--) {
        loaderBlock.children[i].remove();
	}
}

function startWaiting(buttonId, loaderBlockId) {
    const animationDuration = 1000;
    let button = document.getElementById(buttonId);
    let loaderBlock = document.getElementById(loaderBlockId);
    button.disabled = true;
    addLoader(loaderBlock);
    showSlowly(loaderBlock, animationDuration);
}

function stopWaiting(buttonId, loaderBlockId) {
    let button = document.getElementById(buttonId);
    let loaderBlock = document.getElementById(loaderBlockId);
    loaderBlock.hidden = true;
    removeLoader(loaderBlock);
    button.disabled = false;
}

function updateSearchBar(searchInput) {
    const animationDuration = 300;
    searchBar = searchInput.parentElement;
	let hasValue = false;
	for (let i = 0; i < searchBar.children.length; i++) {
	    let child = searchBar.children[i];
	    if (child.tagName !== 'INPUT') {
	        continue;
	    }
	    hasValue = child.value !== null && child.value !== '';
	}
	for (let i = 0; i < searchBar.children.length; i++) {
	    let child = searchBar.children[i];
	    if (child.tagName !== 'BUTTON') {
	        continue;
	    }
	    if (hasValue && child.hidden) {
	        showSlowly(child, animationDuration);
	    }
	    if (!hasValue && !child.hidden) {
	        hideSlowly(child, animationDuration);
	    }
	}
}

function updateTextarea(textarea) {
    let newRows = 0;
    if (textarea.value !== null) {
        newRows = textarea.value.split('\n').length;
    }
    if (newRows < 4) {
        newRows = 4;
    }
    textarea.rows = newRows;
}
