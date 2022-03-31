import {
    getInlineGroupOrThrow,
    parseFormSet,
    ImageUploaderInlineFormSet,
    ImageUploaderInlineManagementInputs,
    updateAllElementsIndexes,
    getManagementInputs,
    getAddButton,
    createTempFileInput,
} from './Utils';
import { EditorImage } from './EditorImage';

export class ImageUploaderInline {
    element: HTMLElement;
    inlineGroup: HTMLElement;
    addImageButton: HTMLElement;
    tempFileInput: HTMLInputElement | null;
    inlineFormset: ImageUploaderInlineFormSet;
    management: ImageUploaderInlineManagementInputs;
    next: number;
    maxCount: number;
    images: EditorImage[];
    canPreview: boolean;
    
    constructor(element: HTMLElement) {
        this.canPreview = true;

        this.tempFileInput = null;
        this.element = element;
        this.inlineGroup = getInlineGroupOrThrow(this.element);
        this.inlineFormset = parseFormSet(this.inlineGroup);
        this.management = getManagementInputs(this.inlineFormset.options.prefix);
        this.next = 0;
        if (this.management.maxNumForms.value === '') {
            this.maxCount = Number.MAX_SAFE_INTEGER;
        } else {
            this.maxCount = parseInt(this.management.maxNumForms.value, 10);
        }
        this.addImageButton = getAddButton(this.element);
        
        this.updateEmpty();
        this.updateAllIndexes();

        this.images = Array
            .from(this.element.querySelectorAll<HTMLElement>('.inline-related'))
            .map((item) => {
                const editorImage = new EditorImage(item, this.canPreview);
                editorImage.onDelete = this.handleImageDelete;
                return editorImage;
            });

        this.bindVariables();
        this.bindEvents();
    }

    bindVariables() {
        this.handleAddImage = this.handleAddImage.bind(this);
        this.handleTempFileInputChange = this.handleTempFileInputChange.bind(this);
    }

    bindEvents() {
        this.addImageButton.addEventListener('click', this.handleAddImage);
        this.element.querySelector('.iuw-empty')?.addEventListener('click', this.handleAddImage);
    }

    updateEmpty() {
        const { length } = this.element.querySelectorAll('.inline-related:not(.empty-form):not(.deleted)');
        this.element.classList.toggle('non-empty', length > 0);
    }

    updateAllIndexes() {
        const { prefix } = this.inlineFormset.options;
        const { length: count } = Array
            .from(this.element.querySelectorAll<HTMLElement>('.inline-related:not(.empty-form)'))
            .map((item, index) => {
                updateAllElementsIndexes(item, prefix, index);
                return item;
            });
        
        this.next = count;
        this.management.totalForms.value = String(this.next);
        this.addImageButton.classList.toggle('visible-by-number', this.maxCount - this.next > 0);
    }

    createFromEmptyTemplate(): HTMLElement {
        const template = this.element.querySelector('.inline-related.empty-form');
        if (!template) {
            throw new Error('no-empty-template');
        }

        const row = <HTMLElement>template.cloneNode(true);
        row.classList.remove('empty-form');
        row.classList.remove('last-related');
        row.setAttribute('data-candelete', 'true');
        row.id = `${this.inlineFormset.options.prefix}-${this.next}`;

        template.parentElement?.insertBefore(row, template);

        return row;
    }

    addFile() {
        const row = this.createFromEmptyTemplate();

        if (!this.tempFileInput) {
            throw new Error('no-temp-input-for-upload');
        }
        const file = (this.tempFileInput.files || [null])[0];
        if (!file) {
            throw new Error('no-file-in-input')
        }
        
        const rowFileInput = row.querySelector('input[type=file]') as HTMLInputElement;
        const parent = rowFileInput.parentElement as HTMLElement;

        const className = rowFileInput.className;
        const name = rowFileInput.getAttribute('name');
        parent.removeChild(rowFileInput);

        this.tempFileInput.className = className;
        this.tempFileInput.setAttribute('name', name || '');
        this.tempFileInput.parentElement?.removeChild(this.tempFileInput);
        parent.appendChild(this.tempFileInput);
        this.tempFileInput = null;

        const editorImage = new EditorImage(row, true, URL.createObjectURL(file));
        editorImage.onDelete = this.handleImageDelete;
        this.images.push(editorImage);
        this.updateEmpty();
        this.updateAllIndexes();
    }

    handleTempFileInputChange() {
        const filesList = this.tempFileInput?.files;
        if (!filesList || filesList.length <= 0) {
            return;
        }
        this.addFile();
    }

    handleAddImage() {
        if(!this.tempFileInput) {
            this.tempFileInput = createTempFileInput();
            this.tempFileInput.addEventListener('change', this.handleTempFileInputChange);
            this.element.appendChild(this.tempFileInput);
        }
        this.tempFileInput.click();
    }

    handleImageDelete = (image: EditorImage) => {
        if (image.element.getAttribute('data-raw')) {
            image.element.classList.add('deleted');
            const checkboxInput = image.element.querySelector('input[type=checkbox]') as HTMLInputElement;
            checkboxInput.checked = true;
        } else {
            image.element.parentElement?.removeChild(image.element);
        }
        this.images = this.images.filter((item) => item !== image);
        this.updateEmpty();
    }
}
