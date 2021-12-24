interface ImageUploaderInlineFormSet {
    name: string;
    options: {
        prefix: string;
        addText: string;
        deleteText: string;
    }
}

class ImageUploaderInline {
    element: HTMLElement;
    inlineGroup: HTMLElement;
    inlineFormset: ImageUploaderInlineFormSet;
    tempFileInput: HTMLInputElement | null = null;
    next: number = 0;

    constructor(element: HTMLElement) {
        this.element = element;
        this.inlineGroup = element.closest('.inline-group');
        this.inlineFormset = <ImageUploaderInlineFormSet>JSON.parse(
            this.inlineGroup.getAttribute('data-inline-formset'),
        );
        
        this.updateEmpty();
        this.updateAllIndexes();

        Array
            .from(this.element.querySelectorAll('.inline-related'))
            .forEach((item) => this.adjustInlineRelated(item));
        Array
            .from(this.element.querySelectorAll('.iuw-add-image-btn, .iuw-empty'))
            .forEach((item) => item.addEventListener('click', this.onChooseAddImageAreaClick));
    }

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
        if (element.getAttribute('for')) {
            element.setAttribute('for', element.getAttribute('for').replace(id_regex, replacement));
        }
        if (element.id) {
            element.id = element.id.replace(id_regex, replacement);
        }
        if (element.getAttribute('name')) {
            element.setAttribute('name', element.getAttribute('name').replace(id_regex, replacement));
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
                .querySelector('.iuw-add-image-btn')
                .classList.add('visible-by-number');
        } else {
            this.element
                .querySelector('.iuw-add-image-btn')
                .classList.remove('visible-by-number');
        }
    }

    adjustInlineRelated(element: Element) {
        const inputs = Array
            .from(
                element.querySelectorAll('input[type=hidden], input[type=checkbox], input[type=file]'),
            )
            .map((item) => {
                item.parentElement.removeChild(item);
                return item;
            });
        // get raw image url
        const rawImage = document.querySelector('p.file-upload a');
        if (rawImage) {
            element.setAttribute('data-raw', rawImage.getAttribute('href'));
        }
        // clear element
        element.innerHTML = '';
        inputs.forEach((item) => element.appendChild(item));
        // apply raw image
        if (rawImage) {
            this.appendItem(element, rawImage.getAttribute('href'));
        }
    }

    onRelatedItemClick = (e: Event) => {
        const target = e.target as HTMLElement;
        const item = target.closest('.inline-related');
        if (target.classList.contains('iuw-delete-icon')) {
            if (item.getAttribute('data-raw')) {
                item.classList.add('deleted');
                const checkboxInput = item.querySelector('input[type=checkbox]') as HTMLInputElement;
                checkboxInput.checked = true;
            } else {
                item.parentElement.removeChild(item);
            }
            this.updateEmpty();
            return;
        }
        var fileInput = item.querySelector('input[type=file]') as HTMLInputElement;
        if (e.target === fileInput) {
            return;
        }
        fileInput.click();
    }

    onFileInputChange = (e: Event) => {
        const target = e.target as HTMLElement;
        if (target.tagName !== 'INPUT') {
            return;
        }
        const fileInput = target as HTMLInputElement;
        var files = fileInput.files;
        if (files.length <= 0) {
            return;
        }
        const imgTag = target.closest('.inline-related').querySelector('img');
        if (imgTag) {
            imgTag.src = URL.createObjectURL(files[0]);
        }
    }

    appendItem(element: Element, url: string) {
        let delete_icon: Element | null = null;
        const related = element.closest('.inline-related');
        if (related.getAttribute('data-candelete') === 'true') {
            delete_icon = document.createElement('span');
            delete_icon.classList.add('iuw-delete-icon');
            delete_icon.innerHTML = 'X';
        }
        const img = document.createElement('img');
        img.src = url;
        element.appendChild(img);
        if (delete_icon) {
            element.appendChild(delete_icon);
        }
        related.removeEventListener('click', this.onRelatedItemClick);
        related.addEventListener('click', this.onRelatedItemClick);
        const fileInput = related.querySelector('input[type=file]');
        fileInput.removeEventListener('change', this.onFileInputChange);
        fileInput.addEventListener('change', this.onFileInputChange);
    }

    onTempFileChange = () => {
        const filesList = this.tempFileInput.files;
        if (filesList.length <= 0) {
            return;
        }
        
        this.tempFileInput.removeEventListener('change', this.onTempFileChange);
        this.tempFileInput.parentElement.removeChild(this.tempFileInput);
        this.tempFileInput = null;
        
        const template = this.element.querySelector('.inline-related.empty-form');
        if (!template) {
            return;
        }
        const row = template.cloneNode(true) as HTMLElement;
        row.classList.remove('empty-form');
        row.classList.remove('last-related');
        row.setAttribute('data-candelete', 'true');
        row.id = `${this.inlineFormset.options.prefix}-${this.next}`;
        
        template.parentElement.insertBefore(row, template);

        const rowFileInput = row.querySelector('input[type=file]') as HTMLInputElement;
        rowFileInput.files = filesList;

        this.appendItem(row, URL.createObjectURL(filesList[0]));
        this.updateEmpty();
        this.updateAllIndexes();
    }

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
}

document.addEventListener('DOMContentLoaded', () => {
    Array
        .from(document.querySelectorAll('.iuw-inline-root'))
        .map((element) => new ImageUploaderInline(element as HTMLElement));
});

// export for testing
export { ImageUploaderInline };
