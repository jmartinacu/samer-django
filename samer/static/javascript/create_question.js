const protocol = window.location.protocol;
const hostname = window.location.hostname;
const port = window.location.port;

const titleInput = document.getElementById('title');
const contentInput = document.getElementById('content');
const tagInput = document.getElementById('tag-input');
const tagLabel = document.getElementById('tag-label');
const tagsContainer = document.getElementById('tags-input-container');
const hiddenTagField = document.getElementById('tag');

let tags = [];

function updateElementPosition() {
    if (tags.length > 0) {
        tagLabel.classList.add('fixed');
    } else {
        tagLabel.classList.remove('fixed');
    }
}

function createMessage(message) {
    fetch(`${protocol}//${hostname}:${port}/messages?level=warning&message=${message}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        const currentUrl = window.location.origin + window.location.pathname;
        let params = new URLSearchParams(window.location.search);
        if (titleInput.value !== '') {
            params.set('title', titleInput.value);
        }
        if (contentInput.value !== '') {
            params.set('content', contentInput.value);
        }
        window.location.href = currentUrl + '?' + params.toString();
        console.log("Mensaje enviado: ", data);
    })
    .catch(error => console.error("Error: ", error));
}

function addTag(tag) {
    if (tags.length == 5 ) {
        createMessage("No puede haber mas de cinco etiquetas")
        return
    }
    if (tag.length >= 14) {
        createMessage("Etiqueta demasiado larga")
        return
    }
    if (tag && !tags.includes(tag)) {
        tags.push(tag);
        updateElementPosition()
        const tagItem = document.createElement('span');
        tagItem.classList.add('tag-item');
        tagItem.textContent = tag;

        const removeButton = document.createElement('button');
        removeButton.textContent = 'x';
        removeButton.onclick = function() {
            removeTag(tag);
        };

        tagItem.appendChild(removeButton);
        tagsContainer.insertBefore(tagItem, tagInput);

        hiddenTagField.value = tags.join(',');

        tagInput.value = '';
    }
}

function removeTag(tag) {
    tags = tags.filter(t => t !== tag);

    updateElementPosition()
    Array.from(tagsContainer.children).forEach(item => {
        if (item.textContent.startsWith(tag)) {
            tagsContainer.removeChild(item);
        }
    });

    hiddenTagField.value = tags.join(',');
}

tagInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const tag = tagInput.value.trim();
        addTag(tag);
    }
});

tagsContainer.addEventListener('click', function() {
    tagInput.focus();
});