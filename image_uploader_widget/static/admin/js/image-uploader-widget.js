document.addEventListener('DOMContentLoaded', function () {
    window.uploaderWidgets = {};
    const DELETE_ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path></svg>';
    const PREVIEW_ICON = '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-zoom-in" viewBox="0 0 16 16" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"></path><path xmlns="http://www.w3.org/2000/svg" d="M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z"></path><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z"></path></svg>';
    let DRAGGING_WIDGET = null;

    function renderPreview(url, canDelete, canPreview) {
        let deleteIcon = "";
        let previewIcon = "";
        if (canDelete) {
            deleteIcon = '<span class="iuw-delete-icon">' + DELETE_ICON + '</span>'
        }
        if (canPreview) {
            let className = "iuw-preview-icon";
            if (!canDelete) {
                className += " iuw-only-preview";
            }
            previewIcon = '<span class="' + className + '">' + PREVIEW_ICON + '</span>';
        }
        const div = document.createElement('div');
        div.className = "iuw-image-preview"
        div.innerHTML = '<img src="' + url + '" />' + deleteIcon + previewIcon;
        return div;
    }

    function getWidget(element) {
        const root = element.closest('.iuw-root');
        if (!root) {
            return null;
        }
        const id = root.getAttribute('data-widget');
        if (!id) {
            return null;
        }
        if (!Object.prototype.hasOwnProperty.call(window.uploaderWidgets, id)) {
            return null;
        }
        return window.uploaderWidgets[id];
    }

    function handleEmptyMarkerClick(e) {
        const widget = getWidget(e.target);
        if (!widget) {
            return;
        }
        widget.fileInput.click();
    }

    function handleFileInputChange(e) {
        const widget = getWidget(e.target);
        if (!widget) {
            return;
        }
        if (!widget.fileInput.files.length) {
            return;
        }
        widget.file = widget.fileInput.files[0];
        updateWidgetRenderState(widget);
    }

    function handleRemoveImage(imageElement) {
        const widget = getWidget(imageElement);
        if (!widget) {
            return;
        }

        imageElement.parentElement.removeChild(imageElement);
        if (widget.checkboxInput) {
            widget.checkboxInput.checked = true;
        }

        widget.fileInput.value = '';
        widget.file = null;
        widget.raw = null;
        updateWidgetRenderState(widget);
    }

    function handlePreviewImage(imageElement) {
        let image = imageElement.querySelector('img');
        if (!image) {
            return;
        }
        image = image.cloneNode(true);
        IUWPreviewModal.createPreviewModal(image);
        IUWPreviewModal.openPreviewModal();
    }

    function handleImagePreviewClick(e) {
        if (!e || !e.target) {
            return;
        }
        const targetElement = e.target;
        if (targetElement.closest('.iuw-delete-icon')) {
            const element = targetElement.closest('.iuw-image-preview');
            handleRemoveImage(element);
            return;
        }
        if (targetElement.closest('.iuw-preview-icon')) {
            const element = targetElement.closest('.iuw-image-preview');
            handlePreviewImage(element);
            return;
        }
        const widget = getWidget(targetElement);
        widget.fileInput.click();
    }

    function handleDragLeave(e) {
        if (e.relatedTarget && getWidget(e.relatedTarget) === DRAGGING_WIDGET) {
            return;
        }
        DRAGGING_WIDGET.dragging = false;
        DRAGGING_WIDGET.element.classList.remove('drop-zone');
        DRAGGING_WIDGET = null;
    }

    function handleDragEnter(e) {
        const widget = getWidget(e.target);
        if (!widget) {
            return;
        }
        DRAGGING_WIDGET = widget;
        widget.dragging = true;
        widget.element.classList.add('drop-zone');
    }

    function handleDragOver (e) {
        if (!e) {
            return;
        }
        e.preventDefault();
    }

    function handleDrop (e) {
        e.preventDefault();

        const widget = DRAGGING_WIDGET;
        if (!widget) {
            return;
        }
        widget.dragging = false;
        widget.element.classList.remove('drop-zone');
        
        DRAGGING_WIDGET = null;

        if (!e.dataTransfer.files.length) {
            return;
        }
        widget.fileInput.files = e.dataTransfer.files;
        widget.file = widget.fileInput.files[0];
        widget.raw = null;

        updateWidgetRenderState(widget);
    }

    function updateCheckboxAndEmptyState(widget) {
        if (!widget.file && !widget.raw) {
            widget.element.classList.add('empty');
            if (!widget.checkboxInput) {
                return;
            }
            widget.checkboxInput.checked = true;
            return;
        }
        widget.element.classList.remove('empty');
        if (!widget.checkboxInput) {
            return;
        }
        widget.checkboxInput.checked = false;
    }

    function updateWidgetRenderState(widget) {
        updateCheckboxAndEmptyState(widget);

        let previews = widget.element.querySelectorAll('.iuw-image-preview');
        for (const preview of previews) {
            widget.element.removeChild(preview);
        }

        if (!!widget.file) {
            const url = URL.createObjectURL(widget.file);
            widget.element.appendChild(renderPreview(url, widget.canDelete, widget.canPreview));
        } else if (!!widget.raw) {
            widget.element.appendChild(renderPreview(widget.raw, widget.canDelete, widget.canPreview));
        }

        previews = widget.element.querySelectorAll('.iuw-image-preview');
        for (const preview of previews) {
            preview.addEventListener('click', handleImagePreviewClick)
        }
    }

    function bindWidgetEvents(widget) {
        widget.fileInput.addEventListener('change', handleFileInputChange);
        widget.element.addEventListener('dragenter', handleDragEnter);
        widget.element.addEventListener('dragover', handleDragOver);
        widget.element.addEventListener('dragleave', handleDragLeave);
        widget.element.addEventListener('dragend', handleDragLeave);
        widget.element.addEventListener('drop', handleDrop);

        if (!widget.emptyMarker) {
            return;
        }
        widget.emptyMarker.addEventListener('click', handleEmptyMarkerClick);
    }
    
    function buildWidget(element) {
        const fileInput = element.querySelector('input[type=file]');
        const id = fileInput.id;
        element.setAttribute('data-widget', id);

        const widget = {
            id: id,
            element: element,
            fileInput: fileInput,
            checkboxInput: element.querySelector('input[type=checkbox]'),
            emptyMarker: element.querySelector('.iuw-empty'),
            canDelete: element.getAttribute('data-candelete') === 'true',
            canPreview: true,
            dragging: false,
            // values
            raw: element.getAttribute('data-raw'),
            file: null,
        };
        
        window.uploaderWidgets[id] = widget;

        bindWidgetEvents(widget);
        updateWidgetRenderState(widget);
        
        return widget;
    }

    function initializeWidgets(element) {
        const widgets = document.querySelectorAll('.iuw-root');
        for (const widgetElement of widgets) {
            buildWidget(widgetElement);
        }
    }

    initializeWidgets(document);

    if (window && window.django && window.django.jQuery) {
        const $ = window.django.jQuery;

        $(document).on('formset:added', (e, rows) => {
            if (!rows || !rows.length) {
                rows = [e.target]
            }
            if (!rows || !rows.length) {
                return;
            }
            initializeWidgets(rows[0]);
        });
    }
});
