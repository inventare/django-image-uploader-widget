import { ImageUploaderInline } from './Inline/Editor';

document.addEventListener('DOMContentLoaded', () => {
    Array
        .from(document.querySelectorAll('.iuw-inline-root'))
        .map((element) => new ImageUploaderInline(element as HTMLElement));
});
