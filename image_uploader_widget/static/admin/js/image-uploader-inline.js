window.dragCounter = 0;
window.draggingEditor = null;

function updateEmptyState(root) {
  const items = root.querySelectorAll('.inline-related:not(.empty-form):not(.deleted)');
  root.classList.toggle('empty', items.length == 0);
}

function updateElementIndex(element, prefix, index) {
  const findRegex = new RegExp('(' + prefix + '-(\\d+|__prefix__))');
  const replacement = prefix + '-' + index;
  // replace at [for]
  const forAttr = element.getAttribute('for');
  if (forAttr) {
    element.setAttribute('for', forAttr.replace(findRegex, replacement));
  }
  // replace at [id]
  const idAttr = element.getAttribute('id');
  if (idAttr) {
    element.setAttribute('id', idAttr.replace(findRegex, replacement));
  }
  // replace at [name]
  const nameAttr = element.getAttribute('name');
  if (nameAttr) {
    element.setAttribute('name', nameAttr.replace(findRegex, replacement));
  }
}

function updateAllElementsIndexes(element, prefix, index) {
  updateElementIndex(element, prefix, index);
  const elements = element.querySelectorAll('*');
  for (const child of elements) {
    updateElementIndex(child, prefix, index);
  }
}

function getPrefix(root) {
  const inlineGroup = root.closest('.inline-group');
  return inlineGroup.getAttribute('data-prefix');
}

function updateOrderFields(root) {
  const inlineGroup = root.closest('.inline-group');
  const orderField = inlineGroup.getAttribute('data-order-field');
  if (!orderField) {
    return;
  }
  const template = root.querySelector('.inline-related.empty-form');

  const orderSelector = 'input[name$="' + orderField + '"]';
  Array
    .from(root.querySelectorAll('.inline-related:not(.empty-form):not(.deleted)'))
    .map(function(item){
      const orderField = item.querySelector(orderSelector);
      return {
        item: item,
        order: parseInt(orderField.value),
      };
    })
    .sort(function(a, b) {
      return a.order - b.order;
    })
    .map(function(item, index) {
      return {
        item: item.item,
        order: index + 1,
      }
    })
    .forEach(function(item){
      const orderField = item.item.querySelector(orderSelector);
      orderField.value = item.order;

      const parent = item.item.parentElement;
      parent.removeChild(item.item);
      parent.appendChild(item.item, template);
    });
}

function updateAllIndexes(root) {
  const prefix = getPrefix(root);
  const elements = root.querySelectorAll('.inline-related:not(.empty-form)');

  let index = 0;
  for (const item of elements) {
    updateAllElementsIndexes(item, prefix, index);
    index += 1;
  }

  const totalForms = document.querySelector('#id_' + prefix + '-TOTAL_FORMS');
  const maxNumForms = document.querySelector('#id_' + prefix + '-MAX_NUM_FORMS');
  const maxCount = maxNumForms.value === '' ? Number.MAX_SAFE_INTEGER : parseInt(maxNumForms.value, 10)

  totalForms.value = index.toString();
  root.querySelector('.iuw-add-image-btn').classList.toggle('visible-by-number', maxCount - elements.length > 0);

  updateEmptyState(root);
  updateOrderFields(root);
}

function getNext(root, prefix) {
  let next = 1;
  while (!!root.querySelector('#' + prefix + '-' + next)) {
    next = next + 1;
  }
  return next;
}

function cloneFromEmptyTemplate(root) {
  const template = root.querySelector('.inline-related.empty-form');
  if (!template) {
      return null;
  }

  const prefix = getPrefix(root);
  const row = template.cloneNode(true);
  row.classList.remove('empty-form', 'last-related');
  row.setAttribute('data-candelete', 'true');
  row.id = prefix + '-' + getNext(root, prefix);

  template.parentElement.appendChild(row);

  const inlineGroup = root.closest('.inline-group');
  const orderField = inlineGroup.getAttribute('data-order-field');
  if (!orderField) {
    return row;
  }
  const orderSelector = 'input[name$="' + orderField + '"]';
  const inputs = inlineGroup.querySelectorAll(orderSelector)
  let order = 1;
  for (const input of inputs) {
    if (parseInt(input.value, 10) >= order) {
      order = parseInt(input.value, 10) + 1;
    }
  }
  row.querySelector(orderSelector).value = order;

  return row;
}

function handleAddNewImage(root, tempFileInput, inputFile = null) {
  file = inputFile ||(tempFileInput.files || [null])[0];
  if (!file) {
      return;
  }
  const row = cloneFromEmptyTemplate(root);
  const img = document.createElement('img');
  img.src = URL.createObjectURL(file);
  row.appendChild(img);
  const rowFileInput = row.querySelector('input[type=file]');
  const parent = rowFileInput.parentElement;

  if (!tempFileInput) {
    const dataTransferList = new DataTransfer();
    dataTransferList.items.add(file);
    rowFileInput.files = dataTransferList.files;

    updateAllIndexes(root);
    return;
  }

  const className = rowFileInput.className;
  const name = rowFileInput.getAttribute('name');
  parent.removeChild(rowFileInput);

  clonedInput = tempFileInput.cloneNode(true)
  clonedInput.className = className;
  clonedInput.setAttribute('name', name || '');

  //
  // TODO: Safari not clone files inside the input.
  //
  //
  const dataTransferList = new DataTransfer();
  dataTransferList.items.add(file);
  clonedInput.files = dataTransferList.files;

  tempFileInput.value = null

  parent.appendChild(clonedInput);

  updateAllIndexes(root);
}

document.addEventListener('change', function(evt) {
  const root = evt.target.closest('.iuw-inline-root');
  if (!root) { return; }

  const inlineRelated = evt.target.closest('.inline-related:not(.empty-form),.temp_file');
  if (!inlineRelated) { return; }

  const fileInput = evt.target.closest('input[type="file"]')
  if (!fileInput?.files.length) { return; }

  if (fileInput.classList.contains('temp_file')) {
    return handleAddNewImage(root, fileInput);
  }

  const [file] = fileInput.files;
  const imgTag = inlineRelated.querySelector('img');
  imgTag.src = URL.createObjectURL(file);
});

function handlePreviewImage(previewItem) {
  let image = previewItem.querySelector('img');
  if (!image) {
      return;
  }
  image = image.cloneNode(true);
  IUWPreviewModal.createPreviewModal(image);
  IUWPreviewModal.openPreviewModal();
}

function handleRemoveImage(previewItem) {
  const root = previewItem.closest('.iuw-inline-root');

  if (previewItem.classList.contains('has_original')) {
    previewItem.classList.add('deleted');
    const checkboxInput = previewItem.querySelector('input[type=checkbox]');
    checkboxInput.checked = true;
  } else {
    previewItem.parentElement.removeChild(previewItem);
  }

  updateAllIndexes(root);
}

document.addEventListener('click', function(evt) {
  const target = evt.target;
  const root = target.closest('.iuw-inline-root');
  if (!root) {
    return;
  }

  const emptyMarker = target.closest('.iuw-empty');
  if (emptyMarker) {
    return root.querySelector('.temp_file').click();
  }

  const deleteButton = target.closest('.iuw-delete-icon');
  if (deleteButton) {
    return handleRemoveImage(target.closest('.inline-related'));
  }

  if (target.closest('.iuw-add-image-btn')) {
    root.querySelector('.temp_file').click();
    return;
  }

  if (target.closest('.iuw-preview-icon')) {
    return handlePreviewImage(target.closest('.inline-related'));
  }

  const inlineRelated = target.closest('.inline-related');
  if (inlineRelated) {
    const fileInput = inlineRelated.querySelector('input[type="file"]');
    fileInput.click();
  }
});

document.addEventListener('dragenter', function(evt) {
  const root = evt.target.closest('.iuw-inline-root');
  if (!root) { return; }
  if (root.classList.contains('dragging')) { return; }

  window.dragCounter = window.dragCounter + 1;
  window.draggingEditor = root;
  root.classList.add('drop-zone');
});

document.addEventListener('dragover', function(evt) {
  const root = evt.target.closest('.iuw-inline-root');
  if (!root) { return; }

  evt.preventDefault();
});

document.addEventListener('dragleave', function(evt) {
  window.dragCounter = window.dragCounter - 1;
  if (window.dragCounter > 0) {
    return;
  }
  if (!window.draggingEditor) {
    return;
  }
  if (evt.relatedTarget && evt.relatedTarget.closest('.iuw-inline-root') === window.draggingEditor) {
    return;
  }

  const root = window.draggingEditor;
  root.classList.remove('drop-zone');
});

document.addEventListener('dragend', function(evt) {
  window.dragCounter = window.dragCounter - 1;
  if (window.dragCounter > 0) {
    return;
  }
  if (!window.draggingEditor) {
    return;
  }
  if (evt.relatedTarget && evt.relatedTarget.closest('.iuw-inline-root') === window.draggingEditor) {
      return;
  }

  const root = window.draggingEditor;
  if (root.classList.contains('dragging')) { return; }

  root.remove('drop-zone');
});

document.addEventListener('drop', function(evt) {
  const root = window.draggingEditor;
  if (!root) { return; }

  if (root.classList.contains('dragging')) { return; }

  evt.preventDefault();
  window.draggingEditor = null;
  root.classList.remove('drop-zone');

  if (!evt.dataTransfer.files.length) {
    return;
  }
  for (const file of evt.dataTransfer.files) {
    handleAddNewImage(root, null, file);
  }
});

function handleFinishOrdering (previewsContainer) {
  const root = previewsContainer.closest('.iuw-inline-root');
  root.classList.remove('dragging');
  const inlineGroup = previewsContainer.closest('.inline-group');
  const orderField = inlineGroup.getAttribute('data-order-field');
  if (!orderField) {
    return;
  }
  const orderSelector = 'input[name$="' + orderField + '"]';

  const inlines = previewsContainer.querySelectorAll('.inline-related');
  let order = 1;
  for (const inline of inlines) {
    const orderInput = inline.querySelector(orderSelector)
    orderInput.value = order;
  }

  updateAllIndexes(root);
}

function handleBeginOrdering(previewsContainer) {
  const root = previewsContainer.closest('.iuw-inline-root');
  root.classList.add('dragging');
}

function initialize(doc) {
  if (!doc) {
    doc = document;
  }
  const items = Array.from(doc.querySelectorAll('.iuw-inline-root .previews'));
  for (const item of items) {
    const root = item.closest('.iuw-inline-root');
    const inlineGroup = root.closest('.inline-group');
    updateAllIndexes(root);

    if (!inlineGroup.getAttribute('data-order-field')) {
      continue;
    }

    new Sortable(item, {
      onStart: function(evt) {
        handleBeginOrdering(evt.to);
      },
      onEnd: function(evt) {
        handleFinishOrdering(evt.to);
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', function() {
  initialize();
});
document.addEventListener('htmx:afterSwap', function(ev) {
  initialize(ev.target);
})
