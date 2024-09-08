document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');

    messages.forEach(function(message) {
        message.addEventListener('click', function() {
            this.style.display = 'none';
        });
    });
});