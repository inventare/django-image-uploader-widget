const IUWPreviewModal = {
    openPreviewModal: function() {
        const modal = document.getElementById('iuw-modal-element');
        if (!modal) {
            return;
        }
        setTimeout(function() {
            modal.classList.add('visible');
            modal.classList.remove('hide');
            document.body.style.overflow = 'hidden';
        }, 50);
    },
    closePreviewModal: function() {
        document.body.style.overflow = 'auto';
        const modal = document.getElementById('iuw-modal-element');
        if (modal) {
            modal.classList.remove('visible');
            modal.classList.add('hide');
            setTimeout(function() {
                modal.parentElement.removeChild(modal);
            }, 300);
        }
    },
    onModalClick: function (e) {
        if (e && e.target) {
            const element = e.target;
            if (element.closest('img.iuw-modal-image-preview-item')) {
                return;
            }
        }
        IUWPreviewModal.closePreviewModal();
    },
    createPreviewModal: function (image) {
        image.className = '';
        image.classList.add('iuw-modal-image-preview-item');

        const modal = document.createElement('div');
        modal.id = 'iuw-modal-element';
        modal.classList.add('iuw-modal', 'hide');
        modal.addEventListener('click', IUWPreviewModal.onModalClick);
        
        const preview = document.createElement('div');
        preview.classList.add('iuw-modal-image-preview');
        preview.innerHTML = '<span class="iuw-modal-close"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path></svg></span>';
        preview.appendChild(image);
        modal.appendChild(preview);
        
        document.body.appendChild(modal);
        return modal;
    }
};
