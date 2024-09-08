const textarea = document.getElementById('create-comment-form');

function textareaKeyEvents(event) {
  if (event.key === 'Enter' && event.shiftKey) {
    event.preventDefault();
    const start = this.selectionStart;
    const end = this.selectionEnd;
    const value = this.value;
    this.value = value.substring(0, start) + '\n' + value.substring(end);
    this.selectionStart = this.selectionEnd = start + 1;
  }
  else if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    document.getElementById('createCommentForm').submit();
  }
}

textarea.addEventListener('keydown', textareaKeyEvents);
