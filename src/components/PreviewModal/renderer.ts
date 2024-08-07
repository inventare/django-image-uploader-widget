import { CloseIcon } from '../icons';
import { previewModalClasses, previewModalId } from './constants';

export const renderCloseButton = (previewModal: HTMLElement) => {
  const cl = previewModalClasses.closeButton;
  const closeButtonHtml = `<span class="${cl}">${CloseIcon}</span>`;
  previewModal.innerHTML = closeButtonHtml;
  return previewModal.querySelector(`span.${cl}`);
};

export const renderModal = (image: HTMLImageElement) => {
  const modal = document.createElement('div');
  modal.id = previewModalId;
  modal.className = previewModalClasses.modal;

  const preview = document.createElement('div');
  preview.className = previewModalClasses.preview;
  image.className = previewModalClasses.image;
  renderCloseButton(preview);
  preview.appendChild(image);
  
  modal.appendChild(preview);

  return modal;
}
