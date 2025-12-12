// Script para mostrar el nombre del archivo seleccionado
document.getElementById('{{ form.archivo.id_for_label }}').addEventListener('change', function (e) {
    const fileSelected = document.getElementById('fileSelected');
    const fileName = fileSelected.querySelector('.file-name');
    const fileSize = fileSelected.querySelector('.file-size');

    if (this.files && this.files[0]) {
        const file = this.files[0];
        fileName.textContent = file.name;

        // Convertir tamaño a formato legible
        const size = file.size;
        let sizeText;
        if (size < 1024) {
            sizeText = size + ' B';
        } else if (size < 1024 * 1024) {
            sizeText = (size / 1024).toFixed(2) + ' KB';
        } else {
            sizeText = (size / (1024 * 1024)).toFixed(2) + ' MB';
        }
        fileSize.textContent = sizeText;

        fileSelected.style.display = 'flex';
    } else {
        fileSelected.style.display = 'none';
    }
});
