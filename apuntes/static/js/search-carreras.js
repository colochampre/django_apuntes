// Búsqueda en tiempo real para carreras con debounce
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchCarreras');
    const clearSearchBtn = document.getElementById('clearSearch');
    const searchForm = document.querySelector('.search-form');

    if (searchInput && searchForm) {
        // Mantener el foco en el input si hay una búsqueda activa
        if (searchInput.value.trim().length > 0) {
            searchInput.focus();
            // Colocar el cursor al final del texto
            searchInput.setSelectionRange(searchInput.value.length, searchInput.value.length);
        }

        // Búsqueda en tiempo real con debounce
        let searchTimeout;
        searchInput.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            const searchTerm = this.value.trim();

            // Debounce de 600ms para enviar el formulario
            searchTimeout = setTimeout(() => {
                if (searchTerm.length > 0) {
                    searchForm.submit();
                }
            }, 600);
        });

        // Limpiar con tecla Escape
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                clearTimeout(searchTimeout);
                window.location.href = window.location.pathname;
            }
        });
    }
});
