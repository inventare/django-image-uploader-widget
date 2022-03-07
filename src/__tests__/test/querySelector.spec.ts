import { getBySelector } from '../../test/querySelector';

describe('querySelector', () => {
    it('getBySelector must return the element if it is found', () => {
        document.body.innerHTML = '<a class="aaa"></a>';

        expect(getBySelector('.aaa')).toBeInTheDocument();
    });

    it('getBySelector must thrown an error if the element is not found', () => {
        document.body.innerHTML = '<a class="aaa"></a>';

        expect(() => getBySelector('.bbb')).toThrow();
    });
});
