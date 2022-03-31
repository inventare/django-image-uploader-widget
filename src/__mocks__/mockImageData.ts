
export const mockImageData = Buffer.from(
    'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TpSIVUQuKOGSogmBBVMRRq1CECqFWaNXB5NIvaNKQpLg4Cq4FBz8Wqw4uzro6uAqC4AeIm5uToouU+L+k0CLWg+N+vLv3uHsHCNUi06y2cUDTbTMRi4qp9KoYeEUQ/ejFKHpkZhlzkhRHy/F1Dx9f7yI8q/W5P0eXmrEY4BOJZ5lh2sQbxNObtsF5nzjE8rJKfE48ZtIFiR+5rnj8xjnnssAzQ2YyMU8cIhZzTaw0McubGvEUcVjVdMoXUh6rnLc4a8Uyq9+TvzCY0VeWuU5zCDEsYgkSRCgoo4AibERo1UmxkKD9aAv/oOuXyKWQqwBGjgWUoEF2/eB/8LtbKzs54SUFo0D7i+N8DAOBXaBWcZzvY8epnQD+Z+BKb/hLVWDmk/RKQwsfAd3bwMV1Q1P2gMsdYODJkE3Zlfw0hWwWeD+jb0oDfbdA55rXW30fpw9AkrqK3wAHh8BIjrLXW7y7o7m3f8/U+/sBgl1yrZQ5tlQAAAAJcEhZcwAALiMAAC4jAXilP3YAAAAHdElNRQflDBcSKSjsMuK5AAAAGXRFWHRDb21tZW50AENyZWF0ZWQgd2l0aCBHSU1QV4EOFwAAABpJREFUKM9jZNj7j4EUwMRAIhjVMKph6GgAAHyXAdui3YKhAAAAAElFTkSuQmCC',
    'base64'
);

export const mockObjectURL = 'test::/file.png';

export const mockFileName = 'file.png';

export const getMockFile = () => {
    global.URL.createObjectURL = jest.fn(() => mockObjectURL);
    const file = new File([mockImageData], mockFileName, {type : 'image/png'});
    return file;
}
