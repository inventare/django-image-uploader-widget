import DeleteIcon from '../../Icons/DeleteIcon';

describe('DeleteIcon', () => {
    it('DeleteIcon must be a string', () => {
        expect(typeof DeleteIcon).toBe('string');
    });

    it('DeleteIcon must contains an svg', () => {
        const div = document.createElement('div');
        div.innerHTML = DeleteIcon;
        
        expect(div.querySelectorAll('svg')).toHaveLength(1);
    });
});
