import userEvent from '@testing-library/user-event';
import { getBySelector } from "../../test/querySelector";
import { getMockImageItem } from "../../__mocks__/mockInlineTemplate";
import { EditorImage } from '../../Inline/EditorImage';
import { PreviewModal } from '../../PreviewModal';

describe('EditorImage', () => {
    it('constructor must preserve the inputs', () => {
        document.body.innerHTML = getMockImageItem({ image: 'test/image.png' });

        const item = getBySelector('.inline-related');
        const inputs = item.querySelectorAll('input');

        new EditorImage(item, true);
        
        Array.from(inputs).forEach((input) => expect(input).toBeInTheDocument());
    });

    it('constructor must create an preview button if canPreview was true', () => {
        document.body.innerHTML = getMockImageItem({ image: 'test/image.png' });
        
        const item = getBySelector('.inline-related');
        
        new EditorImage(item, true);

        expect(getBySelector('.iuw-preview-icon')).toBeInTheDocument();
    });

    it('constructor must not create an preview button if canPreview was false', () => {
        document.body.innerHTML = getMockImageItem({ image: 'test/image.png' });
        
        const item = getBySelector('.inline-related');
        
        new EditorImage(item, false);

        expect(() => getBySelector('.iuw-preview-icon')).toThrow();
    });

    it('constructor must create an delete button if canDelete was true', () => {
        document.body.innerHTML = getMockImageItem({ image: 'test/image.png', canDelete: true });
        
        const item = getBySelector('.inline-related');
        
        new EditorImage(item, true);

        expect(getBySelector('.iuw-delete-icon')).toBeInTheDocument();
    });

    it('constructor must not create an delete button if canDelete was false', () => {
        document.body.innerHTML = getMockImageItem({ image: 'test/image.png', canDelete: false });
        
        const item = getBySelector('.inline-related');
        
        new EditorImage(item, true);

        expect(() => getBySelector('.iuw-delete-icon')).toThrow();
    });

    it('constructor must create an image tag with valid src', () => {
        document.body.innerHTML = getMockImageItem({ image: 'test/image.png' });

        const item = getBySelector('.inline-related');
        new EditorImage(item, true);

        const img = getBySelector('img');
        expect(img).toBeInTheDocument();
        expect(img.getAttribute('src')).toEqual('test/image.png');
    });

    it('constructor must not create an image tag if no valid image was parsed', () => {
        document.body.innerHTML = getMockImageItem({ image: null });

        const item = getBySelector('.inline-related');
        new EditorImage(item, true);

        expect(() => getBySelector('img')).toThrow();
    });

    it('constructor must render an parsed image url', () => {
        document.body.innerHTML = getMockImageItem({ image: null });

        const item = getBySelector('.inline-related');
        new EditorImage(item, true, 'image/data.png');

        const img = getBySelector('img');
        expect(img).toBeInTheDocument();
        expect(img.getAttribute('src')).toEqual('image/data.png');
    });

    it('click on the delete icon must call the onDelete handler', () => {
        document.body.innerHTML = getMockImageItem({ image: null, canDelete: true });

        const item = getBySelector('.inline-related');
        const image = new EditorImage(item, true, 'image/data.png');

        image.onDelete = jest.fn();

        const deleteButton = getBySelector('.iuw-delete-icon');
        userEvent.click(deleteButton);

        expect(image.onDelete).toBeCalled();
        expect(image.onDelete).toBeCalledTimes(1);
    });

    it('click on the preview icon must call open the image modal', () => {
        const spyOpenPreviewModal = jest.spyOn(PreviewModal, 'openPreviewModal');
        const spyCreatePreviewModal = jest.spyOn(PreviewModal, 'createPreviewModal');
        const openPreviewModal = jest.fn();
        const createPreviewModal = jest.fn();
        spyOpenPreviewModal.mockImplementation(openPreviewModal);
        spyCreatePreviewModal.mockImplementation(createPreviewModal);

        document.body.innerHTML = getMockImageItem({ image: null, canDelete: true });

        const item = getBySelector('.inline-related');
        const image = new EditorImage(item, true, 'image/data.png');

        expect(createPreviewModal).not.toHaveBeenCalled();
        expect(openPreviewModal).not.toHaveBeenCalled();

        const previewButton = getBySelector('.iuw-preview-icon');
        userEvent.click(previewButton);

        expect(createPreviewModal).toHaveBeenCalled();
        expect(createPreviewModal).toHaveBeenCalledTimes(1);
        expect(openPreviewModal).toHaveBeenCalled();
        expect(openPreviewModal).toHaveBeenCalledTimes(1);

        spyOpenPreviewModal.mockClear();
        spyCreatePreviewModal.mockClear();
    });

    it('click on the outside of the input must call the input click', () => {
        document.body.innerHTML = getMockImageItem({ image: null, canDelete: true });

        const item = getBySelector('.inline-related');
        const image = new EditorImage(item, true, 'image/data.png');
        
        const fileInput = item.querySelector('input') as HTMLInputElement;
        const imageTag = item.querySelector('img') as HTMLElement;

        fileInput.click = jest.fn();

        userEvent.click(imageTag);

        expect(fileInput.click).toBeCalled();
        expect(fileInput.click).toBeCalledTimes(1);
    });

    it('click on the inside of the input must not call the input click() method', () => {
        document.body.innerHTML = getMockImageItem({ image: null, canDelete: true });

        const item = getBySelector('.inline-related');
        const image = new EditorImage(item, true, 'image/data.png');
        
        const fileInput = item.querySelector('input') as HTMLInputElement;

        fileInput.click = jest.fn();
        userEvent.click(fileInput);

        expect(fileInput.click).not.toBeCalled();
    });
});