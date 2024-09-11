const selectedOption = document.querySelector('.search-criteria');
const dropdownContent = document.querySelector('.dropdown-content');

const searchOptions = {
    Comentarios: '<button class="dropbtn" onclick="handleOption(this)">Comentarios</button>',
    Preguntas: '<button class="dropbtn" onclick="handleOption(this)">Preguntas</button>',
};

function showOptions() {
    if (!Object.keys(searchOptions).includes(selectedOption.textContent)) {
        selectedOption.textContent = "Comentarios";
    }
    dropdownContent.innerHTML = '';
    for (const [key, value] of Object.entries(searchOptions)) {
        if (key !== selectedOption.textContent) {
            dropdownContent.innerHTML += value;
        }
    }
};

function handleOption(button) {
    let content = "comments"
    if (button.textContent == "Preguntas") {
        content = "questions"
    }
    fetch(`${window.location.href}?content=${encodeURIComponent(content)}`, {
        method: 'GET',
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            window.location.href = response.url;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};