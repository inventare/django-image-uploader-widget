import {
    getInlineGroupOrThrow,
    ImageUploaderInlineFormSet,
    parseFormSet,
    updateElementIndex,
    updateAllElementsIndexes,
    getAddButton,
    getManagementInputs,
    createTempFileInput,
} from "../../Inline/Utils";
import { getBySelector } from '../../test/querySelector';
import { getMockManagementForms } from '../../__mocks__/mockInlineTemplate';

describe('Utils', () => {
    it('getInlineGroupOrThrow must return the parent element with inline-group class', () => {
        document.body.innerHTML = '<div class="inline-group"><div class="inline-test"></div></div>';
        
        const testElement = getBySelector('.inline-test');
        expect(getInlineGroupOrThrow(testElement)).toBeInTheDocument();
    });

    it('getInlineGroupOrThrow must throw an error if no inline-group element found as parent', () => {
        document.body.innerHTML = '<div class="no-inline-group"><div class="inline-test"></div></div>';
        
        const testElement = getBySelector('.inline-test');
        expect(() => getInlineGroupOrThrow(testElement)).toThrow();
    });

    it('parseFormSet must returns the parsed json data of the attr', () => {
        const json: ImageUploaderInlineFormSet = {
            name: 'test',
            options: {
                addText: 'add',
                deleteText: 'delete',
                prefix: 'prefix',
            },
        };
        document.body.innerHTML = `<div class="test" data-inline-formset='${JSON.stringify(json)}'></div>`;
        
        const testElement = getBySelector('.test');
        const parsed = parseFormSet(testElement);
        expect(parsed).toMatchObject(json);
    });

    it('parseFormSet must thrown an error if no attr exists', () => {
        document.body.innerHTML = '<div class="test"></div>';
        
        const testElement = getBySelector('.test');
        expect(() => parseFormSet(testElement)).toThrow();
    });

    it('updateElementIndex must update for, id and name __prefix__ and -index-', () => {
        document.body.innerHTML = '<label class="test" id="test-1" name="test-__prefix__-name" for="test-__prefix__-id">Input</label>';
        
        const testElement = getBySelector('.test');
        updateElementIndex(testElement, 'test', 5);

        expect(testElement.getAttribute('for')).toEqual('test-5-id');
        expect(testElement.getAttribute('id')).toEqual('test-5');
        expect(testElement.getAttribute('name')).toEqual('test-5-name');
    });

    it('updateAllElementsIndexes must update all childs', () => {
        document.body.innerHTML = '<div id="test-4" class="test"><label for="test-__prefix__-id">Input</label><input id="test-1-id" name="test-__prefix__-name" /></div>';

        const testElement = getBySelector('.test');
        updateAllElementsIndexes(testElement, 'test', 5);

        const labelElement = getBySelector('.test > label');
        const inputElement = getBySelector('.test > input');

        expect(testElement.getAttribute('id')).toEqual('test-5');
        expect(labelElement.getAttribute('for')).toEqual('test-5-id');
        expect(inputElement.getAttribute('id')).toEqual('test-5-id');
        expect(inputElement.getAttribute('name')).toEqual('test-5-name');
    });

    it('getAddButton must return the element with the correctly class', () => {
        document.body.innerHTML = '<div class="test"><div class="iuw-add-image-btn"></div></div>';

        const testElement = getBySelector('.test');
        
        expect(getAddButton(testElement)).toBeInTheDocument();
    });

    it('getAddButton must throw an error if no element with the correctly class was found', () => {
        document.body.innerHTML = '<div class="test"><div class="no-iuw-add-image-btn"></div></div>';

        const testElement = getBySelector('.test');
        
        expect(() => getAddButton(testElement)).toThrow();
    });

    it('getManagementInputs must return the elements with the valid ids', () => {
        document.body.innerHTML = getMockManagementForms({ prefix: 'test' });
        
        const management = getManagementInputs('test');

        expect(management.totalForms).toBeInTheDocument();
        expect(management.minNumForms).toBeInTheDocument();
        expect(management.maxNumForms).toBeInTheDocument();
        expect(management.initialForms).toBeInTheDocument();
    });

    it('getManagementInputs must throw an error if one was not found', () => {
        document.body.innerHTML = getMockManagementForms({ prefix: 'test', initial: false });
        expect(() => getManagementInputs('test')).toThrow();

        document.body.innerHTML = getMockManagementForms({ prefix: 'test', max: false });
        expect(() => getManagementInputs('test')).toThrow();

        document.body.innerHTML = getMockManagementForms({ prefix: 'test', min: false });
        expect(() => getManagementInputs('test')).toThrow();

        document.body.innerHTML = getMockManagementForms({ prefix: 'test', total: false });
        expect(() => getManagementInputs('test')).toThrow();
    });

    it('createTempFileInput must returns an input', () => {
        const element = createTempFileInput();
        
        expect(element).not.toBeNull();
        expect(element).not.toBeUndefined();
        expect(element.tagName.toLowerCase()).toEqual('input');
    });
});
