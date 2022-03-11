import userEvent from '@testing-library/user-event';
import { ImageUploaderInline } from '../../Inline/Editor';
import * as Utils from '../../Inline/Utils';
import { getBySelector } from '../../test/querySelector';
import { getMockInlineTemplate } from '../../__mocks__/mockInlineTemplate';
import { getMockFile } from '../../__mocks__/mockImageData';

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

    it('call the handleAddImage method must create the tempFileInput', async () => {
        document.body.innerHTML = getMockInlineTemplate({});

        const root = getBySelector('.iuw-inline-root');

        const editor = new ImageUploaderInline(root);
        
        expect(editor.tempFileInput).not.toBeInTheDocument();
        editor.handleAddImage();
        expect(editor.tempFileInput).toBeInTheDocument();
    });

    it('call the handleAddImage method must call the tempFileInput click', async () => {
        document.body.innerHTML = getMockInlineTemplate({});

        const root = getBySelector('.iuw-inline-root');

        const editor = new ImageUploaderInline(root);
        
        editor.tempFileInput = document.createElement('input');
        editor.tempFileInput.click = jest.fn();

        editor.handleAddImage();

        expect(editor.tempFileInput.click).toBeCalled();
        expect(editor.tempFileInput.click).toBeCalledTimes(1);
    });

    it('changing the image of the tempFileInput must call the addFile method', async () => {
        const addFile = jest.spyOn(ImageUploaderInline.prototype, 'addFile');

        document.body.innerHTML = getMockInlineTemplate({});
        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);
        editor.handleAddImage();
        
        const mockFile = getMockFile();
        userEvent.upload(editor.tempFileInput as HTMLInputElement, mockFile);

        expect(addFile).toBeCalled();
        expect(addFile).toBeCalledTimes(1);

        jest.clearAllMocks();
    });

    it('changing the image of the tempFileInput must add an new EditorImage', async () => {
        document.body.innerHTML = getMockInlineTemplate({});
        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);
        editor.handleAddImage();

        expect(editor.images).toHaveLength(1);

        const mockFile = getMockFile();
        userEvent.upload(editor.tempFileInput as HTMLInputElement, mockFile);

        expect(editor.images).toHaveLength(2);
    });

    it('if no template empty-form is present, when uploading a file, must throw an error', async () => {
        document.body.innerHTML = getMockInlineTemplate({ emptyForm: false });
        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);
        editor.handleAddImage();

        expect(() => editor.addFile()).toThrowError('no-empty-template');
    });

    it('if no temp file input is present, when call addFile, must throw an error', async () => {
        document.body.innerHTML = getMockInlineTemplate({});
        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);

        expect(() => editor.addFile()).toThrowError('no-temp-input-for-upload');
    });

    it('if no file in the input is present, when call addFile, must throw an error', async () => {
        document.body.innerHTML = getMockInlineTemplate({});
        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);
        editor.handleAddImage();

        expect(() => editor.addFile()).toThrowError('no-file-in-input');
    });

    it('if no file in the input change event, addFile must not called', async () => {
        const addFile = jest.spyOn(ImageUploaderInline.prototype, 'addFile');

        document.body.innerHTML = getMockInlineTemplate({});
        const root = getBySelector('.iuw-inline-root');
        const editor = new ImageUploaderInline(root);
        editor.handleAddImage();
        
        const event = new Event('change');
        editor.tempFileInput?.dispatchEvent(event);

        expect(addFile).not.toBeCalled();

        jest.clearAllMocks();
    });
});
