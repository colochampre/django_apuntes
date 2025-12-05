document.addEventListener('DOMContentLoaded', function() {
    // Obtener el token CSRF
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
    const csrftoken = getCookie('csrftoken');

    // Manejar clics en las estrellas
    const estrellasBtn = document.querySelectorAll('.estrella-btn');
    console.log('Estrellas encontradas:', estrellasBtn.length);
    console.log('CSRF Token:', csrftoken);
    
    estrellasBtn.forEach(estrella => {
        estrella.addEventListener('click', function() {
            const valor = this.getAttribute('data-valor');
            const apunteId = this.getAttribute('data-apunte-id');
            
            console.log('Click en estrella - Valor:', valor, 'Apunte ID:', apunteId);
            
            // Enviar puntuación al servidor
            fetch(`/apuntes/puntuar/${apunteId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken
                },
                body: `valor=${valor}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar la visualización del promedio
                    const apunteItem = document.querySelector(`.apunte-item[data-apunte-id="${apunteId}"]`);
                    const displayDiv = apunteItem.querySelector('.puntuacion-display');
                    
                    // Actualizar estrellas del promedio
                    let estrellasHTML = '<span class="promedio-estrellas">';
                    const promedio = data.promedio;
                    for (let i = 1; i <= 5; i++) {
                        if (i <= Math.floor(promedio)) {
                            estrellasHTML += '<span class="estrella llena">★</span>';
                        } else if (i - 1 < promedio) {
                            estrellasHTML += '<span class="estrella media">★</span>';
                        } else {
                            estrellasHTML += '<span class="estrella vacia">☆</span>';
                        }
                    }
                    estrellasHTML += '</span>';
                    estrellasHTML += `<span class="promedio-numero">(${promedio}/5 - ${data.total} valoraciones)</span>`;
                    
                    displayDiv.innerHTML = estrellasHTML;
                    
                    // Actualizar estrellas del usuario
                    const estrellasUsuario = apunteItem.querySelectorAll('.estrella-btn');
                    estrellasUsuario.forEach((est, index) => {
                        if (index < valor) {
                            est.classList.add('activa');
                        } else {
                            est.classList.remove('activa');
                        }
                    });
                    
                    // Mostrar mensaje de éxito
                    console.log(data.mensaje);
                } else {
                    alert('Error al puntuar: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al enviar la puntuación');
            });
        });
        
        // Efecto hover para mostrar las estrellas que se seleccionarían
        estrella.addEventListener('mouseenter', function() {
            const valor = parseInt(this.getAttribute('data-valor'));
            const apunteId = this.getAttribute('data-apunte-id');
            const contenedor = this.parentElement;
            const todasEstrellas = contenedor.querySelectorAll('.estrella-btn');
            
            todasEstrellas.forEach((est, index) => {
                if (index < valor) {
                    est.style.color = '#ffc107';
                } else {
                    est.style.color = '#ccc';
                }
            });
        });
        
        estrella.parentElement.addEventListener('mouseleave', function() {
            const todasEstrellas = this.querySelectorAll('.estrella-btn');
            todasEstrellas.forEach(est => {
                est.style.color = '';
            });
        });
    });
});
