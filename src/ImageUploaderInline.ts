import { PreviewModal } from './PreviewModal';

interface ImageUploaderInlineFormSet {
    name: string;
    options: {
        prefix: string;
        addText: string;
        deleteText: string;
    }
}

class ImageUploaderInline {
    /*
    element: HTMLElement;
    inlineGroup: HTMLElement;
    inlineFormset: ImageUploaderInlineFormSet;
    */
    tempFileInput: HTMLInputElement | null = null;
    next: number = 0;
    dragging: boolean = false;
    canPreview: boolean = true;

    constructor(element: HTMLElement) {
        /*
        this.element = element;
        const inlineGroup = element.closest<HTMLElement>('.inline-group');
        if (!inlineGroup) {
            throw new Error('no-inline-group-found');
        }
        this.inlineGroup = inlineGroup;
        const formSetDataString = this.inlineGroup.getAttribute('data-inline-formset');
        if (!formSetDataString) {
            throw new Error('no-formset-data-found');
        }
        this.inlineFormset = <ImageUploaderInlineFormSet>JSON.parse(formSetDataString);
        
        this.updateEmpty();
        this.updateAllIndexes();

        Array
            .from(this.element.querySelectorAll('.inline-related'))
            .forEach((item) => this.adjustInlineRelated(item));
        Array
            .from(this.element.querySelectorAll('.iuw-add-image-btn, .iuw-empty'))
            .forEach((item) => item.addEventListener('click', this.onChooseAddImageAreaClick));
        */
        
        this.element.addEventListener('dragenter', this.onDragEnter);
        this.element.addEventListener('dragover', this.onDragOver);
        this.element.addEventListener('dragleave', this.onDragLeave);
        this.element.addEventListener('dragend', this.onDragLeave);
        this.element.addEventListener('drop', this.onDrop);
    }

    onDrop = (e: DragEvent) => {
        e.preventDefault();

        this.dragging = false;
        this.element.classList.remove('drop-zone');

        if (e.dataTransfer?.files.length) {
            for (const file of e.dataTransfer.files) {
                this.addFile(file);
            }
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
        if (e.relatedTarget && (e.relatedTarget as HTMLElement).closest('.iuw-inline-root') === this.element) {
            return;
        }
        this.dragging = false;
        this.element.classList.remove('drop-zone');
    }

    /*
    updateEmpty() {
        const { length } = this.element.querySelectorAll('.inline-related:not(.empty-form):not(.deleted)');
        if (length > 0) {
            this.element.classList.add('non-empty');
        } else {
            this.element.classList.remove('non-empty');
        }
    }
    
    updateElementIndex(element: HTMLElement, prefix: string, index: number) {
        const id_regex = new RegExp(`(${prefix}-(\\d+|__prefix__))`);
        const replacement = `${prefix}-${index}`;
        const forAttr = element.getAttribute('for');
        if (forAttr) {
            element.setAttribute('for', forAttr.replace(id_regex, replacement));
        }
        if (element.id) {
            element.id = element.id.replace(id_regex, replacement);
        }
        const nameAttr = element.getAttribute('name');
        if (nameAttr) {
            element.setAttribute('name', nameAttr.replace(id_regex, replacement));
        }
    }

    updateAllIndexes() {
        const { prefix } = this.inlineFormset.options;
        const { length: count } = Array
            .from(this.element.querySelectorAll('.inline-related:not(.empty-form)'))
            .map((item) => item as HTMLElement)
            .map((item, index) => {
                this.updateElementIndex(item, prefix, index);
                Array
                    .from(item.querySelectorAll('*'))
                    .map((childItem) => childItem as HTMLElement)
                    .forEach((childItem) => {
                        this.updateElementIndex(childItem, prefix, index);
                    });
                return item;
            });
        this.next = count;
        const totalFormsInput = document.getElementById(`id_${prefix}-TOTAL_FORMS`) as HTMLInputElement;
        totalFormsInput.value = String(this.next);
        const maxFormsInput = document.getElementById(`id_${prefix}-MAX_NUM_FORMS`) as HTMLInputElement;
        let maxNumber = parseInt(maxFormsInput.value, 10);
        if (Number.isNaN(maxNumber)) {
            maxNumber = 0;
        }
        if (maxFormsInput.value === '' || maxNumber - this.next > 0) {
            this.element
                .querySelector('.iuw-add-image-btn')?.classList.add('visible-by-number');
        } else {
            this.element
                .querySelector('.iuw-add-image-btn')?.classList.remove('visible-by-number');
        }
    }

    adjustInlineRelated(element: Element) {
        const inputs = Array
            .from(
                element.querySelectorAll('input[type=hidden], input[type=checkbox], input[type=file]'),
            )
            .map((item) => {
                item.parentElement?.removeChild(item);
                return item;
            });
        // get raw image url
        let rawImage = document.querySelector('p.file-upload a');
        if (element.classList.contains('empty-form')) {
            rawImage = null;
        }
        let hrefAttr: string | null = null;
        if (rawImage) {
            hrefAttr = rawImage.getAttribute('href');
            if (hrefAttr) {
                element.setAttribute('data-raw', hrefAttr);
            }
        }
        // clear element
        element.innerHTML = '';
        inputs.forEach((item) => element.appendChild(item));
        // apply raw image
        if (hrefAttr) {
            this.appendItem(element, hrefAttr);
        }
    }
    */

    onRelatedItemClick = (e: Event) => {
        if (!e || !e.target) {
            return;
        }
        const target = e.target as HTMLElement;
        const item = target.closest('.inline-related');
        if (target.closest('.iuw-delete-icon')) {
            if (item?.getAttribute('data-raw')) {
                item?.classList.add('deleted');
                const checkboxInput = item.querySelector('input[type=checkbox]') as HTMLInputElement;
                checkboxInput.checked = true;
            } else {
                item?.parentElement?.removeChild(item);
            }
            this.updateEmpty();
            return;
        }
        if (target.closest('.iuw-preview-icon')) {
            let image = item?.querySelector('img');
            if (image) {
                image = image.cloneNode(true) as HTMLImageElement;
                PreviewModal.createPreviewModal(image);
                PreviewModal.openPreviewModal();
                return;
            }
        }
        const fileInput = item?.querySelector<HTMLInputElement>('input[type=file]');
        if (e.target === fileInput) {
            return;
        }
        fileInput?.click();
    }

    onFileInputChange = (e: Event) => {
        const target = e.target as HTMLElement;
        if (target.tagName !== 'INPUT') {
            return;
        }
        const fileInput = target as HTMLInputElement;
        var files = fileInput.files;
        if (!files?.length) {
            return;
        }
        const imgTag = target.closest('.inline-related')?.querySelector('img');
        if (imgTag) {
            imgTag.src = URL.createObjectURL(files[0]);
        }
    }

    appendItem(element: Element, url: string) {
        let delete_icon: Element | null = null;
        const related = element.closest('.inline-related');
        if (related?.getAttribute('data-candelete') === 'true') {
            delete_icon = document.createElement('span');
            delete_icon.classList.add('iuw-delete-icon');
            delete_icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path></svg>';
        }
        if (this.canPreview) {
            const span = document.createElement('span');
            span.classList.add('iuw-preview-icon');
            if (related?.getAttribute('data-candelete') !== 'true') {
                span.classList.add('iuw-only-preview');
            }
            span.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-zoom-in" viewBox="0 0 16 16" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"></path><path xmlns="http://www.w3.org/2000/svg" d="M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z"></path><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z"></path></svg>';
            element.appendChild(span);
        }
        const img = document.createElement('img');
        img.src = url;
        element.appendChild(img);
        if (delete_icon) {
            element.appendChild(delete_icon);
        }
        related?.removeEventListener('click', this.onRelatedItemClick);
        related?.addEventListener('click', this.onRelatedItemClick);
        const fileInput = related?.querySelector('input[type=file]');
        fileInput?.removeEventListener('change', this.onFileInputChange);
        fileInput?.addEventListener('change', this.onFileInputChange);
    }

    /*
    onTempFileChange = () => {
        const filesList = this.tempFileInput?.files;
        if (!filesList?.length) {
            return;
        }
        
        this.tempFileInput?.removeEventListener('change', this.onTempFileChange);
        this.tempFileInput?.parentElement?.removeChild(this.tempFileInput);
        this.tempFileInput = null;
        
        this.addFile(filesList[0]);
    }
    */

    addFile(file: File) {
        const template = this.element.querySelector('.inline-related.empty-form');
        if (!template) {
            return;
        }
        const row = template.cloneNode(true) as HTMLElement;
        row.classList.remove('empty-form');
        row.classList.remove('last-related');
        row.setAttribute('data-candelete', 'true');
        row.id = `${this.inlineFormset.options.prefix}-${this.next}`;
        
        template.parentElement?.insertBefore(row, template);

        const dataTransferList = new DataTransfer();
        dataTransferList.items.add(file);

        const rowFileInput = row.querySelector('input[type=file]') as HTMLInputElement;
        rowFileInput.files = dataTransferList.files;

        this.appendItem(row, URL.createObjectURL(file));
        this.updateEmpty();
        this.updateAllIndexes();
    }

    /*
    onChooseAddImageAreaClick = () => {
        if (!this.tempFileInput) {
            this.tempFileInput = document.createElement('input');
            this.tempFileInput.setAttribute('type', 'file');
            this.tempFileInput.classList.add('temp_file');
            this.tempFileInput.setAttribute('accept', 'image/*');
            this.tempFileInput.style.display = 'none';
            this.tempFileInput.addEventListener('change', this.onTempFileChange);
            this.element.appendChild(this.tempFileInput);
        }
        this.tempFileInput.click();
    }
    */
}

document.addEventListener('DOMContentLoaded', () => {
    Array
        .from(document.querySelectorAll('.iuw-inline-root'))
        .map((element) => new ImageUploaderInline(element as HTMLElement));
});

// export for testing
export { ImageUploaderInline };
