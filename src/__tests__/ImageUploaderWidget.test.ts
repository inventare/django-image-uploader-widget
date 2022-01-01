import userEvent from '@testing-library/user-event';
import { ImageUploaderWidget } from '../ImageUploaderWidget';

const RAW_URL = 'https://via.placeholder.com/350x150';

const IMAGE_DATA = Buffer.from(
    'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TpSIVUQuKOGSogmBBVMRRq1CECqFWaNXB5NIvaNKQpLg4Cq4FBz8Wqw4uzro6uAqC4AeIm5uToouU+L+k0CLWg+N+vLv3uHsHCNUi06y2cUDTbTMRi4qp9KoYeEUQ/ejFKHpkZhlzkhRHy/F1Dx9f7yI8q/W5P0eXmrEY4BOJZ5lh2sQbxNObtsF5nzjE8rJKfE48ZtIFiR+5rnj8xjnnssAzQ2YyMU8cIhZzTaw0McubGvEUcVjVdMoXUh6rnLc4a8Uyq9+TvzCY0VeWuU5zCDEsYgkSRCgoo4AibERo1UmxkKD9aAv/oOuXyKWQqwBGjgWUoEF2/eB/8LtbKzs54SUFo0D7i+N8DAOBXaBWcZzvY8epnQD+Z+BKb/hLVWDmk/RKQwsfAd3bwMV1Q1P2gMsdYODJkE3Zlfw0hWwWeD+jb0oDfbdA55rXW30fpw9AkrqK3wAHh8BIjrLXW7y7o7m3f8/U+/sBgl1yrZQ5tlQAAAAJcEhZcwAALiMAAC4jAXilP3YAAAAHdElNRQflDBcSKSjsMuK5AAAAGXRFWHRDb21tZW50AENyZWF0ZWQgd2l0aCBHSU1QV4EOFwAAABpJREFUKM9jZNj7j4EUwMRAIhjVMKph6GgAAHyXAdui3YKhAAAAAElFTkSuQmCC',
    'base64'
);

const renderWidget = (rawUrl?: string | null, required: boolean = false): { element: Element; widget: ImageUploaderWidget; } => {
    const html = `
        <div class="iuw-root" ${required ? '' : ' data-candelete="true" '} ${rawUrl ? ` data-raw="${rawUrl}"` : ''}>
            <input type="file" name="image" accept="image/*" id="image-widget" />
            
            <div class="iuw-drop-label">
                Drop your file here.
            </div>

            <div class="iuw-empty">
                The widget is empty.
            </div>

            ${required ? '' : '<input type="checkbox" name="image-clear" id="image-clear_id" />'}
        </div>
    `;
    document.body.innerHTML = html;
    const element = document.querySelector('.iuw-root');
    if (!element) {
        throw new Error('no element found');
    }
    const widget = new ImageUploaderWidget(element as HTMLElement);
    return { element, widget };
};

const testTwoWidgets = async (
    callback: (widget: ImageUploaderWidget, element: Element, required: boolean) => void | Promise<void>,
    rawUrl?: string | null
) => {
    {
        const { widget, element } = renderWidget(rawUrl, true);
        await callback(widget, element, true);
    }
    {
        const { widget, element } = renderWidget(rawUrl, false);
        await callback(widget, element, false);
    }
}

test('[Widget] widget instantiated must be correctly set variables', async () => {
    await testTwoWidgets((widget, element, required) => {
        // widget variables
        expect(widget.raw).toBeNull();
        expect(widget.file).toBeNull();
        expect(widget.canDelete).toBe(required ? false : true);
        expect(widget.element).toBe(element);
        // child elements
        expect(widget.fileInput).not.toBeNull();
        expect(widget.emptyMarker).not.toBeNull();
        if (required) {
            expect(widget.checkboxInput).toBeNull();
        } else {
            expect(widget.checkboxInput).not.toBeNull();
            // no images -> checkbox must be true
            expect(widget.checkboxInput?.checked).toBeTruthy();
        }
        // element variables
        expect(element.classList.contains('non-empty')).toBeFalsy();
    });
});

test('[Widget] widget instantiated with "data-raw" must be correctly set variables', async () => {
    await testTwoWidgets((widget, element, required) => {
        // widget variables
        expect(widget.raw).toBe(RAW_URL);
        expect(widget.file).toBeNull();
        expect(widget.canDelete).toBe(required ? false : true);
        expect(widget.element).toBe(element);
        // child elements
        expect(widget.fileInput).not.toBeNull();
        expect(widget.emptyMarker).not.toBeNull();
        if (required) {
            expect(widget.checkboxInput).toBeNull();
        } else {
            expect(widget.checkboxInput).not.toBeNull();
            expect(widget.checkboxInput?.checked).toBeFalsy();
        }
        // element variables
        expect(element.classList.contains('non-empty')).toBeTruthy();
    }, RAW_URL);
});

test('[Widget] widget instantiated without "data-raw" must be not have any image-preview', async () => {
    await testTwoWidgets((widget, element, required) => {
        const preview = element.querySelectorAll('.iuw-image-preview');
        expect(preview).toHaveLength(0);
    });
});

test('[Widget] widget instantiated with "data-raw" must be have a image-preview', async () => {
    await testTwoWidgets((widget, element, required) => {
        const preview = element.querySelectorAll('.iuw-image-preview');
        expect(preview).toHaveLength(1);

        const [previewItem] = preview;
        const image = previewItem.querySelector('img');

        expect(image).not.toBeNull();
        expect(image?.src).toBe(RAW_URL);

        if (required) {
            expect(previewItem.querySelector('.iuw-delete-icon')).toBeNull();
        } else {
            expect(previewItem.querySelector('.iuw-delete-icon')).not.toBeNull();
        }
        expect(previewItem.querySelector('.iuw-preview-icon')).not.toBeNull();
    }, RAW_URL);
});

test('[Widget] click on empty label must be call click on file input', async () => {
    await testTwoWidgets((widget, element, required) => {
        const { fileInput, emptyMarker } = widget;

        const clickFn = jest.fn();
        fileInput.click = clickFn;

        if (emptyMarker) {
            userEvent.click(emptyMarker);
            expect(clickFn).toBeCalledTimes(1);
        }
    });
});

test('[Widget] click on the preview button must be open a modal', async () => {
    await testTwoWidgets(async (widget, element, required) => {
        let modal = document.getElementById('iuw-modal-element');
        // no modal exists, when not clicked
        expect(modal).toBeNull();
        // get and click in the preview button
        const previewButton = element.querySelector('.iuw-preview-icon');
        expect(previewButton).not.toBeNull();
        
        if (!previewButton) { // type check error only
            return;
        }
        userEvent.click(previewButton);
        // get the modal and the image element
        modal = document.getElementById('iuw-modal-element');
        const image = modal?.querySelector('img');
        // await the modal open time
        await new Promise((resolve) => setTimeout(() => resolve(null), 100));
        // modal and image not be null
        expect(modal).not.toBeNull();
        expect(image).not.toBeNull();
        // modal visible class
        expect(modal?.classList.contains('visible')).toBeTruthy();
        // modal image src
        expect(image?.src).toBe(RAW_URL);
        // modal is not children of a iuw-root component
        expect(modal?.closest('.iuw-root')).toBeNull();
    }, RAW_URL);
});

test('[Widget] when the modal is open, click in the image must not close the modal', async () => {
    await testTwoWidgets(async (widget, element, required) => {
        const previewButton = element.querySelector('.iuw-preview-icon');
        expect(previewButton).not.toBeNull();
        if (!previewButton) { // type check error only
            return;
        }
        userEvent.click(previewButton);
        // await full modal open time
        await new Promise((resolve) => setTimeout(() => resolve(null), 600));
        // get the modal and the image
        let modal = document.getElementById('iuw-modal-element');
        const image = modal?.querySelector('img');
        expect(modal).not.toBeNull();
        expect(image).not.toBeNull();
        if (!modal || !image) { // type check error only
            return;
        }
        
        userEvent.click(image);

        // await full modal close time
        await new Promise((resolve) => setTimeout(() => resolve(null), 600));
        
        modal = document.getElementById('iuw-modal-element');
        expect(modal).not.toBeNull();
        if (!modal) { // type check error only
            return;
        }
        expect(modal?.classList.contains('visible')).toBeTruthy();
        expect(modal?.classList.contains('hide')).toBeFalsy();
    }, RAW_URL);
});

test('[Widget] when the modal is open, click in the modal close icon must be close the modal', async () => {
    await testTwoWidgets(async (widget, element, required) => {
        const previewButton = element.querySelector('.iuw-preview-icon');
        expect(previewButton).not.toBeNull();
        if (!previewButton) { // type check error only
            return;
        }
        userEvent.click(previewButton);
        // await full modal open time
        await new Promise((resolve) => setTimeout(() => resolve(null), 600));
        // get the modal and the image
        let modal = document.getElementById('iuw-modal-element');
        const closeButton = modal?.querySelector('.iuw-modal-close');
        expect(modal).not.toBeNull();
        expect(closeButton).not.toBeNull();
        if (!modal || !closeButton) { // type check error only
            return;
        }
        
        userEvent.click(closeButton);

        // await 100ms
        await new Promise((resolve) => setTimeout(() => resolve(null), 100));

        modal = document.getElementById('iuw-modal-element');
        expect(modal).not.toBeNull();
        expect(modal?.classList.contains('hide')).toBeTruthy();

        // await full modal close time
        await new Promise((resolve) => setTimeout(() => resolve(null), 500));
        
        modal = document.getElementById('iuw-modal-element');
        // modal must be destructed/removed
        expect(modal).toBeNull();
    }, RAW_URL);
});

test('[Widget] when try to instantiate the widget without file input must be thrown a error', async () => {
    const html = `
        <div class="iuw-root">
            <div class="iuw-drop-label">
                Drop your file here.
            </div>

            <div class="iuw-empty">
                The widget is empty.
            </div>
        </div>
    `;
    document.body.innerHTML = html;
    const element = document.querySelector('.iuw-root');
    expect(element).not.toBeNull();
    if (!element) { // type check only
        return;
    }
    expect(() => {
        new ImageUploaderWidget(element as HTMLElement);
    }).toThrowError('no-file-input-found');
});

test('[Widget] must be possible to upload file when "data-raw" is set and widget must be rendered with new file', () => {
    testTwoWidgets((widget, element, required) => {
        // checkbox
        if (!required) {
            expect(widget.checkboxInput).not.toBeNull();
            expect(widget.checkboxInput?.checked).toBeFalsy();
        }

        expect(element.classList.contains('non-empty')).toBeTruthy();

        // get preview
        let preview = element.querySelector('.iuw-image-preview');
        expect(preview).not.toBeNull();
        // get preview image
        let img = preview?.querySelector('img');
        expect(img).not.toBeNull();
        expect(img?.src).toBe(RAW_URL);

        // mock the createObjectURL
        global.URL.createObjectURL = jest.fn(() => 'test::/file.png');
        const file = new File([IMAGE_DATA], 'file.png', {type : 'image/png'});

        const fileInput = element.querySelector<HTMLInputElement>('input[type=file]');
        expect(fileInput).not.toBeNull();
        if (!fileInput) { // type check error only
            return;
        }
        userEvent.upload(fileInput, file);

        // check the file input changes
        expect(fileInput?.files).toHaveLength(1);
        expect(fileInput?.files?.item(0)).toStrictEqual(file);
        
        // get the new preview
        preview = document.querySelector('.iuw-image-preview');
        expect(preview).not.toBeNull();

        // check the new rendered item
        img = preview?.querySelector('img');
        expect(img).not.toBeNull();
        expect(img?.src).toBe('test::/file.png');

        expect(element.classList.contains('non-empty')).toBeTruthy();

        // checkbox
        if (!required) {
            expect(widget.checkboxInput).not.toBeNull();
            expect(widget.checkboxInput?.checked).toBeFalsy();
        }
    }, RAW_URL);
});

test('[Widget] must be possible to upload file when "data-raw" is not set and widget must be rendered with new file', () => {
    testTwoWidgets((widget, element, required) => {
        // checkbox
        if (!required) {
            expect(widget.checkboxInput).not.toBeNull();
            expect(widget.checkboxInput?.checked).toBeTruthy();
        }
        expect(element.classList.contains('non-empty')).toBeFalsy();

        // get preview
        let preview = element.querySelector('.iuw-image-preview');
        expect(preview).toBeNull();

        // mock the createObjectURL
        global.URL.createObjectURL = jest.fn(() => 'test::/file.png');
        const file = new File([IMAGE_DATA], 'file.png', {type : 'image/png'});

        const fileInput = element.querySelector<HTMLInputElement>('input[type=file]');
        expect(fileInput).not.toBeNull();
        if (!fileInput) { // type check error only
            return;
        }
        userEvent.upload(fileInput, file);

        // check the file input changes
        expect(fileInput?.files).toHaveLength(1);
        expect(fileInput?.files?.item(0)).toStrictEqual(file);
        
        // get the new preview
        preview = document.querySelector('.iuw-image-preview');
        expect(preview).not.toBeNull();

        // check the new rendered item
        const img = preview?.querySelector('img');
        expect(img).not.toBeNull();
        expect(img?.src).toBe('test::/file.png');
        
        expect(element.classList.contains('non-empty')).toBeTruthy();

        // checkbox
        if (!required) {
            expect(widget.checkboxInput).not.toBeNull();
            expect(widget.checkboxInput?.checked).toBeFalsy();
        }
    });
});

test('[Widget] click on preview image must be call click on file input', async () => {
    await testTwoWidgets((widget, element, required) => {
        const { fileInput } = widget;

        const clickFn = jest.fn();
        fileInput.click = clickFn;

        const preview = element.querySelectorAll('.iuw-image-preview');
        expect(preview).toHaveLength(1);

        const [previewItem] = preview;
        expect(previewItem).not.toBeNull();

        if (!previewItem) { // type check error only
            return;
        }

        userEvent.click(previewItem);

        expect(clickFn).toBeCalledTimes(1);
    }, RAW_URL);
});
