import {
    getInlineGroupOrThrow,
    parseFormSet,
    ImageUploaderInlineFormSet,
    ImageUploaderInlineManagementInputs,
    updateAllElementsIndexes,
    getManagementInputs,
    getAddButton,
    createTempFileInput,
    applyFileToInput,
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
            .map((item) => new EditorImage(item, this.canPreview));

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

    addFile(file: File) {
        const row = this.createFromEmptyTemplate();
        
        const rowFileInput = row.querySelector<HTMLInputElement>('input[type=file]');
        applyFileToInput(file, rowFileInput);
        
        this.images.push(new EditorImage(row, true, URL.createObjectURL(file)));
        this.updateEmpty();
        this.updateAllIndexes();
    }

    handleTempFileInputChange() {
        const filesList = this.tempFileInput?.files;
        if (!filesList || filesList.length <= 0) {
            return;
        }
        this.tempFileInput?.removeEventListener('change', this.handleTempFileInputChange);
        this.tempFileInput?.parentElement?.removeChild(this.tempFileInput);
        this.tempFileInput = null;
        this.addFile(filesList[0]);
    }

    handleAddImage() {
        if(!this.tempFileInput) {
            this.tempFileInput = createTempFileInput();
            this.tempFileInput.addEventListener('change', this.handleTempFileInputChange);
            this.element.appendChild(this.tempFileInput);
        }
        this.tempFileInput.click();
    }
}
