


function deal() {
    axios.get("http://127.0.0.1:8000/api/game/234/deal")
        .then(d => d.data)
        .then(data => {
            let player_cards = document.querySelector("#player_cards");
            player_cards.innerHTML = data.hand;
            let player_score = document.querySelector("#player_score")
            player_score.innerHTML = data.score;
            let outcome = document.querySelector("#outcome")
            outcome.innerHTML = data.winner;
        })
}

let hitButton = document.querySelector("#hit");
hitButton.onclick = () => deal();


function restart_game(){
    axios.delete("http://127.0.0.1:8000/api/game/234/restart").then(() => {
        window.location.reload();
    });
}

let restartButton = document.querySelector("#restart");
restartButton.onclick = () => restart_game();


function stand(){
    axios.get("http://127.0.0.1:8000/api/game/234/stand")
        .then(d => d.data)
        .then(data => {
            let dealer_cards = document.querySelector("#dealer_cards");
            dealer_cards.innerHTML = data.hand;
            let outcome = document.querySelector("#outcome")
            outcome.innerHTML = data.winner;
        })
}

let standButton = document.querySelector("#stand");
standButton.onclick = () => stand();