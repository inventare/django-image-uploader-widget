class ImageUploaderWidget {
    constructor(element) {
        this.element = element;
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
