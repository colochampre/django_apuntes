document.addEventListener('DOMContentLoaded', function () {
    // Toast logic
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(function (toastElement) {
        // Auto-hide after 5 seconds
        setTimeout(function () {
            const bsToast = bootstrap.Toast.getOrCreateInstance(toastElement);
            bsToast.hide();
        }, 5000);
    });

    // Auto-download logic (Login -> Redirect -> Download)
    const urlParams = new URLSearchParams(window.location.search);
    const downloadId = urlParams.get('download_pending');
    
    if (downloadId) {
        // Remove the param from URL to prevent double download on refresh
        urlParams.delete('download_pending');
        const newUrl = window.location.pathname + (urlParams.toString() ? '?' + urlParams.toString() : '');
        window.history.replaceState({}, '', newUrl);
        
        // Trigger download
        window.location.href = '/apuntes/descargar/' + downloadId + '/';
    }
});