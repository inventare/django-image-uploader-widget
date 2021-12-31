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
    }, RAW_URL);
});

test('[Widget] click on empty label must be call click on file input', async () => {
    await testTwoWidgets((widget, element, required) => {
        const { fileInput, emptyMarker } = widget;

        const clickFn = jest.fn();
        fileInput.click = clickFn;

        userEvent.click(emptyMarker);

        expect(clickFn).toBeCalledTimes(1);
    });
});

/*
test('[Widget] widget instantiated with "data-raw" must be correctly initialize some variables', () => {
    const raw = 'https://via.placeholder.com/350x150';
    {
        // not required
        const { widget, element } = renderWidget(raw, false);
        
        expect(widget.raw).toBe(raw);
        expect(widget.file).toBeNull();
        expect(widget.id).toBe('image-widget');
        expect(widget.canDelete).toBe(true);
        expect(element.classList.contains('non-empty')).toBeTruthy();
    }
    {
        // required
        const { widget, element } = renderWidget(raw, true);
        
        expect(widget.raw).toBe(raw);
        expect(widget.file).toBeNull();
        expect(widget.id).toBe('image-widget');
        expect(widget.canDelete).toBe(false);
        expect(element.classList.contains('non-empty')).toBeTruthy();
    }
});

/*

test('[Widget] image preview must be rendered with a img element', () => {
    const raw = 'https://via.placeholder.com/350x150';
    renderRequiredWidget(raw);

    const preview = document.querySelector('.iuw-image-preview');
    expect(preview).not.toBeNull();

    const img = preview.querySelector('img');
    expect(img).not.toBeNull();
});

test('[Required Widget] close button for a image preview must not be rendered', () => {
    const raw = 'https://via.placeholder.com/350x150';
    renderRequiredWidget(raw);

    const closeButton = document.querySelector('.iuw-delete-icon');
    expect(closeButton).toBeNull();
});

test('[Widget] preview button for a image preview must be rendered', () => {
    const raw = 'https://via.placeholder.com/350x150';
    renderRequiredWidget(raw);

    const previewButton = document.querySelector('.iuw-preview-icon');
    expect(previewButton).not.toBeNull();
});



test('[Widget]')

test('[Widget] must be possible to upload file and widget must be rendered with new file', () => {
    const raw = 'https://via.placeholder.com/350x150';
    const { element } = renderRequiredWidget(raw);

    let preview = document.querySelector('.iuw-image-preview');
    expect(preview).not.toBeNull();

    let img = preview.querySelector('img');
    expect(img).not.toBeNull();
    expect(img.src).toBe(raw);

    global.URL.createObjectURL = jest.fn(() => 'test::/file.png');
    const file = new File([IMAGE_DATA], 'file.png', {type : 'image/png'});
    
    const fileInput = element.querySelector('input[type=file]') as HTMLInputElement;
    userEvent.upload(fileInput, file);

    expect(fileInput.files[0]).toStrictEqual(file)
    expect(fileInput.files.item(0)).toStrictEqual(file)
    expect(fileInput.files).toHaveLength(1)

    preview = document.querySelector('.iuw-image-preview');
    expect(preview).not.toBeNull();

    img = preview.querySelector('img');
    expect(img).not.toBeNull();
    expect(img.src).toBe('test::/file.png');
});

test('[Widget] click on preview button must be open a modal', async () => {
    const raw = 'https://via.placeholder.com/350x150';
    renderRequiredWidget(raw);

    let modal = document.getElementById('iuw-modal-element');
    expect(modal).toBeNull();

    const previewButton = document.querySelector('.iuw-preview-icon');
    userEvent.click(previewButton);

    //await new Promise((resolve) => setTimeout(() => resolve(null), 500));
    modal = document.getElementById('iuw-modal-element');
    const image = modal.querySelector('img');

    expect(modal).not.toBeNull();
    expect(image).not.toBeNull();
    expect(image.src).toEqual(raw);
});

*/
