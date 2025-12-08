document.addEventListener('DOMContentLoaded', function () {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(function (toastElement) {
        // Auto-hide after 5 seconds
        setTimeout(function () {
            const bsToast = bootstrap.Toast.getOrCreateInstance(toastElement);
            bsToast.hide();
        }, 5000);
    });
});