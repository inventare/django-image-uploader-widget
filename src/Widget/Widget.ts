import { PreviewModal } from '../PreviewModal';
import { renderPreview } from '../Preview';

export class ImageUploaderWidget {
    element: HTMLElement;
    fileInput: HTMLInputElement;
    checkboxInput: HTMLInputElement | null;
    emptyMarker: HTMLElement | null;
    canDelete: boolean = false;
    dragging: boolean = false;
    canPreview: boolean = true;

    raw: string | null = null;
    file: File | null = null;

    constructor(element: HTMLElement) {
        // get main elements
        this.element = element;
        const fileInput = element.querySelector<HTMLInputElement>(
            'input[type=file]'
        );
        const checkBoxInput = element.querySelector<HTMLInputElement>(
            'input[type=checkbox]'
        );
        // check if file input exists
        if (!fileInput) {
            throw new Error('no-file-input-found')
        }
        // store variables
        this.fileInput = fileInput;
        this.checkboxInput = checkBoxInput;
        this.emptyMarker = element.querySelector<HTMLElement>('.iuw-empty');
        this.canDelete = element.getAttribute('data-candelete') === 'true';
        this.dragging = false;
        // add events

        // init
        this.raw = element.getAttribute('data-raw');
        this.file = null;
        this.renderWidget();
    }

    updateCheckBoxAndEmptyState() {
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
    }

    renderWidget() {
        this.updateCheckBoxAndEmptyState();

        Array
            .from(this.element.querySelectorAll('.iuw-image-preview'))
            .forEach((item) => this.element.removeChild(item));
        if (this.file) {
            const url = URL.createObjectURL(this.file);
            this.element.appendChild(renderPreview(url, this.canDelete, this.canPreview));
        } else if (this.raw) {
            this.element.appendChild(renderPreview(this.raw, this.canDelete, this.canPreview));
        }
        Array
            .from(this.element.querySelectorAll('.iuw-image-preview'))
            .forEach((item) => item.addEventListener('click', this.onImagePreviewClick));
    }

    performDeleteImage = (previewElement?: Element | null) => {
        previewElement?.parentElement?.removeChild(previewElement);
        if (this.checkboxInput) {
            this.checkboxInput.checked = true;
        }
        this.fileInput.value = '';
        this.file = null;
        this.raw = null;
        this.renderWidget();
    }
    
    performPreviewImage = (previewElement?: Element | null) => {
        let image = previewElement?.querySelector('img');
        if (image) {
            image = image.cloneNode(true) as HTMLImageElement;
            PreviewModal.createPreviewModal(image);
            PreviewModal.openPreviewModal();
        }
    }

    onImagePreviewClick = (e: Event) => {
        if (e && e.target) {
            const targetElement = e.target as HTMLElement;
            if (targetElement.closest('.iuw-delete-icon')) {
                const element = targetElement.closest('.iuw-image-preview');
                return this.performDeleteImage(element);
            } else if (targetElement.closest('.iuw-preview-icon')) {
                const element = targetElement.closest('.iuw-image-preview');
                return this.performPreviewImage(element);
            }
        }
        this.fileInput.click();
    }
}
