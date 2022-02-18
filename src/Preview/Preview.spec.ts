import { renderPreview } from './Preview';
import { RAW_URL } from '../Widget/__tests__/Utils';

describe('Preview', () => {
    function renderPreviewAndTest(canDelete: boolean, canPreview: boolean) {
        // render
        const element = renderPreview(RAW_URL, canDelete, canPreview);
        // test
        expect(element).toHaveClass('iuw-image-preview');
        expect(element.querySelectorAll('img')).toHaveLength(1);
        return element;
    }

    test('renderPreview without canDelete and canPreview must render an preview and an img', () => {
        const element = renderPreviewAndTest(false, false);
        
        expect(element).toHaveClass('iuw-image-preview');
        expect(element.querySelectorAll('img')).toHaveLength(1);
        
        expect(element.querySelectorAll('.iuw-preview-icon')).toHaveLength(0);
        expect(element.querySelectorAll('.iuw-delete-icon')).toHaveLength(0);
        
        const [image] = element.querySelectorAll('img');
        
        expect(image.src).toBe(RAW_URL);
    });
    
    test('renderPreview with canDelete and without canPreview must render an preview and an img and the delete button', () => {
        const element = renderPreviewAndTest(true, false);

        expect(element.querySelectorAll('.iuw-delete-icon')).toHaveLength(1);
        expect(element.querySelectorAll('.iuw-preview-icon')).toHaveLength(0);
        
        const [image] = element.querySelectorAll('img');
        
        expect(image.src).toBe(RAW_URL);
    });
    
    test('renderPreview without canDelete and with canPreview must render an preview and an img and the preview button', () => {
        const element = renderPreviewAndTest(false, true);

        expect(element.querySelectorAll('.iuw-delete-icon')).toHaveLength(0);
        expect(element.querySelectorAll('.iuw-preview-icon')).toHaveLength(1);
        
        const [image] = element.querySelectorAll('img');
        
        expect(image.src).toBe(RAW_URL);
    });

    test('renderPreview with canDelete and canPreview must render an preview and an img and the delete and the preview button', () => {
        const element = renderPreviewAndTest(true, true);

        expect(element.querySelectorAll('.iuw-delete-icon')).toHaveLength(1);
        expect(element.querySelectorAll('.iuw-preview-icon')).toHaveLength(1);
        
        const [image] = element.querySelectorAll('img');
        
        expect(image.src).toBe(RAW_URL);
    });
});
