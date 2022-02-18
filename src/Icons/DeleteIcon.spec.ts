import DeleteIcon from './DeleteIcon';

describe('DeleteIcon', () => {
    test('DeleteIcon must be a string', () => {
        expect(typeof DeleteIcon).toBe('string');
    });

    test('DeleteIcon must contains an svg', () => {
        const div = document.createElement('div');
        div.innerHTML = DeleteIcon;
        
        expect(div.querySelectorAll('svg')).toHaveLength(1);
    });
});
