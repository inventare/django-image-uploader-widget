import { getBySelector } from "../../test/querySelector";
import { getMockImageItem } from "../../__mocks__/mockInlineTemplate";
import { EditorImage } from '../../Inline/EditorImage';

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
});