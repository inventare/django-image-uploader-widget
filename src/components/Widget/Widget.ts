import { widgetClasses } from './constants';
import { renderPreview } from '../Preview';
import { PreviewModal } from '../PreviewModal';

class WidgetInputNotFoundError extends Error {
  constructor(input: string) {
    super(`The widget ${input} input was not found.`);
  }
}

export class Widget {
  private static instances: Widget[] = [];

  private static pushInstance(instance: Widget) {
    Widget.instances.push(instance);
  }

  private static getInstance(element: HTMLElement) {
    const root = element.closest(`.${widgetClasses.root}`);
    if (!root || !root.getAttribute('data-widget')) {
      return null;
    }
    const id = root.getAttribute('data-widget');
    const items = Widget.instances.filter((item) => item.id === id);
    if (!items.length) {
      return null;
    }
    return items[0];
  }

  private static handleEmptyMarkerClick(e: Event) {
    const widget = Widget.getInstance(e.target as HTMLElement);
    if (!widget) {
        return;
    }
    widget.fileInput.click();
  }

  private static handleFileInputChange(e: Event) {
    const widget = Widget.getInstance(e.target as HTMLElement);
    if (!widget) {
      return;
    }
    if (!widget.fileInput.files?.length) {
      return;
    }
    widget.file = widget.fileInput.files[0];
    widget.render();
  }

  private static handleImagePreviewClick(e: Event) {
    if (!e || !e.target) {
        return;
    }
    const targetElement = e.target as HTMLElement;
    const widget = Widget.getInstance(targetElement);
    if (!widget) {
      return;
    }

    if (targetElement.closest(`.${widgetClasses.deleteIcon}`)) {
        const element = targetElement.closest<HTMLElement>(`.${widgetClasses.preview}`);
        if (!element) {
          return;
        }
        return widget.removeImage(element);
    }
    if (targetElement.closest(`.${widgetClasses.previewIcon}`)) {
        const element = targetElement.closest<HTMLElement>(`.${widgetClasses.preview}`);
        if (!element) {
          return;
        }
        return widget.previewImage(element);
    }
    widget?.fileInput.click();
  }

  private element: HTMLElement;
  private id: string = '';
  private file: File | null = null;
  private raw: string | null = null;

  private get fileInput() {
    const input =  this.element.querySelector<HTMLInputElement>('input[type=file]');
    if (!input) {
      throw new WidgetInputNotFoundError('file');
    }
    return input;
  }

  private get checkboxInput() {
    return this.element.querySelector<HTMLInputElement>('input[type=checkbox]');
  }

  private get emptyMarker() {
    return this.element.querySelector<HTMLElement>('.iuw-empty');
  }

  private get canDelete() {
    return this.element.getAttribute('data-candelete') === 'true';
  }

  private get canPreview() {
    return this.element.getAttribute('data-canpreview') === 'true';
  }

  private get previews() {
    return this.element.querySelectorAll<HTMLElement>(`.${widgetClasses.preview}`);
  }

  constructor(element: HTMLElement) {
    this.element = element;
    
    this.buildWidget();
    this.addEvents();
    Widget.pushInstance(this);
  }

  private addEvents() {
    this.fileInput.addEventListener('change', Widget.handleFileInputChange);
    
    if (!this.emptyMarker) {
      return;
    }
    this.emptyMarker.addEventListener('click', Widget.handleEmptyMarkerClick);
  }

  private buildWidget() {
    this.id = this.fileInput.id;
    this.element.setAttribute('data-widget', this.id);
    
    this.raw = this.element.getAttribute('data-raw');

    this.render();
  }

  private updateStates() {
    if (!this.file && !this.raw) {
      this.element.classList.add(widgetClasses.empty);
      if (!this.checkboxInput) {
        return;
      }
      this.checkboxInput.checked = true;
      return;
    }
    this.element.classList.remove(widgetClasses.empty);
    if (!this.checkboxInput) {
      return;
    }
    this.checkboxInput.checked = false;
  }

  render() {
    this.updateStates();

    this.previews.forEach((item) => item.parentElement?.removeChild(item));
    
    const url = this.file
      ? URL.createObjectURL(this.file)
      : this.raw;

    if (!url) {
      return;
    }

    this.element.appendChild(renderPreview(url, this.canDelete, this.canPreview));
    this.previews.forEach((item) => item.addEventListener('click', Widget.handleImagePreviewClick))
  }

  removeImage(imageElement: HTMLElement) {
    imageElement.parentElement?.removeChild(imageElement);
    if (this.checkboxInput) {
      this.checkboxInput.checked = true;
    }

    this.fileInput.value = '';
    this.file = null;
    this.raw = null;
    this.render();
  };

  previewImage(imageElement: HTMLElement) {
    let image = imageElement.querySelector<HTMLImageElement>('img');
    if (!image) {
      return;
    }
    image = image.cloneNode(true) as HTMLImageElement;
    PreviewModal.getInstance().show(image);
  }
}
