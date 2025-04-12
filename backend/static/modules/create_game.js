function createGame() {
    fetch('/organizer/{{ organizer_id }}/create-game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: 'test'
        })
    }).then(response => response.json())
    .then(data => {
        console.log(data);
    })
};

