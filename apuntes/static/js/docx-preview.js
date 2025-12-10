/**
 * Script para previsualizar archivos DOCX usando docx-preview library
 * Requiere: docx-preview.min.js (CDN)
 */

document.addEventListener('DOMContentLoaded', function() {
    const docxContainers = document.querySelectorAll('.docx-preview-container');
    
    docxContainers.forEach(container => {
        const url = container.dataset.url;
        
        if (url && typeof docx !== 'undefined') {
            // Fetch el archivo DOCX
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error al cargar el archivo');
                    }
                    return response.arrayBuffer();
                })
                .then(arrayBuffer => {
                    // Limpiar el contenedor
                    container.innerHTML = '';
                    
                    // Renderizar el DOCX
                    docx.renderAsync(arrayBuffer, container, null, {
                        className: "docx-preview-content",
                        inWrapper: true,
                        ignoreWidth: false,
                        ignoreHeight: false,
                        ignoreFonts: false,
                        breakPages: false,
                        ignoreLastRenderedPageBreak: true,
                        experimental: false,
                        trimXmlDeclaration: true,
                        useBase64URL: false,
                        useMathMLPolyfill: false,
                        renderHeaders: false,
                        renderFooters: false,
                        renderFootnotes: true,
                        renderEndnotes: true
                    }).catch(error => {
                        console.error('Error renderizando DOCX:', error);
                        container.innerHTML = `
                            <div class="preview-icon word">
                                <i class="bi bi-file-earmark-word-fill"></i>
                                <span class="preview-label">No se pudo cargar la vista previa</span>
                                <small style="color: #999; margin-top: 0.5rem;">Descarga el archivo para verlo</small>
                            </div>
                        `;
                    });
                })
                .catch(error => {
                    console.error('Error cargando archivo:', error);
                    container.innerHTML = `
                        <div class="preview-icon word">
                            <i class="bi bi-file-earmark-word-fill"></i>
                            <span class="preview-label">Error al cargar</span>
                        </div>
                    `;
                });
        } else {
            // Si no está disponible la librería, mostrar icono
            container.innerHTML = `
                <div class="preview-icon word">
                    <i class="bi bi-file-earmark-word-fill"></i>
                    <span class="preview-label">Word</span>
                    <small style="color: #999; margin-top: 0.5rem;">Vista previa no disponible</small>
                </div>
            `;
        }
    });
});
