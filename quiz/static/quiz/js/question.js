document.addEventListener('DOMContentLoaded', () => {
    console.log('document loading')

    const upvotebtn = document.getElementById('upvote-btn')
    const downvotebtn = document.getElementById('downvote-btn')
    const qid = document.getElementById('qid').value
    console.log('qid:', qid)

    upvotebtn.addEventListener('click', () => {
        console.log('upvote')
        upvotebtn.disabled = true
        upvotebtn.classList.add('disabled')
        downvotebtn.disabled = false
        downvotebtn.classList.remove('disabled')
        updatevotecount(qid, 1)
    })

    downvotebtn.onclick = () => {
        console.log('downvote')
        upvotebtn.disabled = false
        upvotebtn.classList.remove('disabled')

        downvotebtn.disabled = true
        downvotebtn.classList.add('disabled')
        updatevotecount(qid, -1)
    }
})

async function delete_comment(cid) {
    const url = `/delete-comment/${cid}/`
    const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        }
    })
    const commentElement = document.getElementById(`c${cid}`)

    if (commentElement) {
        commentElement.classList.add('fade-out');

        commentElement.addEventListener('transitionend', () => {
            commentElement.remove();
        });
    }
}

async function updatevotecount(qid, change) {
    const url = `/update_vote/${qid}/`
    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ 'votechange': change }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.log('Vote updated successfully:', data.new_vote_count);
                // Optionally update the vote count display in your UI
                // document.getElementById(`vote-count-${questionId}`).innerText = data.new_vote_count;
                document.getElementById('nvotes').innerHTML = data.new_vote_count
            } else {
                console.error('Failed to update vote:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the CSRF token name?
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
