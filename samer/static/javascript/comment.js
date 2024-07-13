function submitFormOnEnter(event) {
    if (event.key === 'Enter') {
        event.preventDefault()
        document.getElementById('createCommentForm').submit()
    }
}

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}