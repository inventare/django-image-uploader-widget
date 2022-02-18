import {
    renderWidget,
    testTwoWidgets,
    IMAGE_DATA,
    RAW_URL,
} from './Utils';

describe('Widget', () => {
    test('Widget instantiated must be correctly set variables', async () => {
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

    test('widget instantiated with "data-raw" must be correctly set variables', async () => {
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
    
    test('widget instantiated without "data-raw" must be not have any image-preview', async () => {
        await testTwoWidgets((widget, element, required) => {
            const preview = element.querySelectorAll('.iuw-image-preview');
            expect(preview).toHaveLength(0);
        });
    });
    
    test('widget instantiated with "data-raw" must be have a image-preview', async () => {
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
});