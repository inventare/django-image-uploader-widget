import userEvent from '@testing-library/user-event';
import { ImageUploaderInline } from '../../Inline/Editor';
import * as Utils from '../../Inline/Utils';
import { getBySelector } from '../../test/querySelector';
import { getMockInlineTemplate } from '../../__mocks__/mockInlineTemplate';

describe('ImageUploaderInline', () => {
    it('constructor must call getInlineGroupOrThrow and parseFormSet', () => {
        document.body.innerHTML = getMockInlineTemplate({});

        const spyGetInlineGroupOrThrow = jest.spyOn(Utils, 'getInlineGroupOrThrow');
        const spyParseFormSet = jest.spyOn(Utils, 'parseFormSet');

        const root = getBySelector('.iuw-inline-root');
        new ImageUploaderInline(root);

        expect(spyGetInlineGroupOrThrow).toHaveBeenCalled();
        expect(spyGetInlineGroupOrThrow).toHaveBeenCalledTimes(1);
        expect(spyParseFormSet).toHaveBeenCalled();
        expect(spyParseFormSet).toHaveBeenCalledTimes(1);
    });

    it('constructor without default image must not have non-empty class', () => {
        document.body.innerHTML = getMockInlineTemplate({});

        const root = getBySelector('.iuw-inline-root');
        new ImageUploaderInline(root);

        expect(root).not.toHaveClass('non-empty');
    });

    it('constructor with default image must have non-empty class', () => {
        document.body.innerHTML = getMockInlineTemplate({ images: ['test/base.png'] });

        const root = getBySelector('.iuw-inline-root');
        new ImageUploaderInline(root);

        expect(root).toHaveClass('non-empty');
    });

    it('constructor with default image must update the next counter', () => {
        document.body.innerHTML = getMockInlineTemplate({ images: ['test/base.png'] });

        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);

        expect(editor.next).toEqual(1);
    });

    it('constructor initialize maxCount from the management input', () => {
        document.body.innerHTML = getMockInlineTemplate({ images: ['test/base.png'], maxCount: 40 });

        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);

        expect(editor.maxCount).toEqual(40);
    });

    it('constructor initialize maxCount as max_safe_integer if no set in input', () => {
        document.body.innerHTML = getMockInlineTemplate({ images: ['test/base.png'], maxCount: '' });

        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);

        expect(editor.maxCount).toEqual(Number.MAX_SAFE_INTEGER);
    });

    it('constructor must add visible-by-number to add button if not reached the limit ', () => {
        document.body.innerHTML = getMockInlineTemplate({ images: ['test/base.png'] });

        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);

        expect(editor.addImageButton).toHaveClass('visible-by-number');
    });

    it('constructor must remove visible-by-number to add button if reached the limit ', () => {
        document.body.innerHTML = getMockInlineTemplate({ images: ['test/base.png'], maxCount: 1 });

        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);

        expect(editor.addImageButton).not.toHaveClass('visible-by-number');
    });

    it('constructor must create correctly EditorImage objects', () => {
        document.body.innerHTML = getMockInlineTemplate({ images: ['test/base.png', 'two/base.png'] });

        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);

        // two and the empty
        expect(editor.images).toHaveLength(3);
        editor.images.forEach((img) => {
            expect(img.element).toBeInTheDocument();
        });
    });

    it('click on the add button must call handleAddImage method', async () => {
        const handleAddImage = jest.spyOn(ImageUploaderInline.prototype, 'handleAddImage');

        document.body.innerHTML = getMockInlineTemplate({});
        
        const root = getBySelector('.iuw-inline-root');
        
        const editor = new ImageUploaderInline(root);
        userEvent.click(editor.addImageButton);

        expect(handleAddImage).toHaveBeenCalled();
        expect(handleAddImage).toHaveBeenCalledTimes(1);

        jest.clearAllMocks();
    });

    it('click on the empty label must call handleAddImage method', async () => {
        const handleAddImage = jest.spyOn(ImageUploaderInline.prototype, 'handleAddImage');

        document.body.innerHTML = getMockInlineTemplate({});
        
        const root = getBySelector('.iuw-inline-root');
        
        new ImageUploaderInline(root);
        userEvent.click(getBySelector('.iuw-empty'));

        expect(handleAddImage).toHaveBeenCalled();
        expect(handleAddImage).toHaveBeenCalledTimes(1);

        jest.clearAllMocks();
    });
});
