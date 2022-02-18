import userEvent from '@testing-library/user-event';
import { testTwoWidgets, RAW_URL } from './Utils';
import { PreviewModal } from '../../PreviewModal/PreviewModal';

describe('Widget', () => {
    test('Click on the preview button must be call the open modal method', async () => {
        await testTwoWidgets(async (widget, element, required) => {
            const spyOpenPreviewModal = jest.spyOn(PreviewModal, 'openPreviewModal');
            const spyCreatePreviewModal = jest.spyOn(PreviewModal, 'createPreviewModal');
            
            
            const openPreviewModal = jest.fn();
            const createPreviewModal = jest.fn();
            spyOpenPreviewModal.mockImplementation(openPreviewModal);
            spyCreatePreviewModal.mockImplementation(createPreviewModal);

            expect(createPreviewModal).not.toHaveBeenCalled();
            expect(openPreviewModal).not.toHaveBeenCalled();

            // get and click in the preview button
            const previewButton = element.querySelector('.iuw-preview-icon');
            expect(previewButton).not.toBeNull();
            if (!previewButton) { // type check error only
                return;
            }
            userEvent.click(previewButton);
            
            expect(createPreviewModal).toHaveBeenCalled();
            expect(createPreviewModal).toHaveBeenCalledTimes(1);
            expect(openPreviewModal).toHaveBeenCalled();
            expect(openPreviewModal).toHaveBeenCalledTimes(1);

            spyOpenPreviewModal.mockClear();
            spyCreatePreviewModal.mockClear();
        }, RAW_URL);
    });
});
