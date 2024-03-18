document.addEventListener('DOMContentLoaded', function() {
    let DRAGGING_EDITOR = null;
    window.uploaderEditors = {};
    const DELETE_ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path></svg>';
    const PREVIEW_ICON = '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-zoom-in" viewBox="0 0 16 16" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"></path><path xmlns="http://www.w3.org/2000/svg" d="M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z"></path><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z"></path></svg>';

    function getEditor(element) {
        const root = element.closest('.iuw-inline-root');
        if (!root) {
            return null;
        }
        const id = root.getAttribute('data-editor');
        if (!id) {
            return null;
        }
        if (!Object.prototype.hasOwnProperty.call(window.uploaderEditors, id)) {
            return null;
        }
        return window.uploaderEditors[id];
    }

    function getManagementInputs(prefix) {
        const totalForms = document.querySelector('#id_' + prefix + '-TOTAL_FORMS');
        const initialForms = document.querySelector('#id_' + prefix + '-INITIAL_FORMS');
        const minNumForms = document.querySelector('#id_' + prefix + '-MIN_NUM_FORMS');
        const maxNumForms = document.querySelector('#id_' + prefix + '-MAX_NUM_FORMS');
        return {
            totalForms: totalForms,
            initialForms: initialForms,
            minNumForms: minNumForms,
            maxNumForms: maxNumForms,
        };
    }

    function getFromEmptyTemplate(editor) {
        const template = editor.element.querySelector('.inline-related.empty-form');
        if (!template) {
            return null;
        }

        const row = template.cloneNode(true);
        row.classList.remove('empty-form');
        row.classList.remove('last-related');
        row.setAttribute('data-candelete', 'true');
        row.id = editor.inlineFormset.options.prefix + '-' + editor.next;

        template.parentElement.insertBefore(row, editor.addImageButton);

        return row;
    }

    function getAndUpdateDataRaw(element) {
        if (element.classList.contains('empty-form')) {
            return null;
        }
        const rawImage = element.querySelector('p.file-upload a');
        if (!rawImage) {
            return null;
        }
        const hrefAttr = rawImage.getAttribute('href');
        if (!hrefAttr) {
            return null;
        }
        element.setAttribute('data-raw', hrefAttr);
        return hrefAttr;
    }

    function updatePreviewState(editor, element, url) {
        if (!url) {
            const inputOrder = editor.orderField ? ' , .field-' + editor.orderField + ' input' : '';
            const inputs = element.querySelectorAll('input[type=hidden], input[type=checkbox], input[type=file]' + inputOrder);
            for (const item of inputs) {
                item.parentElement.removeChild(item);
            }
            url = getAndUpdateDataRaw(element);
            element.innerHTML = '';
            for (const item of inputs) {
                element.appendChild(item)
            }
        }

        if (!url) {
            return;
        }

        let deleteIcon = null;
        const related = element.closest('.inline-related');

        related.addEventListener('click', handleItemPreviewClick);
        if (editor.orderField) {
            related.addEventListener('dragstart', handleItemPreviewDragStart);
            related.addEventListener('dragend', handleItemPreviewDragEnd);
        }
        
        related.querySelector('input[type=file]').addEventListener('change', handleItemPreviewFileChange);
        
        if (related.getAttribute('data-candelete') === 'true') {
            deleteIcon = document.createElement('span');
            deleteIcon.classList.add('iuw-delete-icon');
            deleteIcon.innerHTML = DELETE_ICON;
        }

        if (editor.canPreview) {
            const span = document.createElement('span');
            span.classList.add('iuw-preview-icon');
            if (related.getAttribute('data-candelete') !== 'true') {
                span.classList.add('iuw-only-preview');
            }
            span.innerHTML = PREVIEW_ICON;
            element.appendChild(span);
        }

        const img = document.createElement('img');
        img.src = url;
        element.appendChild(img);
        
        if (deleteIcon) {
            element.appendChild(deleteIcon);
        }
    }

    function handleItemPreviewDragStart(e) {
        this.classList.add("dragging");
        const editor = getEditor(this);
        const widget = editor.element;
        widget.setAttribute('dragging-element', this.id);
    }

    function handleItemPreviewDragEnd(e) {
        this.classList.remove("dragging");
        const editor = getEditor(this);
        const widget = editor.element;
        widget.removeAttribute('dragging-element');
    }

    function handleItemPreviewFileChange(e) {
        if (!e || !e.target || e.target.tagName !== 'INPUT') {
            return;
        }

        const fileInput = e.target;
        const files = fileInput.files;
        if (!files.length) {
            return;
        }

        const imgTag = fileInput.closest('.inline-related').querySelector('img');
        if (imgTag) {
            imgTag.src = URL.createObjectURL(files[0]);
        }
    }

    function handleItemPreviewRemove(editor, element) {
        if (element.getAttribute('data-raw')) {
            element.classList.add('deleted');
            const checkboxInput = element.querySelector('input[type=checkbox]');
            checkboxInput.checked = true;
        } else {
            element.parentElement.removeChild(element);
        }
        
        updateEmptyState(editor);
        updateAllIndexes(editor);
    }

    function handleItemPreviewClick(e) {
        if (!e || !e.target) {
            return;
        }

        const target = e.target;
        const item = target.closest('.inline-related');
        if (target.closest('.iuw-delete-icon')) {
            const editor = getEditor(target);
            handleItemPreviewRemove(editor, item);
            return;
        }

        if (target.closest('.iuw-preview-icon')) {
            let image = item.querySelector('img');
            if (image) {
                image = image.cloneNode(true);
                IUWPreviewModal.createPreviewModal(image);
                IUWPreviewModal.openPreviewModal();
                return;
            }
            return;
        }

        const fileInput = item.querySelector('input[type=file]');
        if (e.target === fileInput) {
            return;
        }
        fileInput.click();
    }

    function getNextOrder(editor) {
        const inputOrdersSelector = '.inline-related:not(.empty-form) input[name$="' + editor.orderField + '"]';
        const inputs = editor.element.querySelectorAll(inputOrdersSelector)
        if (!inputs.length) {
            return 1;
        }

        let currentOrder = 1;
        for (const input of inputs) {
            const order = parseInt(input.value);
            if ((order + 1) > currentOrder) {
                currentOrder = order + 1;
            }
        }

        return currentOrder;
    }

    function handleAddFile(editor, file) {
        let newOrder = 1;
        if (editor.orderField) {
            newOrder = getNextOrder(editor);
        }

        const row = getFromEmptyTemplate(editor);

        if (editor.orderField) {
            const orderField = row.querySelector('input[name$="' + editor.orderField + '"]');
            orderField.value = newOrder;
        }
        
        if (!!file) {
            const rowFileInput = row.querySelector('input[type=file]');
            
            const dataTransferList = new DataTransfer();
            dataTransferList.items.add(file);

            rowFileInput.files = dataTransferList.files;
        } else {
            if (!editor.tempFileInput) {
                return;
            }
            file = (editor.tempFileInput.files || [null])[0];
            if (!file) {
                return;
            }
            const rowFileInput = row.querySelector('input[type=file]');
            const parent = rowFileInput.parentElement;

            const className = rowFileInput.className;
            const name = rowFileInput.getAttribute('name');
            parent.removeChild(rowFileInput);

            clonedInput = editor.tempFileInput.cloneNode(true)
            clonedInput.className = className;
            clonedInput.setAttribute('name', name || '');

            //
            // TODO: Safari not clone files inside the input.
            //
            //
            const dataTransferList = new DataTransfer();
            dataTransferList.items.add(file);
            clonedInput.files = dataTransferList.files;

            editor.tempFileInput.value = null

            parent.appendChild(clonedInput);
        }

        updatePreviewState(editor, row, URL.createObjectURL(file));
        updateEmptyState(editor);
        updateAllIndexes(editor);
    }

    function handleDragEnter(e) {
        const editor = getEditor(e.target);
        if (!editor) {
            return;
        }
        DRAGGING_EDITOR = editor;

        if (editor.element.getAttribute('dragging-element')) {
            return;
        }
        editor.element.classList.add('drop-zone');
    }

    function handleDragOver(e) {
        if (!e) {
            return;
        }
        e.preventDefault();
    }
    
    function handleDragLeave(e) {
        if (!DRAGGING_EDITOR) {
            return;
        }
        if (e.relatedTarget && e.relatedTarget.closest('.iuw-inline-root') === DRAGGING_EDITOR.element) {
            return;
        }
        DRAGGING_EDITOR.element.classList.remove('drop-zone');
        DRAGGING_EDITOR = null;
    }

    function getElementNewPosition(editor, dragging, x, y) {
        const items = editor.element.querySelectorAll('.inline-related:not(.empty-form):not(.deleted)');
        let index = 0;
        for (const item of items) {
            const rc = item.getBoundingClientRect();
            if (x > rc.left && x < rc.right && y > rc.top && y <= rc.bottom) {
                if (item === dragging) {
                    // not dragged
                    return null;
                }

                const isRight = x > (rc.left + rc.width / 2);
                if (isRight) {
                    return index;
                }
                return index - 1;
            }
            index = index + 1;
        }
        return -1;
    }

    function reorderItems(editor, dragging, newPosition) {
        const orderSelector = 'input[name$="' + editor.orderField + '"]';
        const items = Array
            .from(editor.element.querySelectorAll('.inline-related:not(.empty-form):not(.deleted)'))
            .map(function(item){
                const orderField = item.querySelector(orderSelector);

                return {
                    item: item,
                    order: parseInt(orderField.value),
                };
            })
            .sort(function(a, b) {
                return a.order - b.order;
            });
        
        const prevItems = items.filter(function (item, index){
            if (item.item === dragging) {
                return false;
            }

            return index <= newPosition;
        });
        const postItems = items.filter(function (item, index){
            if (item.item === dragging) {
                return false;
            }
            return index > newPosition;
        });

        [...prevItems, { item: dragging, order: 0 }, ...postItems]
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
                parent.insertBefore(item.item, editor.addImageButton);
            });

        dragging.classList.remove("dragging");
        editor.element.removeAttribute('dragging-element');
    }

    function handleDrop(e) {
        e.preventDefault();
        
        const editor = DRAGGING_EDITOR;
        if (!editor) {
            return;
        }
        DRAGGING_EDITOR = null;
        editor.element.classList.remove('drop-zone');

        if (editor.element.getAttribute('dragging-element')) {
            const draggingElement = document.getElementById(editor.element.getAttribute('dragging-element'));
            editor.element.removeAttribute('dragging-element');
            const x = e.pageX;
            const y = e.pageY;
            const newIndex = getElementNewPosition(editor, draggingElement, x, y);
            reorderItems(editor, draggingElement, newIndex);
            return;
        }

        if (!e.dataTransfer.files.length) {
            return;
        }
        for (const file of e.dataTransfer.files) {
            handleAddFile(editor, file);
        }
    }

    function handleTempFileInputChange(e) {
        const editor = getEditor(e.target);
        
        const filesList = editor.tempFileInput.files;
        if (!filesList || filesList.length <= 0) {
            return;
        }
        handleAddFile(editor);
    }

    function handleAddImageClick(e) {
        const editor = getEditor(e.target);

        if(!editor.tempFileInput) {
            return;
        }
        editor.tempFileInput.click();
    }

    function updateEmptyState(editor) {
        const items = editor.element.querySelectorAll('.inline-related:not(.empty-form):not(.deleted)');
        editor.element.classList.toggle('empty', items.length == 0);
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

    function updateAllIndexes(editor) {
        const prefix = editor.inlineFormset.options.prefix;
        const elements = editor.element.querySelectorAll('.inline-related:not(.empty-form)');
        
        let index = 0;
        for (const item of elements) {
            updateAllElementsIndexes(item, prefix, index);
            index += 1;
        }
        
        editor.next = elements.length;
        editor.management.totalForms.value = editor.next.toString();
        editor.addImageButton.classList.toggle('visible-by-number', editor.maxCount - editor.next > 0);

        if (!editor.orderField) {
            return;
        }
        const orderSelector = 'input[name$="' + editor.orderField + '"]';
        Array
            .from(editor.element.querySelectorAll('.inline-related:not(.empty-form):not(.deleted)'))
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
                parent.insertBefore(item.item, editor.addImageButton);
            });
    }

    function bindEvents(editor) {
        editor.element.addEventListener('dragenter', handleDragEnter);
        editor.element.addEventListener('dragover', handleDragOver);
        editor.element.addEventListener('dragleave', handleDragLeave);
        editor.element.addEventListener('dragend', handleDragLeave);
        editor.element.addEventListener('drop', handleDrop);

        editor.addImageButton.addEventListener('click', handleAddImageClick);

        if (!editor.element.querySelector('.iuw-empty')) {
            return;
        }
        editor.element.querySelector('.iuw-empty').addEventListener('click', handleAddImageClick);
    }

    function buildInlineEditor(element) {
        const inlineGroup = element.closest('.inline-group');
        const inlineFormset = JSON.parse(inlineGroup.getAttribute('data-inline-formset'));
        const id = inlineGroup.id;
        element.setAttribute('data-editor', id);
        const orderField = inlineGroup.getAttribute('data-order-field')

        const editor = {
            id: id,
            element: element,
            canPreview: true,
            tempFileInput: null,
            element: element,
            inlineGroup: inlineGroup,
            inlineFormset: inlineFormset,
            management: getManagementInputs(inlineFormset.options.prefix),
            next: 0,
            maxCount: 0,
            addImageButton: element.querySelector('.iuw-add-image-btn'),
            orderField: orderField,
        };

        const tempFileInput = document.createElement('input');
        tempFileInput.setAttribute('type', 'file');
        tempFileInput.classList.add('temp_file');
        tempFileInput.setAttribute('accept', inlineGroup.getAttribute('data-accept') || 'image/*');
        tempFileInput.style.display = 'none';
        editor.tempFileInput = tempFileInput;
        editor.tempFileInput.addEventListener('change', handleTempFileInputChange);
        editor.element.appendChild(editor.tempFileInput);

        if (editor.management.maxNumForms.value === '') {
            editor.maxCount = Number.MAX_SAFE_INTEGER;
        } else {
            editor.maxCount = parseInt(editor.management.maxNumForms.value, 10);
        }

        window.uploaderEditors[id] = editor;
        
        updateEmptyState(editor);
        updateAllIndexes(editor);

        const related = element.querySelectorAll('.inline-related');
        for (const item of related) {
            updatePreviewState(editor, item);
        }

        bindEvents(editor);
    }

    const elements = document.querySelectorAll('.iuw-inline-root');
    for (const element of elements) {
        buildInlineEditor(element);
    }
});
