const carousel = document.querySelector('.carousel-images');
let scrollAmount = 0;

function carouselScrollRight() {
    const maxScroll = carousel.scrollWidth - carousel.clientWidth;
    if (scrollAmount < maxScroll) {
        scrollAmount += carousel.clientWidth;
        if (scrollAmount > maxScroll) {
            scrollAmount = maxScroll;
        }
        carousel.style.transform = `translateX(-${scrollAmount}px)`;
    }
    updateButtons();
}

function carouselScrollLeft() {
    if (scrollAmount > 0) {
        scrollAmount -= carousel.clientWidth;
        if (scrollAmount < 0) {
            scrollAmount = 0;
        }
        carousel.style.transform = `translateX(-${scrollAmount}px)`;
    }
    updateButtons();
}

function updateButtons() {
    console.log()
    document.querySelector('.prev').disabled = scrollAmount <= 0;
    document.querySelector('.next').disabled = scrollAmount >= carousel.scrollWidth - carousel.clientWidth;
}

updateButtons();
