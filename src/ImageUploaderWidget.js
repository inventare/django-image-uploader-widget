class ImageUploaderWidget {
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
        this.renderWidget();
    }

    browseFile() {
        this.fileInput.click();
    }

    previewClick(e) {
        if (e && e.target && e.target.classList.contains('iuw-delete-icon')) {
            const element = e.target.closest('.iuw-image-preview');
            element.parentElement.removeChild(element);
            this.checkboxInput.checked = true;
            this.fileInput.value = null;
            this.renderWidget();
            return;
        }
        this.fileInput.click();
    }

    fileChange() {
        this.renderWidget();
    }

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

    renderWidget() {
        if (this.fileInput.files.length === 0 && !this.raw) {
            this.fileInput.classList.remove('non-empty');
            if (this.checkboxInput) {
                this.checkboxInput.checked = true;
            }
        } else {
            this.fileInput.classList.add('non-empty');
            if (this.checkboxInput) {
                this.checkboxInput.checked = false;
            }
        }

        Array
            .from(this.element.querySelectorAll('.iuw-image-preview'))
            .forEach((item) => this.element.removeChild(item));
        if (this.fileInput.files.length > 0) {
            const url = URL.createObjectURL(this.fileInput.files[0]);
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
    const elements = Array.from(
        document.querySelectorAll('.iuw-root'),
    );
    elements.forEach((element) => {
        const iuw = new ImageUploaderWidget(element);
    });

    // $ = window.django.jQuery;
    // TODO: add a event handler to inlines
});

// export for testing purpose
export { ImageUploaderWidget };
