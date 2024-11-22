// Logique JavaScript pour interagir avec l'API
document.getElementById('calculForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const a = document.getElementById('a').value;
    const b = document.getElementById('b').value;
    const operation = document.getElementById('operation').value;

    // Envoi de la requête POST à l'API
    fetch('http://localhost:5000/api/calcul', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ a: parseFloat(a), b: parseFloat(b), operation: operation })
    })
    .then(response => response.json())
    .then(data => {
        const calcul_id = data.id;
        checkResult(calcul_id);
    });
});

function checkResult(id) {
    // Récupération du résultat
    fetch(`http://localhost:5000/api/calcul/${id}`)
    .then(response => response.json())
    .then(data => {
        if (data.resultat) {
            document.getElementById('resultat').innerText = data.resultat;
        } else {
            setTimeout(() => checkResult(id), 1000); // Réessaie après 1 seconde
        }
    });
}
