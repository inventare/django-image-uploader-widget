document.addEventListener('DOMContentLoaded', function () {
    window.uploaderWidgets = {};
    let DRAGGING_WIDGET = null;

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
    
});
