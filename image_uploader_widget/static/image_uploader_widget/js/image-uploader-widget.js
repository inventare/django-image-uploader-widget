document.addEventListener('DOMContentLoaded', function(){
  function changeImagePreview(root, input) {
    if (!input) {
      input = root.querySelector('input[type=file]');
    }

    const [file] = input.files;
    const url = URL.createObjectURL(file);
    root.classList.remove('empty');

    const checkbox = root.querySelector('input[type="checkbox"]');
    if (checkbox) {
      checkbox.checked = false;
    }

    const previewImage = root.querySelector('.iuw-image-preview img');
    if (!previewImage) {
      const previewRoot = root.querySelector('.iuw-image-preview');

      const img = document.createElement('img');
      img.src = url;
      previewRoot.appendChild(img);
      return;
    }
    previewImage.src = url;
  }

  document.addEventListener('change', function(evt) {
    const { target } = evt;
    const root = target.closest('.iuw-root');
    if (!root) { return; }

    const input = root.querySelector('input[type="file"]');
    if (!input.files.length) { return; }

    changeImagePreview(root, input);
  });

  function handleEmptyMarkerClick(emptyMarker) {
    const root = emptyMarker.closest('.iuw-root');
    if (!root) { return; }

    root.querySelector('input[type="file"]').click();
  }

  function handlePreviewImage(previewItem) {
    let image = previewItem.querySelector('img');
    if (!image) {
        return;
    }
    image = image.cloneNode(true);
    IUWPreviewModal.createPreviewModal(image);
    IUWPreviewModal.openPreviewModal();
  }

  function handleRemoveImage(root) {
    const checkbox = root.querySelector('input[type="checkbox"]');
    if (checkbox) {
      checkbox.checked = true;
    }

    const fileInput = root.querySelector('input[type="file"]');
    fileInput.value = '';
    root.classList.add('empty');
  }

  document.addEventListener('click', function(evt) {
    const { target } = evt;
    const emptyMarker = target.closest('.iuw-empty');
    if (emptyMarker) {
      return handleEmptyMarkerClick(emptyMarker);
    }

    const deleteButton = target.closest('.iuw-delete-icon');
    if (deleteButton) {
      return handleRemoveImage(target.closest('.iuw-root'));
    }

    const previewButton = target.closest('.iuw-preview-icon');
    if (previewButton) {
      return handlePreviewImage(target.closest('.iuw-image-preview'));
    }

    const previewItem = target.closest('.iuw-image-preview');
    if (previewItem) {
      const root = target.closest('.iuw-root');
      const fileInput = root.querySelector('input[type="file"]');
      fileInput.click();
    }
  });

  document.addEventListener('dragenter', function(evt) {
    const root = evt.target.closest('.iuw-root');
    if (!root) { return; }

    window.draggingWidget = root;
    root.classList.add('drop-zone');
  });

  document.addEventListener('dragover', function(evt) {
    const root = evt.target.closest('.iuw-root');
    if (!root) { return; }

    evt.preventDefault();
  });

  document.addEventListener('dragleave', function(evt) {
    if (evt.relatedTarget && evt.relatedTarget.closest('.iuw-root') === window.draggingWidget) {
      return;
    }
    const root = evt.target.closest('.iuw-root');
    if (!root) { return; }

    root.classList.remove('drop-zone');
    window.draggingWidget = null;
  });

  document.addEventListener('dragend', function(evt) {
    const root = evt.target.closest('.iuw-root');
    if (!root) { return; }

    root.classList.remove('drop-zone');
  });

  document.addEventListener('drop', function(evt) {
    const root = window.draggingWidget;
    if (!root) { return; }

    evt.preventDefault();

    window.draggingWidget = null;
    root.classList.remove('drop-zone');
    if (!evt.dataTransfer.files.length) {
        return;
    }

    const fileInput = root.querySelector('input[type="file"]');

    fileInput.files = evt.dataTransfer.files;
    changeImagePreview(root, fileInput);
  });
});
