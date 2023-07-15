function insertAfter(element, prevElement) {
    var parent = prevElement.parentNode;
    if (parent.lastChild == prevElement) {
        parent.appendChild(element);
    } else {
        parent.insertBefore(element, prevElement.nextSibling);
    }
}

function removeMessage(forId) {
    let forElem = document.getElementById(forId);
    if (forElem.nextSibling === null) {
        return;
    }
    if (forElem.nextSibling.classList === undefined) {
        return;
    }
    if (forElem.nextSibling.classList.contains('msg')) {
        forElem.nextSibling.remove();
    }
}

function addMessage(forId, message) {
    removeMessage(forId);
    let forElem = document.getElementById(forId);
    let errorSpan = document.createElement('span');
    errorSpan.classList.add('msg');
    errorSpan.innerHTML = message;
    insertAfter(errorSpan, forElem);
}
