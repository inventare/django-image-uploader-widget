import { Widget } from './components/Widget/Widget';
import { widgetClasses } from './components/Widget/constants';

(window as any).initializeWidgets = (element: HTMLElement) => {
  Array
    .from(element.querySelectorAll<HTMLElement>(`.${widgetClasses.root}`))
    .map((item) => new Widget(item));
}

document.addEventListener('DOMContentLoaded', () => {
  (window as any).initializeWidgets(document);

  if (window && (window as any).django && (window as any).django.jQuery) {
    const $ = (window as any).django.jQuery;
    $(document).on('formset:added', (e, rows) => {
      if (!rows || !rows.length) {
          rows = [e.target]
      }
      if (!rows || !rows.length) {
          return;
      }
      (window as any).initializeWidgets(rows[0]);
    });
  };
});
