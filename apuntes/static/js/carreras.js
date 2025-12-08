document.addEventListener('DOMContentLoaded', function() {
    // Prevenir que el clic en el botón de eliminar active el enlace de la tarjeta
    const deleteLinks = document.querySelectorAll('.btn-delete-carrera');
    
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.stopPropagation(); // Evita que se active el enlace de la tarjeta
            
            const carreraNombre = this.dataset.carreraNombre;
            
            // Confirmar eliminación
            if (!confirm(`¿Estás seguro de que deseas eliminar la carrera "${carreraNombre}"?\n\nEsta acción no se puede deshacer.`)) {
                e.preventDefault(); // Solo previene la navegación si el usuario cancela
            }
            // Si el usuario confirma, el enlace navegará normalmente a la URL de eliminación
        });
    });
});
