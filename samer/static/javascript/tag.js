const addPostButton = document.getElementById("search-button")
const searchPost = document.getElementById("search")
const dropdownContainer = document.getElementById("dropdown")

const protocol = window.location.protocol;
const hostname = window.location.hostname;
const port = window.location.port;

let timeout = null;

function handleSelectedPost(post) {
    fetch(`${protocol}//${hostname}:${port}/posts/tag/add/${TAG_ID}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify({ post_ids: [post["id"]] })
    })
    .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.text();
            }
        })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function handleSearchAnswer(posts) {
    dropdownContainer.innerHTML = '';
    if (posts && posts.length > 0) {
        posts.forEach(post => {
            if (TAG_POSTS.map(p => p["id"]).includes(post["id"])) {
                return
            }
            const dropdownElement = document.createElement('p');
            dropdownElement.textContent = post.name;
            dropdownElement.addEventListener('click', () => {
                handleSelectedPost(post);
            });
            dropdownContainer.appendChild(dropdownElement);
        });
    } else {
        dropdownContainer.innerHTML = '<p>No hay resultados</p>';
    }
}

addPostButton.addEventListener("click", () => {
    searchPost.style.display = "block"
})

searchPost.addEventListener('focus', () => {
        dropdownContainer.style.display = 'block';
    });

searchPost.addEventListener('blur', () => {
    // Usamos un pequeño delay para permitir el click en los elementos del dropdown
    setTimeout(() => {
        dropdownContainer.style.display = 'none';
    }, 200);
});

searchPost.addEventListener('input', () => {
    if (timeout) {
        clearTimeout(timeout);
    }

    timeout = setTimeout(() => {
        const post_name = searchPost.value;

        fetch(`${protocol}//${hostname}:${port}/posts/search?post_name=${post_name}`, {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            handleSearchAnswer(data)
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }, 1000);
});