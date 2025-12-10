/**
 * Sistema de Filtrado y Ordenamiento de Apuntes
 */

document.addEventListener('DOMContentLoaded', function () {
    const filtrosButtons = document.querySelectorAll('.filtro-btn');
    const apuntesGrid = document.querySelector('.apuntes-grid');

    if (!apuntesGrid || filtrosButtons.length === 0) return;

    // Obtener todas las tarjetas de apuntes
    let apuntesCards = Array.from(apuntesGrid.querySelectorAll('.apunte-card-wrapper'));

    filtrosButtons.forEach(button => {
        button.addEventListener('click', function () {
            const filtro = this.dataset.filtro;
            let orden = this.dataset.orden;

            // Si el botón ya está activo, alternar el orden
            if (this.classList.contains('active')) {
                orden = orden === 'asc' ? 'desc' : 'asc';
                this.dataset.orden = orden;
            } else {
                // Desactivar todos los botones
                filtrosButtons.forEach(btn => btn.classList.remove('active'));
                // Activar el botón clickeado
                this.classList.add('active');
            }
            // Actualizar ícono del filtro de nombre según el orden
            if (filtro === 'nombre') {
                const iconoNombre = this.querySelector('i:first-child');
                if (orden === 'asc') {
                    iconoNombre.className = 'bi bi-sort-alpha-up-alt';
                } else {
                    iconoNombre.className = 'bi bi-sort-alpha-down-alt';
                }
            }

            // Aplicar ordenamiento
            ordenarApuntes(filtro, orden);
        });
    });

    function ordenarApuntes(filtro, orden) {
        // Clonar el array para no mutar el original
        const apuntesOrdenados = [...apuntesCards];

        apuntesOrdenados.sort((a, b) => {
            let valorA, valorB;

            switch (filtro) {
                case 'nombre':
                    valorA = a.querySelector('.apunte-titulo').textContent.trim().toLowerCase();
                    valorB = b.querySelector('.apunte-titulo').textContent.trim().toLowerCase();
                    break;

                case 'fecha':
                    // Obtener fecha del atributo data o del texto
                    const fechaTextA = a.querySelector('.apunte-fecha').textContent.trim();
                    const fechaTextB = b.querySelector('.apunte-fecha').textContent.trim();
                    valorA = parsearFecha(fechaTextA);
                    valorB = parsearFecha(fechaTextB);
                    break;

                case 'puntuacion':
                    const puntuacionA = a.querySelector('.puntuacion-promedio');
                    const puntuacionB = b.querySelector('.puntuacion-promedio');
                    valorA = puntuacionA ? parseFloat(puntuacionA.textContent) : 0;
                    valorB = puntuacionB ? parseFloat(puntuacionB.textContent) : 0;
                    break;

                case 'tipo':
                    const extensionA = a.querySelector('.file-extension');
                    const extensionB = b.querySelector('.file-extension');
                    valorA = extensionA ? extensionA.textContent.trim().toLowerCase() : 'zzz';
                    valorB = extensionB ? extensionB.textContent.trim().toLowerCase() : 'zzz';
                    break;

                case 'tamano':
                    const sizeA = a.querySelector('.file-size');
                    const sizeB = b.querySelector('.file-size');
                    valorA = sizeA ? parsearTamano(sizeA.textContent) : 0;
                    valorB = sizeB ? parsearTamano(sizeB.textContent) : 0;
                    break;

                default:
                    return 0;
            }

            // Comparar valores
            let comparacion = 0;
            if (valorA > valorB) comparacion = 1;
            if (valorA < valorB) comparacion = -1;

            // Aplicar orden ascendente o descendente
            return orden === 'asc' ? comparacion : -comparacion;
        });

        // Limpiar el grid y re-agregar en el nuevo orden
        apuntesGrid.innerHTML = '';
        apuntesOrdenados.forEach(card => {
            apuntesGrid.appendChild(card);
        });

        // Actualizar la referencia
        apuntesCards = apuntesOrdenados;

        // Animación suave
        apuntesGrid.style.opacity = '0';
        setTimeout(() => {
            apuntesGrid.style.opacity = '1';
        }, 50);
    }

    /**
     * Parsear fecha en formato DD/MM/YYYY a timestamp
     */
    function parsearFecha(fechaText) {
        // Extraer solo la fecha (remover el ícono si existe)
        const match = fechaText.match(/(\d{1,2})\/(\d{1,2})\/(\d{4})/);
        if (!match) return 0;

        const [, dia, mes, anio] = match;
        return new Date(anio, mes - 1, dia).getTime();
    }

    /**
     * Parsear tamaño de archivo a bytes
     */
    function parsearTamano(sizeText) {
        const text = sizeText.trim().toLowerCase();
        const match = text.match(/([\d.]+)\s*(bytes?|kb|mb|gb)/i);

        if (!match) return 0;

        const valor = parseFloat(match[1]);
        const unidad = match[2].toLowerCase();

        const multiplicadores = {
            'bytes': 1,
            'byte': 1,
            'kb': 1024,
            'mb': 1024 * 1024,
            'gb': 1024 * 1024 * 1024
        };

        return valor * (multiplicadores[unidad] || 1);
    }

    // Agregar transición suave al grid
    apuntesGrid.style.transition = 'opacity 0.3s ease';
});
