const textarea = document.getElementById('create-comment-form');

function submitFormOnEnter(event) {
    if (event.key === 'Enter') {
        event.preventDefault()
        document.getElementById('createCommentForm').submit()
    }
}

function textareaKeyEvents(event) {
  if (event.key === 'Enter' && event.ctrlKey) {
    event.preventDefault()
    document.getElementById('createCommentForm').submit()
  }
}

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

textarea.addEventListener('keydown', textareaKeyEvents);
