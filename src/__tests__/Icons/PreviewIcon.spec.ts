import PreviewIcon from '../../Icons/PreviewIcon';

describe('PreviewIcon', () => {
    it('PreviewIcon must be a string', () => {
        expect(typeof PreviewIcon).toBe('string');
    });

    it('PreviewIcon must contains an svg', () => {
        const div = document.createElement('div');
        div.innerHTML = PreviewIcon;
        
        expect(div.querySelectorAll('svg')).toHaveLength(1);
    });
});
