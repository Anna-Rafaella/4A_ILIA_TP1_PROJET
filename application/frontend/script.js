// Logique JavaScript pour interagir avec l'API
document.getElementById('calculForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Empêche le rechargement de la page lors de la soumission

    const a = document.getElementById('a').value;
    const b = document.getElementById('b').value;
    const operation = document.getElementById('operation').value;

    // Vérifie que les champs ne sont pas vides avant de continuer
    if (!a || !b || !operation) {
        alert('Veuillez remplir tous les champs.');
        return;
    }

    // Envoi de la requête POST à l'API
    fetch('http://localhost:5000/api/calcul', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ a: parseFloat(a), b: parseFloat(b), operation: operation })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur dans la requête POST : ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Requête POST réussie. ID du calcul :', data.id);
            checkResult(data.id); // Appelle la fonction pour surveiller le résultat
        })
        .catch(error => {
            console.error('Erreur lors de l’envoi du calcul :', error);
            alert('Erreur : Impossible d’envoyer le calcul.');
        });
});

function checkResult(id) {
    // Fonction pour récupérer le résultat depuis l'API
    fetch(`http://localhost:5000/api/calcul/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur dans la requête GET : ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.resultat) {
                // Affiche le résultat une fois disponible
                document.getElementById('resultat').innerText = ` ${data.resultat}`;
            } else {
                console.log('Résultat non prêt, réessaie dans 1 seconde...');
                setTimeout(() => checkResult(id), 1000); // Réessaie après 1 seconde
            }
        })
        .catch(error => {
            console.error('Erreur lors de la récupération du résultat :', error);
            document.getElementById('resultat').innerText =
                'Une erreur s’est produite lors de la récupération du résultat.';
        });
}
