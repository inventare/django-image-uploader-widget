class ImageUploaderWidget {
    element: HTMLElement;
    fileInput: HTMLInputElement;
    checkboxInput: HTMLInputElement | null;
    emptyMarker: HTMLElement;
    canDelete: boolean = false;
    dragging: boolean = false;
    canPreview: boolean = true;

    raw: string | null = null;
    file: File | null = null;

    constructor(element: HTMLElement) {
        this.element = element;
        const fileInput = element.querySelector<HTMLInputElement>('input[type=file]');
        const checkBoxInput = element.querySelector<HTMLInputElement>('input[type=checkbox]');
        const emptyMarker = element.querySelector<HTMLElement>('.iuw-empty')
        if (!fileInput) {
            throw new Error('no-file-input-found')
        }
        this.fileInput = fileInput;
        this.checkboxInput = checkBoxInput;
        if (!emptyMarker) {
            throw new Error('no-empty-label-found');
        }
        this.emptyMarker = emptyMarker;
        this.canDelete = element.getAttribute('data-candelete') === 'true';
        this.dragging = false;

        // add events
        this.fileInput.addEventListener('change', this.onFileInputChange);
        this.emptyMarker.addEventListener('click', this.onEmptyMarkerClick);
        this.element.addEventListener('dragenter', this.onDragEnter);
        this.element.addEventListener('dragover', this.onDragOver);
        this.element.addEventListener('dragleave', this.onDragLeave);
        this.element.addEventListener('dragend', this.onDragLeave);
        this.element.addEventListener('drop', this.onDrop);
        // init
        this.raw = element.getAttribute('data-raw');
        this.file = null;
        this.renderWidget();
    }

    onEmptyMarkerClick = () => {
        this.fileInput.click();
    }

    onDrop = (e: DragEvent) => {
        e.preventDefault();

        this.dragging = false;
        this.element.classList.remove('drop-zone');

        if (e.dataTransfer?.files.length) {
            this.fileInput.files = e.dataTransfer.files;
            this.file = this.fileInput.files[0];
            this.raw = null;
            this.renderWidget();
        }
    }

    onDragEnter = () => {
        this.dragging = true;
        this.element.classList.add('drop-zone');
    }

    onDragOver = (e: DragEvent) => {
        if (e) {
            e.preventDefault();
        }
    }
    
    onDragLeave = (e: DragEvent) => {
        if (e.relatedTarget && (e.relatedTarget as HTMLElement).closest('.iuw-root') === this.element) {
            return;
        }
        this.dragging = false;
        this.element.classList.remove('drop-zone');
    }

    closePreviewModal = () => {
        document.body.style.overflow = 'auto';
        const modal = document.getElementById('iuw-modal-element');
        if (modal) {
            modal.classList.remove('visible');
            modal.classList.add('hide');
            setTimeout(() => {
                modal.parentElement?.removeChild(modal);
            }, 300);
        }
    }

    onModalClick = (e: Event) => {
        if (e && e.target) {
            const element = e.target as HTMLElement;
            if (element.closest('img.iuw-modal-image-preview-item')) {
                return;
            }
        }
        this.closePreviewModal();
    }

    createPreviewModal = (image: HTMLImageElement) : HTMLElement => {
        image.className = '';
        image.classList.add('iuw-modal-image-preview-item');

        const modal = document.createElement('div');
        modal.id = 'iuw-modal-element';
        modal.classList.add('iuw-modal', 'hide');
        modal.addEventListener('click', this.onModalClick);
        
        const preview = document.createElement('div');
        preview.classList.add('iuw-modal-image-preview');
        preview.innerHTML = '<span class="iuw-modal-close"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path></svg></span>';
        preview.appendChild(image);
        modal.appendChild(preview);
        
        document.body.appendChild(modal);
        return modal;
    }

    onImagePreviewClick = (e: Event) => {
        if (e && e.target) {
            const targetElement = e.target as HTMLElement;
            if (targetElement.closest('.iuw-delete-icon')) {
                const element = targetElement.closest('.iuw-image-preview');
                element?.parentElement?.removeChild(element);
                if (this.checkboxInput) {
                    this.checkboxInput.checked = true;
                }
                this.fileInput.value = '';
                this.file = null;
                this.raw = null;
                this.renderWidget();
                return;
            }
            if (targetElement.closest('.iuw-preview-icon')) {
                const element = targetElement.closest('.iuw-image-preview');
                let image = element?.querySelector('img');
                if (image) {
                    image = image.cloneNode(true) as HTMLImageElement;
                    const modal = this.createPreviewModal(image);
                    setTimeout(() => {
                        modal.classList.add('visible');
                        modal.classList.remove('hide');
                        document.body.style.overflow = 'hidden';
                    }, 50);
                    return;
                }
            }
        }
        this.fileInput.click();
    }

    onFileInputChange = () => {
        if (this.fileInput.files?.length) {
            this.file = this.fileInput.files[0];
        }
        this.renderWidget();
    }

    renderPreview(url: string) {
        const preview = document.createElement('div');
        preview.classList.add('iuw-image-preview');
        const img = document.createElement('img');
        img.src = url;
        preview.appendChild(img);
        if (this.canDelete) {
            const span = document.createElement('span');
            span.classList.add('iuw-delete-icon');
            span.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path></svg>';
            preview.appendChild(span);
        }

        if (this.canPreview) {
            const span = document.createElement('span');
            span.classList.add('iuw-preview-icon');
            if (!this.canDelete) {
                span.classList.add('iuw-only-preview');
            }
            span.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-zoom-in" viewBox="0 0 16 16" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"></path><path xmlns="http://www.w3.org/2000/svg" d="M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z"></path><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z"></path></svg>';
            preview.appendChild(span);
        }

        return preview;
    }

    renderWidget() {
        if (!this.file && !this.raw) {
            this.element.classList.remove('non-empty');
            if (this.checkboxInput) {
                this.checkboxInput.checked = true;
            }
        } else {
            this.element.classList.add('non-empty');
            if (this.checkboxInput) {
                this.checkboxInput.checked = false;
            }
        }

        Array
            .from(this.element.querySelectorAll('.iuw-image-preview'))
            .forEach((item) => this.element.removeChild(item));
        if (this.file) {
            const url = URL.createObjectURL(this.file);
            this.element.appendChild(this.renderPreview(url));
        }
        if (this.raw) {
            this.element.appendChild(this.renderPreview(this.raw));
        }
        Array
            .from(this.element.querySelectorAll('.iuw-image-preview'))
            .forEach((item) => item.addEventListener('click', this.onImagePreviewClick));
    }
}

declare global {
    interface Window {
        django: {
            jQuery: any;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    Array
        .from(document.querySelectorAll('.iuw-root'))
        .map((element) => new ImageUploaderWidget(element as HTMLElement));

    if (window && window.django && window.django.jQuery) {
        const $ = window.django.jQuery;
        
        $(document).on('formset:added', (_: Event, row: HTMLElement[]) => {
            if (!row.length) {
                return;
            }
            Array
                .from(row[0].querySelectorAll('.iuw-root'))
                .map((element) => new ImageUploaderWidget(element as HTMLElement));
        });
    }
});

// export for testing
export { ImageUploaderWidget };
