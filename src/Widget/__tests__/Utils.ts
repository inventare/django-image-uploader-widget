import { ImageUploaderWidget } from '../Widget';

export const RAW_URL = 'https://via.placeholder.com/350x150';

export const IMAGE_DATA = Buffer.from(
    'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TpSIVUQuKOGSogmBBVMRRq1CECqFWaNXB5NIvaNKQpLg4Cq4FBz8Wqw4uzro6uAqC4AeIm5uToouU+L+k0CLWg+N+vLv3uHsHCNUi06y2cUDTbTMRi4qp9KoYeEUQ/ejFKHpkZhlzkhRHy/F1Dx9f7yI8q/W5P0eXmrEY4BOJZ5lh2sQbxNObtsF5nzjE8rJKfE48ZtIFiR+5rnj8xjnnssAzQ2YyMU8cIhZzTaw0McubGvEUcVjVdMoXUh6rnLc4a8Uyq9+TvzCY0VeWuU5zCDEsYgkSRCgoo4AibERo1UmxkKD9aAv/oOuXyKWQqwBGjgWUoEF2/eB/8LtbKzs54SUFo0D7i+N8DAOBXaBWcZzvY8epnQD+Z+BKb/hLVWDmk/RKQwsfAd3bwMV1Q1P2gMsdYODJkE3Zlfw0hWwWeD+jb0oDfbdA55rXW30fpw9AkrqK3wAHh8BIjrLXW7y7o7m3f8/U+/sBgl1yrZQ5tlQAAAAJcEhZcwAALiMAAC4jAXilP3YAAAAHdElNRQflDBcSKSjsMuK5AAAAGXRFWHRDb21tZW50AENyZWF0ZWQgd2l0aCBHSU1QV4EOFwAAABpJREFUKM9jZNj7j4EUwMRAIhjVMKph6GgAAHyXAdui3YKhAAAAAElFTkSuQmCC',
    'base64'
);

export interface RenderWidgetResult {
    element: Element;
    widget: ImageUploaderWidget;
}

export const renderWidget = (
    rawUrl?: string | null,
    required: boolean = false
): RenderWidgetResult => {
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

export type TestTwoWidgetsCallback = (
    widget: ImageUploaderWidget,
    element: Element, required: boolean
) => void | Promise<void>;

export const testTwoWidgets = async (
    callback: TestTwoWidgetsCallback,
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
