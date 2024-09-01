const textarea = document.querySelector(".descriptions-form");
textarea.addEventListener("keyup", e => {
    let scHeight = e.target.scrollHeight;
    textarea.style.height = `${scHeight}px`;
});

document.querySelector('.overlay-icon').addEventListener('click', function() {
    document.querySelector('.image-url-form').click();
});