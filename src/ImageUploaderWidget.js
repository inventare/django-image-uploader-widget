/**
 * A class that manage a Image Uploader Widget.
 */
class ImageUploaderWidget {
    /**
     * Creates a new ImageUploaderWidget instance.
     * @param {HTMLElement} element the root element.
     */
    constructor(element) {
        this.element = element;
        this.fileInput = element.querySelector('input[type=file]');
        this.checkboxInput = element.querySelector('input[type=checkbox]');
        this.emptyMarker = this.element.querySelector('.iuw-empty');
        this.canDelete = element.getAttribute('data-candelete') === 'true';

        // add events
        this.fileChange = this.fileChange.bind(this);
        this.browseFile = this.browseFile.bind(this);
        this.previewClick = this.previewClick.bind(this);
        this.fileInput.addEventListener('change', this.fileChange);
        if (this.emptyMarker) {
            this.emptyMarker.addEventListener('click', this.browseFile);
        }
        // init
        this.raw = element.getAttribute('data-raw');
        this.file = null;
        this.renderWidget();
    }

    /**
     * A method called to open the file browser dialog.
     */
    browseFile() {
        this.fileInput.click();
    }

    /**
     * Event called when user clicks on the preview image element.
     * @param {MouseEvent} e the click mouse event.
     * @returns undefined.
     */
    previewClick(e) {
        if (e && e.target && e.target.closest('.iuw-delete-icon')) {
            const element = e.target.closest('.iuw-image-preview');
            element.parentElement.removeChild(element);
            this.checkboxInput.checked = true;
            this.fileInput.value = null;
            this.file = null;
            this.raw = null;
            this.renderWidget();
            return;
        }
        this.fileInput.click();
    }

    /**
     * Event called when the file input file is changed.
     */
    fileChange() {
        if (this.fileInput.files.length > 0) {
            this.file = this.fileInput.files[0];
        }
        this.renderWidget();
    }

    /**
     * render a preview image element.
     * @param {String} url the url of the preview image.
     * @returns HTMLElement
     */
    renderPreview(url) {
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

    /**
     * update the rendered widget.
     */
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
            .forEach((item) => item.addEventListener('click', this.previewClick));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    Array
        .from(document.querySelectorAll('.iuw-root'))
        .map((element) => new ImageUploaderWidget(element));

    if (window && window.django && window.django.jQuery) {
        $ = window.django.jQuery;
        
        $(document).on('formset:added', (_, row) => {
            if (!row.length) {
                return;
            }
            Array
                .from(row[0].querySelectorAll('.iuw-root'))
                .map((element) => new ImageUploaderWidget(element));
        });
    }
});

// export for testing
export { ImageUploaderWidget };
