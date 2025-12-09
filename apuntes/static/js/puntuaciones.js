document.addEventListener('DOMContentLoaded', function() {
    const estrellasInteractivas = document.querySelectorAll('.estrella-btn');

    estrellasInteractivas.forEach(function(estrella) {
        estrella.addEventListener('click', function() {
            const valor = parseInt(this.getAttribute('data-valor'));
            const apunteId = parseInt(this.getAttribute('data-apunte-id'));
            const card = this.closest('.apunte-card');
            
            // Enviar puntuación al servidor
            fetch(`/apuntes/puntuar/${apunteId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `valor=${valor}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar las estrellas del usuario
                    const estrellas = card.querySelectorAll('.estrella-btn');
                    estrellas.forEach(function(est, index) {
                        if (index < valor) {
                            est.classList.add('activa');
                        } else {
                            est.classList.remove('activa');
                        }
                    });

                    // Actualizar el promedio y total de puntuaciones
                    const puntuacionDisplay = card.querySelector('.puntuacion-display');
                    if (data.promedio) {
                        const estrellaPromedio = puntuacionDisplay.querySelector('.estrellas-promedio');
                        const puntuacionPromedio = puntuacionDisplay.querySelector('.puntuacion-promedio');
                        const puntuacionVotos = puntuacionDisplay.querySelector('.puntuacion-votos');
                        
                        if (!estrellaPromedio) {
                            // Si no había puntuaciones antes, crear la estructura
                            puntuacionDisplay.innerHTML = `
                                <span class="puntuacion-promedio">${data.promedio.toFixed(1)}</span>
                                <div class="estrellas-promedio">
                                    ${generarEstrellas(data.promedio)}
                                </div>
                                <span class="puntuacion-votos">(${data.total})</span>
                            `;
                        } else {
                            // Actualizar las estrellas existentes
                            estrellaPromedio.innerHTML = generarEstrellas(data.promedio);
                            puntuacionPromedio.textContent = data.promedio.toFixed(1);
                            puntuacionVotos.textContent = `(${data.total})`;
                        }
                    }
                } else {
                    console.error('Error al puntuar:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });

        // Efecto hover para las estrellas
        estrella.addEventListener('mouseenter', function() {
            const valor = parseInt(this.getAttribute('data-valor'));
            const card = this.closest('.apunte-card');
            const estrellas = card.querySelectorAll('.estrella-btn');
            
            estrellas.forEach(function(est, index) {
                if (index < valor) {
                    est.style.color = '#ffc107';
                } else {
                    est.style.color = '#ddd';
                }
            });
        });

        estrella.addEventListener('mouseleave', function() {
            const card = this.closest('.apunte-card');
            const estrellas = card.querySelectorAll('.estrella-btn');
            
            estrellas.forEach(function(est) {
                if (est.classList.contains('activa')) {
                    est.style.color = '#ffc107';
                } else {
                    est.style.color = '#ddd';
                }
            });
        });
    });
});

// Función para generar HTML de estrellas según el promedio
function generarEstrellas(promedio) {
    let html = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= promedio) {
            html += '<i class="bi bi-star-fill estrella llena"></i>';
        } else if (i - 0.5 <= promedio) {
            html += '<i class="bi bi-star-half estrella media"></i>';
        } else {
            html += '<i class="bi bi-star estrella vacia"></i>';
        }
    }
    return html;
}

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
