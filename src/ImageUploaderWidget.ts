import { ImageUploaderWidget } from './Widget';

declare global {
    interface Window {
        django: {
            jQuery: any;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    Array
        .from(document.querySelectorAll<HTMLElement>('.iuw-root'))
        .map((element) => new ImageUploaderWidget(element));

    if (window && window.django && window.django.jQuery) {
        const $ = window.django.jQuery;
        
        $(document).on('formset:added', (e: Event, row: HTMLElement[]) => {
            if (!row || !row.length) {
                row = [e.target as HTMLElement]
            }
            if (!row || !row.length) {
                return;
            }
            Array
                .from(row[0].querySelectorAll<HTMLElement>('.iuw-root'))
                .map((element) => new ImageUploaderWidget(element));
        });
    }
});
