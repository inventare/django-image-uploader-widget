import { ImageUploaderWidget } from './ImageUploaderWidget';
import userEvent from '@testing-library/user-event';

const IMAGE_DATA = Buffer.from(
    'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TpSIVUQuKOGSogmBBVMRRq1CECqFWaNXB5NIvaNKQpLg4Cq4FBz8Wqw4uzro6uAqC4AeIm5uToouU+L+k0CLWg+N+vLv3uHsHCNUi06y2cUDTbTMRi4qp9KoYeEUQ/ejFKHpkZhlzkhRHy/F1Dx9f7yI8q/W5P0eXmrEY4BOJZ5lh2sQbxNObtsF5nzjE8rJKfE48ZtIFiR+5rnj8xjnnssAzQ2YyMU8cIhZzTaw0McubGvEUcVjVdMoXUh6rnLc4a8Uyq9+TvzCY0VeWuU5zCDEsYgkSRCgoo4AibERo1UmxkKD9aAv/oOuXyKWQqwBGjgWUoEF2/eB/8LtbKzs54SUFo0D7i+N8DAOBXaBWcZzvY8epnQD+Z+BKb/hLVWDmk/RKQwsfAd3bwMV1Q1P2gMsdYODJkE3Zlfw0hWwWeD+jb0oDfbdA55rXW30fpw9AkrqK3wAHh8BIjrLXW7y7o7m3f8/U+/sBgl1yrZQ5tlQAAAAJcEhZcwAALiMAAC4jAXilP3YAAAAHdElNRQflDBcSKSjsMuK5AAAAGXRFWHRDb21tZW50AENyZWF0ZWQgd2l0aCBHSU1QV4EOFwAAABpJREFUKM9jZNj7j4EUwMRAIhjVMKph6GgAAHyXAdui3YKhAAAAAElFTkSuQmCC',
    'base64'
);

const renderRequiredWidget = (rawUrl?: string) => {
    const html = `
        <div class="iuw-root" ${rawUrl ? ` data-raw="${rawUrl}"` : ''}>
            <input type="file" name="image" accept="image/*" id="image-widget" />
            
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
    const widget = new ImageUploaderWidget(element as HTMLElement);
    return { element, widget };
};

test('[Required Widget] Element of a widget instantiated without data-raw must be not contains "not-empty" class', () => {
    const { widget, element } = renderRequiredWidget();

    expect(widget.raw).toBeNull();
    expect(widget.file).toBeNull();
    expect(widget.id).toBe('image-widget');
    expect(widget.canDelete).toBe(false);
    expect(element.classList.contains('non-empty')).toBeFalsy();
});

test('[Required Widget] Element of a widget instantiated with data-raw must be contains "not-empty" class', () => {
    const raw = 'https://via.placeholder.com/350x150';
    const { widget, element } = renderRequiredWidget(raw);
    
    expect(widget.raw).toBe(raw);
    expect(widget.file).toBeNull();
    expect(widget.id).toBe('image-widget');
    expect(widget.canDelete).toBe(false);
    expect(element.classList.contains('non-empty')).toBeTruthy();
});

test('[Required Widget] image preview must be rendered with a img element', () => {
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

test('[Required Widget] must be possible to upload file and widget must be rendered with new file', () => {
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
    expect(img.src).toBe('aaatest::/file.png');
});

