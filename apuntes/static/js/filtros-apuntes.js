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

        // Guardar el estado de visibilidad antes de ordenar
        const estadosVisibilidad = new Map();
        apuntesOrdenados.forEach(card => {
            estadosVisibilidad.set(card, card.classList.contains('hidden'));
        });

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
            // Restaurar estado de visibilidad
            if (estadosVisibilidad.get(card)) {
                card.classList.add('hidden');
            }
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
        const match = text.match(/([\d.,]+)\s*(bytes?|kb|mb|gb)/i);

        if (!match) return 0;

        // Reemplazar coma por punto para parseFloat (formato español -> formato JS)
        const valor = parseFloat(match[1].replace(',', '.'));
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

    // ========================================
    // SISTEMA DE BÚSQUEDA
    // ========================================

    const searchInput = document.getElementById('searchApuntes');
    const clearSearchBtn = document.getElementById('clearSearch');
    const searchResultsInfo = document.getElementById('searchResultsInfo');

    if (searchInput) {
        // Búsqueda en tiempo real con debounce
        let searchTimeout;
        searchInput.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            const searchTerm = this.value.trim();

            // Mostrar/ocultar botón de limpiar
            if (searchTerm.length > 0) {
                clearSearchBtn.style.display = 'flex';
            } else {
                clearSearchBtn.style.display = 'none';
                searchResultsInfo.style.display = 'none';
            }

            // Debounce de 300ms
            searchTimeout = setTimeout(() => {
                buscarApuntes(searchTerm);
            }, 300);
        });

        // Botón para limpiar búsqueda
        if (clearSearchBtn) {
            clearSearchBtn.addEventListener('click', function () {
                searchInput.value = '';
                clearSearchBtn.style.display = 'none';
                searchResultsInfo.style.display = 'none';
                buscarApuntes('');
                searchInput.focus();
            });
        }

        // Limpiar con tecla Escape
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                searchInput.value = '';
                clearSearchBtn.style.display = 'none';
                searchResultsInfo.style.display = 'none';
                buscarApuntes('');
            }
        });
    }

    /**
     * Función de búsqueda de apuntes
     */
    function buscarApuntes(searchTerm) {
        const term = searchTerm.toLowerCase();
        let matchCount = 0;
        let totalCount = 0;

        apuntesCards.forEach(card => {
            totalCount++;

            if (term === '') {
                // Si no hay término de búsqueda, mostrar todos
                card.classList.remove('hidden', 'search-match');
                matchCount++;
            } else {
                // Obtener título y descripción
                const titulo = card.querySelector('.apunte-titulo');
                const descripcion = card.querySelector('.apunte-descripcion');

                const tituloText = titulo ? titulo.textContent.toLowerCase() : '';
                const descripcionText = descripcion ? descripcion.textContent.toLowerCase() : '';

                // Buscar coincidencias
                const matchTitulo = tituloText.includes(term);
                const matchDescripcion = descripcionText.includes(term);

                if (matchTitulo || matchDescripcion) {
                    card.classList.remove('hidden');
                    card.classList.add('search-match');
                    matchCount++;

                    // Remover la clase de animación después de que termine
                    setTimeout(() => {
                        card.classList.remove('search-match');
                    }, 400);
                } else {
                    card.classList.add('hidden');
                    card.classList.remove('search-match');
                }
            }
        });

        // Actualizar información de resultados
        if (term !== '') {
            const resultsText = matchCount === 1
                ? `Se encontró 1 apunte de ${totalCount}`
                : `Se encontraron ${matchCount} apuntes de ${totalCount}`;

            searchResultsInfo.querySelector('.results-count').textContent = resultsText;
            searchResultsInfo.style.display = 'flex';

            // Si no hay resultados, mostrar mensaje especial
            if (matchCount === 0) {
                searchResultsInfo.style.background = '#fff3cd';
                searchResultsInfo.style.borderColor = '#ffc107';
                searchResultsInfo.querySelector('.results-count').style.color = '#856404';
                searchResultsInfo.querySelector('.results-count').textContent =
                    `No se encontraron apuntes que coincidan con "${searchTerm}"`;
            } else {
                searchResultsInfo.style.background = '#e7f3ff';
                searchResultsInfo.style.borderColor = 'var(--primary-color)';
                searchResultsInfo.querySelector('.results-count').style.color = 'var(--primary-color)';
            }
        } else {
            searchResultsInfo.style.display = 'none';
        }
    }

    /**
     * Modificar la función ordenarApuntes para que respete la búsqueda activa
     */
    const ordenarApuntesOriginal = ordenarApuntes;
    ordenarApuntes = function (filtro, orden) {
        // Llamar a la función original
        ordenarApuntesOriginal(filtro, orden);

        // Re-aplicar búsqueda si hay término activo
        if (searchInput && searchInput.value.trim() !== '') {
            buscarApuntes(searchInput.value.trim());
        }
    };
});
