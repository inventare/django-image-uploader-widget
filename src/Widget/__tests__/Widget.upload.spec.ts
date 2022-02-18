import userEvent from '@testing-library/user-event';
import {
    testTwoWidgets,
    RAW_URL,
    IMAGE_DATA
} from './Utils';

describe("Widget", () => {
    test('click on empty label must be call click on file input', async () => {
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

    test('Must be possible to upload file when "data-raw" is set and widget must be rendered with new file', () => {
        testTwoWidgets((widget, element, required) => {
            // checkbox
            if (!required) {
                expect(widget.checkboxInput).not.toBeNull();
                expect(widget.checkboxInput?.checked).toBeFalsy();
            }
    
            expect(element.classList.contains('non-empty')).toBeTruthy();
    
            // get preview
            let previews = element.querySelectorAll('.iuw-image-preview');
            expect(previews).toHaveLength(1);
            let [preview] = previews;
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
            previews = document.querySelectorAll('.iuw-image-preview');
            expect(previews).toHaveLength(1);
            preview = previews[0];
    
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

    test('Must be possible to upload file when "data-raw" is not set and widget must be rendered with new file', () => {
        testTwoWidgets((widget, element, required) => {
            // checkbox
            if (!required) {
                expect(widget.checkboxInput).not.toBeNull();
                expect(widget.checkboxInput?.checked).toBeTruthy();
            }
            expect(element.classList.contains('non-empty')).toBeFalsy();
    
            // get preview
            let previews = element.querySelectorAll('.iuw-image-preview');
            expect(previews).toHaveLength(0)
    
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
            previews = document.querySelectorAll('.iuw-image-preview');
            expect(previews).toHaveLength(1);
            const preview = previews[0];
    
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
    
    test('Click on preview image must be call click on file input', async () => {
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
});
