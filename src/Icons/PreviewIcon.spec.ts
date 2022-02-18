import PreviewIcon from './PreviewIcon';

describe('PreviewIcon', () => {
    test('PreviewIcon must be a string', () => {
        expect(typeof PreviewIcon).toBe('string');
    });

    test('PreviewIcon must contains an svg', () => {
        const div = document.createElement('div');
        div.innerHTML = PreviewIcon;
        
        expect(div.querySelectorAll('svg')).toHaveLength(1);
    });
});
