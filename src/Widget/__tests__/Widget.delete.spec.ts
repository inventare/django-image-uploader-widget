import userEvent from '@testing-library/user-event';
import {
    renderWidget,
    RAW_URL,
    IMAGE_DATA
} from './Utils';

describe("Widget", () => {
    test('Click on the delete icon on the preview image must be remove the image if it is not the raw', async () => {
        const { element, widget } = renderWidget(undefined, false);
    
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
        let previews = element.querySelectorAll('.iuw-image-preview');
        expect(previews).toHaveLength(1)
        let [preview] = previews;
        // check the new rendered item
        const img = preview?.querySelector('img');
        expect(img).not.toBeNull();
        expect(img?.src).toBe('test::/file.png');
    
        expect(widget.checkboxInput).not.toBeNull();
        expect(widget.checkboxInput?.checked).toBeFalsy();
    
        const deleteButton = preview?.querySelector('.iuw-delete-icon');
        expect(deleteButton).not.toBeNull();
    
        if (!deleteButton) { // type check only
            return;
        }
    
        userEvent.click(deleteButton);
    
        previews = element.querySelectorAll('.iuw-image-preview');
        expect(previews).toHaveLength(0);
        
        expect(widget.checkboxInput?.checked).toBeTruthy();
    });
    
    test('Click on the delete icon on the preview image must be check the checkbox if it is the raw', async () => {
        const { element, widget } = renderWidget(RAW_URL, false);
       
        // get the new preview
        let previews = element.querySelectorAll('.iuw-image-preview');
        expect(previews).toHaveLength(1);
        const [preview] = previews;
        // check the new rendered item
        const img = preview?.querySelector('img');
        expect(img).not.toBeNull();
        expect(img?.src).toBe(RAW_URL);
    
        expect(widget.checkboxInput).not.toBeNull();
        expect(widget.checkboxInput?.checked).toBeFalsy();
    
        const deleteButton = preview?.querySelector('.iuw-delete-icon');
        expect(deleteButton).not.toBeNull();
    
        if (!deleteButton) { // type check only
            return;
        }
    
        userEvent.click(deleteButton);
    
        previews = element.querySelectorAll('.iuw-image-preview');
        expect(previews).toHaveLength(0);
        
        expect(widget.checkboxInput?.checked).toBeTruthy();
    });
});
