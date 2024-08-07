import { previewModalClasses, previewModalId } from './constants';
import { renderModal } from './renderer';

export class PreviewModal {
  private static instance: PreviewModal;

  public static getInstance(): PreviewModal {
    if (!PreviewModal.instance) {
      PreviewModal.instance = new PreviewModal();
    }
    return PreviewModal.instance;
  }

  private static handleModalClick(ev: MouseEvent) {
    if (!ev || !ev.target) {
      return;
    }
    const element = ev.target as HTMLElement;
    if (element.closest(`.${previewModalClasses.image}`)) {
      return;
    }
    PreviewModal.getInstance().close();
  }

  private constructor() {}

  private createModalElement(image: HTMLImageElement) {
    const modal = renderModal(image);
    modal.addEventListener('click', PreviewModal.handleModalClick);

    document.body.appendChild(modal);
    return modal;
  }

  private removeExistingModalElement() {
    const modal = document.getElementById(previewModalId);
    if (!modal) {
      return;
    }
    modal.parentElement?.removeChild(modal);
  }

  close() {
    document.body.style.overflow = 'auto';
    const modal = document.getElementById(previewModalId);
    if (!modal) {
      return;
    }

    modal.classList.remove(previewModalClasses.visible);
    modal.classList.add(previewModalClasses.hide);
    setTimeout(() => {
      this.removeExistingModalElement();
    }, 300);
  }

  show(image: HTMLImageElement) {
    this.removeExistingModalElement();
    const modal = this.createModalElement(image);

    setTimeout(() => {
      modal.classList.add(previewModalClasses.visible);
      modal.classList.remove(previewModalClasses.hide);

      document.body.style.overflow = 'hidden';
    }, 50);
  }
};
