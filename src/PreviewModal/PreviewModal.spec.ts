import userEvent from '@testing-library/user-event';
import { PreviewModal } from './PreviewModal';

describe('PreviewModal', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
    });

    test('createPreviewModal must be append widget in the document body', () => {
        const img = document.createElement('img');
        const modal = PreviewModal.createPreviewModal(img);
        
        expect(modal).toBeInTheDocument();
        expect(img).toBeInTheDocument();
        expect(document.querySelectorAll('.iuw-modal-close')).toHaveLength(1);
    });

    test('click on Modal Preview Image must not close the modal', () => {
        const img = document.createElement('img');
        PreviewModal.createPreviewModal(img);

        const { closePreviewModal } = PreviewModal;
        PreviewModal.closePreviewModal = jest.fn();

        userEvent.click(img);
        expect(PreviewModal.closePreviewModal).not.toBeCalled();
        
        PreviewModal.closePreviewModal = closePreviewModal;
    });

    test('click on Modal outside of the preview image must close the modal', () => {
        const img = document.createElement('img');
        const modal = PreviewModal.createPreviewModal(img);
        
        const { closePreviewModal } = PreviewModal;
        PreviewModal.closePreviewModal = jest.fn();

        userEvent.click(modal);
        expect(PreviewModal.closePreviewModal).toBeCalled();
        expect(PreviewModal.closePreviewModal).toBeCalledTimes(1);
        
        PreviewModal.closePreviewModal = closePreviewModal;
    });

    test('click on Modal close button must close the modal', () => {
        const img = document.createElement('img');
        PreviewModal.createPreviewModal(img);
        const closeButton = document.querySelector('.iuw-modal-close');

        expect(closeButton).toBeInTheDocument();
        if (!closeButton) {
            return;
        }

        const { closePreviewModal } = PreviewModal;
        PreviewModal.closePreviewModal = jest.fn();

        userEvent.click(closeButton);
        expect(PreviewModal.closePreviewModal).toBeCalled();
        expect(PreviewModal.closePreviewModal).toBeCalledTimes(1);
        
        PreviewModal.closePreviewModal = closePreviewModal;
    });

    test('openPreviewModal must change modal classes after 51ms and change document body overflow to hidden', async () => {
        const img = document.createElement('img');
        const modal = PreviewModal.createPreviewModal(img);
        PreviewModal.openPreviewModal();
        
        await new Promise((resolve) => setTimeout(resolve, 51));

        expect(modal).toBeInTheDocument();
        if (!modal) {
            return;
        }
        
        expect(modal).toHaveClass('visible');
        expect(modal).not.toHaveClass('hide');
        expect(document.body).toHaveStyle('overflow: hidden');
    });

    test('openPreviewModal must be not throw Error if no modal in document', async () => {
        expect(() => {
            PreviewModal.openPreviewModal();
        }).not.toThrow();

        await new Promise((resolve) => setTimeout(resolve, 51));

        const modal = document.getElementById('iuw-modal-element');
        expect(modal).not.toBeInTheDocument();
    });

    test('closePreviewModal must be change modal classes and set document body overflow to auto', async () => {
        const img = document.createElement('img');
        const modal = PreviewModal.createPreviewModal(img);
        PreviewModal.openPreviewModal();
        
        await new Promise((resolve) => setTimeout(resolve, 51));

        PreviewModal.closePreviewModal();

        expect(modal).toHaveClass('hide');
        expect(modal).not.toHaveClass('visible');
        expect(document.body).toHaveStyle('overflow: auto');
    });

    test('closePreviewModal must be remove the modal element after 300ms', async () => {
        const img = document.createElement('img');
        const modal = PreviewModal.createPreviewModal(img);
        PreviewModal.openPreviewModal();
        
        await new Promise((resolve) => setTimeout(resolve, 51));

        PreviewModal.closePreviewModal();

        expect(modal).toBeInTheDocument();

        await new Promise((resolve) => setTimeout(resolve, 301));

        expect(modal).not.toBeInTheDocument();
    });

    test('closePreviewModal must be not throw Error if no modal in document', async () => {
        expect(() => {
            PreviewModal.closePreviewModal();
        }).not.toThrow();

        await new Promise((resolve) => setTimeout(resolve, 301));

        const modal = document.getElementById('iuw-modal-element');
        expect(modal).not.toBeInTheDocument();
    });
});
