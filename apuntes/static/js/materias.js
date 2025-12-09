document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('materiasSidebar');
    const toggleBtn = document.getElementById('sidebarToggle');
    const closeBtn = document.getElementById('sidebarClose');
    const materiaLinks = document.querySelectorAll('.materia-link');

    // Toggle sidebar on button click
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.add('active');
        });
    }

    // Close sidebar on close button click
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            sidebar.classList.remove('active');
        });
    }

    // Close sidebar when clicking on a materia link (mobile)
    materiaLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 767) {
                sidebar.classList.remove('active');
            }
        });
    });

    // Close sidebar when clicking outside (mobile)
    document.addEventListener('click', function(event) {
        if (window.innerWidth <= 767) {
            const isClickInsideSidebar = sidebar.contains(event.target);
            const isClickOnToggle = toggleBtn.contains(event.target);
            
            if (!isClickInsideSidebar && !isClickOnToggle && sidebar.classList.contains('active')) {
                sidebar.classList.remove('active');
            }
        }
    });
});
