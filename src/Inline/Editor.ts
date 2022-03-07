import {
    getInlineGroupOrThrow,
    parseFormSet,
    ImageUploaderInlineFormSet,
    ImageUploaderInlineManagementInputs,
    updateAllElementsIndexes,
    getManagementInputs,
    getAddButton,
} from './Utils';
import { EditorImage } from './EditorImage';

export class ImageUploaderInline {
    element: HTMLElement;
    inlineGroup: HTMLElement;
    addImageButton: HTMLElement;
    inlineFormset: ImageUploaderInlineFormSet;
    management: ImageUploaderInlineManagementInputs;
    next: number;
    maxCount: number;
    images: EditorImage[];
    canPreview: boolean;
    
    constructor(element: HTMLElement) {
        this.canPreview = true;

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

    handleAddImage() {
        console.log("QQQ?");
    }
}
