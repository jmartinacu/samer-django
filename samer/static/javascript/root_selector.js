const protocol = window.location.protocol;
const hostname = window.location.hostname;
const port = window.location.port;

const selectedRows = [];

function toggleSelection(checkbox, postId) {
    if (checkbox.checked) {
        selectedRows.push(postId);
    } else {
        const index = selectedRows.indexOf(postId);
        if (index > -1) {
            selectedRows.splice(index, 1);
        }
    }
}

function toggleActions() {
    const deleteAction = document.querySelector('.delete-action')
    const tagAction = document.querySelector('.tag-action')
    const archiveAction = document.querySelector('.archive-action')
    if (selectedRows.length === 0) {
        deleteAction.classList.add('disabled-link');
        deleteAction.setAttribute('aria-disabled', 'true');
        if (tagAction !== null) {
            tagAction.classList.add('disabled-link');
            tagAction.setAttribute('aria-disabled', 'true');
        }
        if (archiveAction !== null) {
            archiveAction.classList.add('disabled-link');
            archiveAction.setAttribute('aria-disabled', 'true');
        }
    } else {
        deleteAction.classList.remove('disabled-link');
        deleteAction.setAttribute('aria-disabled', 'false');
        if (tagAction !== null) {
            tagAction.classList.remove('disabled-link');
            tagAction.setAttribute('aria-disabled', 'false');
        }
        if (archiveAction !== null) {
            archiveAction.classList.remove('disabled-link');
            archiveAction.setAttribute('aria-disabled', 'false');
        }
    }
}

function deleteAction() {
    console.log("Action triggered: ", `/root/actions/delete/${MODEL}`)
    fetch(`/root/actions/delete/${MODEL}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify({ delete_ids: selectedRows })
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

function tagAction() {
    const post_ids = selectedRows.join(",");
    fetch(`/root/actions/tag?post_ids=${encodeURIComponent(post_ids)}`, {
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
}

function archiveAction(question_ids) {
    console.log(question_ids)
    fetch(`${protocol}//${hostname}:${port}/questions/archive/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify({ question_ids: question_ids })
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.text();
        }
    }).catch((error) => {
        console.error('Error:', error);
    });
}