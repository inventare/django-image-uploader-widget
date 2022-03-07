import PreviewIcon from '../Icons/PreviewIcon';
import DeleteIcon from '../Icons/DeleteIcon';

export class EditorImage {
    element: HTMLElement;
    canPreview: boolean;
    
    constructor(element: HTMLElement, canPreview: boolean) {
        this.element = element;
        this.canPreview = canPreview;

        const inputs = this.removeAndGetInputs();
        const link = this.getAndUpdateRawImage();

        this.element.innerHTML = '';
        inputs.forEach((item) => this.element.appendChild(item));
        this.render(link);
    }

    private removeAndGetInputs() {
        return Array
            .from(
                this.element.querySelectorAll<HTMLInputElement>(
                    'input[type=hidden], input[type=checkbox], input[type=file]'
                ),
            )
            .map((item) => {
                item.parentElement?.removeChild(item);
                return item;
            });
    }

    private getAndUpdateRawImage() {
        let rawImage = document.querySelector('p.file-upload a');
        if (this.element.classList.contains('empty-form')) {
            rawImage = null;
        }
        let hrefAttr: string | null = null;
        if (rawImage) {
            hrefAttr = rawImage.getAttribute('href');
            if (hrefAttr) {
                this.element.setAttribute('data-raw', hrefAttr);
            }
        }
        return hrefAttr;
    }

    private render(link: string | null) {
        if (!link) {
            return;
        }
        let delete_icon: Element | null = null;
        const related = this.element.closest('.inline-related');
        if (related?.getAttribute('data-candelete') === 'true') {
            delete_icon = document.createElement('span');
            delete_icon.classList.add('iuw-delete-icon');
            delete_icon.innerHTML = DeleteIcon;
        }
        if (this.canPreview) {
            const span = document.createElement('span');
            span.classList.add('iuw-preview-icon');
            if (related?.getAttribute('data-candelete') !== 'true') {
                span.classList.add('iuw-only-preview');
            }
            span.innerHTML = PreviewIcon;
            this.element.appendChild(span);
        }
        const img = document.createElement('img');
        img.src = link;
        this.element.appendChild(img);
        if (delete_icon) {
            this.element.appendChild(delete_icon);
        }
    }
}
