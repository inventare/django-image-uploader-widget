import { previewClasses } from './constants'
import { DeleteIcon, PreviewIcon } from '../icons';

const renderDeleteButton = (canDelete: boolean) => {
  if (!canDelete) {
    return '';
  }
  return `<span class="${previewClasses.deleteIcon}">${DeleteIcon}</span>`;
}

const renderPreviewButton = (canDelete: boolean, canPreview: boolean) => {
  if (!canPreview) {
    return '';
  }
  const className = canDelete
    ? previewClasses.previewIcon
    : `${previewClasses.previewIcon} ${previewClasses.onlyPreview}`;
  return `<span class="${className}">${PreviewIcon}</span>`
};

export const renderPreview = (url: string, canDelete: boolean, canPreview: boolean) => {
  const deleteButton = renderDeleteButton(canDelete);
  const previewButton = renderPreviewButton(canDelete, canPreview);
  
  const div = document.createElement('div');
  div.className = previewClasses.preview;
  div.innerHTML = '<img src="' + url + '" />' + deleteButton + previewButton;
  return div;
}
