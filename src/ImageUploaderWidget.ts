class ImageUploaderWidget {
    element: HTMLElement;
    fileInput: HTMLInputElement;
    checkboxInput: HTMLInputElement;
    emptyMarker: HTMLElement;
    dropLabel: HTMLElement;
    canDelete: boolean = false;
    dragging: boolean = false;

    id: string;

    raw: string | null = null;
    file: File | null = null;

    constructor(element: HTMLElement) {
        this.element = element;
        this.fileInput = element.querySelector('input[type=file]');
        this.checkboxInput = element.querySelector('input[type=checkbox]');
        this.emptyMarker = this.element.querySelector('.iuw-empty');
        this.canDelete = element.getAttribute('data-candelete') === 'true';
        this.dragging = false;
        this.id = this.fileInput.getAttribute('id');
        this.dropLabel = this.element.querySelector('.drop-label');
        
        if (this.dropLabel) {
            this.dropLabel.setAttribute('for', this.id);
        }

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

        if (e.dataTransfer.files.length) {
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

    onImagePreviewClick = (e: Event) => {
        if (e && e.target) {
            const targetElement = e.target as HTMLElement;
            if (e && e.target && targetElement.closest('.iuw-delete-icon')) {
                const element = targetElement.closest('.iuw-image-preview');
                element.parentElement.removeChild(element);
                this.checkboxInput.checked = true;
                this.fileInput.value = null;
                this.file = null;
                this.raw = null;
                this.renderWidget();
                return;
            }
        }
        this.fileInput.click();
    }

    onFileInputChange = () => {
        if (this.fileInput.files.length > 0) {
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
            span.innerHTML = 'X';
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
