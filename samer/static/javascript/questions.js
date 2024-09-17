const protocol = window.location.protocol;
const hostname = window.location.hostname;
const port = window.location.port;

const questionsContent = document.querySelector('.questions-content');
const searchBar = document.getElementById("search-questions");
const selectedOption = document.querySelector('.search-criteria');
const dropdownContent = document.querySelector('.dropdown-content');

const searchOptions = {
    Resueltas: '<button onclick="handleOption(this)">Resueltas</button>',
    Autor: '<button onclick="handleOption(this)">Autor</button>',
    Contenido: '<button onclick="handleOption(this)">Contenido</button>',
    Titulo: '<button onclick="handleOption(this)">Titulo</button>',
    Etiqueta: '<button onclick="handleOption(this)">Etiqueta</button>',
};

searchBar.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        searchQuestions();
    }
});

function showOptions() {
    if (!Object.keys(searchOptions).includes(selectedOption.textContent)) {
        selectedOption.textContent = "Titulo";
    }
    dropdownContent.innerHTML = '';
    for (const [key, value] of Object.entries(searchOptions)) {
        if (key !== selectedOption.textContent) {
            dropdownContent.innerHTML += value;
        }
    }
};

function handleOption(button) {
    const html_option = button.textContent;
    selectedOption.textContent = html_option;
};

function searchQuestions() {
    const html_option = selectedOption.textContent;
    let option = "";
    if (html_option === "Resueltas") {
        option = "resolved";
    } else if (html_option === "Autor") {
        option = "author";
    } else if (html_option === "Contenido") {
        option = "content";
    } else if (html_option === "Titulo") {
        option = "title";
    } else if (html_option === "Etiqueta") {
        option = "tag";
    }
    let search = searchBar.value;
    if (option === "resolved") {
        search = "";
    }
    fetch(`${protocol}//${hostname}:${port}/questions?option=${option}&search=${search}`, {
        method: 'GET',
    })
    .then(
        response => response.text()
    ).then(html => {
        const parser = new DOMParser();
        const questionsHtml = parser.parseFromString(html, 'text/html');
        const questionsSection = questionsHtml.querySelector('.questions-content');
        if (questionsSection) {
            console.log("Se encontró la sección de preguntas");
            questionsContent.innerHTML = questionsSection.innerHTML;
        } else {
            return Error('No se encontró la sección de preguntas');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};

function showAnswer(question_id) {
    window.location.href = `${protocol}//${hostname}:${port}/questions/${question_id}`
}