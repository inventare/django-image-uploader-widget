(() => {
  var __defProp = Object.defineProperty;
  var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
  var __publicField = (obj, key, value) => __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);

  // src/components/Preview/constants.ts
  var previewClasses = {
    preview: "iuw-image-preview",
    deleteIcon: "iuw-delete-icon",
    previewIcon: "iuw-preview-icon",
    onlyPreview: "iuw-only-preview"
  };

  // src/components/Widget/constants.ts
  var widgetClasses = {
    root: "iuw-root",
    empty: "empty",
    ...previewClasses
  };

  // src/components/icons/CloseIcon.ts
  var CloseIcon = `
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%">
    <path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path>
  </svg>
`;

  // src/components/icons/DeleteIcon.ts
  var DeleteIcon = `
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%">
    <path xmlns="http://www.w3.org/2000/svg" d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path>
  </svg>
`;

  // src/components/icons/PreviewIcon.ts
  var PreviewIcon = `
  <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-zoom-in" viewBox="0 0 16 16" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%">
    <path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"></path>
    <path xmlns="http://www.w3.org/2000/svg" d="M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z"></path>
    <path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z"></path>
  </svg>
`;

  // src/components/Preview/renderer.ts
  var renderDeleteButton = (canDelete) => {
    if (!canDelete) {
      return "";
    }
    return `<span class="${previewClasses.deleteIcon}">${DeleteIcon}</span>`;
  };
  var renderPreviewButton = (canDelete, canPreview) => {
    if (!canPreview) {
      return "";
    }
    const className = canDelete ? previewClasses.previewIcon : `${previewClasses.previewIcon} ${previewClasses.onlyPreview}`;
    return `<span class="${className}">${PreviewIcon}</span>`;
  };
  var renderPreview = (url, canDelete, canPreview) => {
    const deleteButton = renderDeleteButton(canDelete);
    const previewButton = renderPreviewButton(canDelete, canPreview);
    const div = document.createElement("div");
    div.className = previewClasses.preview;
    div.innerHTML = '<img src="' + url + '" />' + deleteButton + previewButton;
    return div;
  };

  // src/components/PreviewModal/constants.ts
  var previewModalClasses = {
    image: "iuw-modal-image-preview-item",
    preview: "iuw-modal-image-preview",
    modal: "iuw-modal hide",
    closeButton: "iuw-modal-close",
    visible: "visible",
    hide: "hide"
  };
  var previewModalId = "iuw-modal-element";

  // src/components/PreviewModal/renderer.ts
  var renderCloseButton = (previewModal) => {
    const cl = previewModalClasses.closeButton;
    const closeButtonHtml = `<span class="${cl}">${CloseIcon}</span>`;
    previewModal.innerHTML = closeButtonHtml;
    return previewModal.querySelector(`span.${cl}`);
  };
  var renderModal = (image) => {
    const modal = document.createElement("div");
    modal.id = previewModalId;
    modal.className = previewModalClasses.modal;
    const preview = document.createElement("div");
    preview.className = previewModalClasses.preview;
    image.className = previewModalClasses.image;
    renderCloseButton(preview);
    preview.appendChild(image);
    modal.appendChild(preview);
    return modal;
  };

  // src/components/PreviewModal/PreviewModal.ts
  var _PreviewModal = class _PreviewModal {
    static getInstance() {
      if (!_PreviewModal.instance) {
        _PreviewModal.instance = new _PreviewModal();
      }
      return _PreviewModal.instance;
    }
    static handleModalClick(ev) {
      if (!ev || !ev.target) {
        return;
      }
      const element = ev.target;
      if (element.closest(`.${previewModalClasses.image}`)) {
        return;
      }
      _PreviewModal.getInstance().close();
    }
    constructor() {
    }
    createModalElement(image) {
      const modal = renderModal(image);
      modal.addEventListener("click", _PreviewModal.handleModalClick);
      document.body.appendChild(modal);
      return modal;
    }
    removeExistingModalElement() {
      var _a;
      const modal = document.getElementById(previewModalId);
      if (!modal) {
        return;
      }
      (_a = modal.parentElement) == null ? void 0 : _a.removeChild(modal);
    }
    close() {
      document.body.style.overflow = "auto";
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
    show(image) {
      this.removeExistingModalElement();
      const modal = this.createModalElement(image);
      setTimeout(() => {
        modal.classList.add(previewModalClasses.visible);
        modal.classList.remove(previewModalClasses.hide);
        document.body.style.overflow = "hidden";
      }, 50);
    }
  };
  __publicField(_PreviewModal, "instance");
  var PreviewModal = _PreviewModal;

  // src/components/Widget/Widget.ts
  var WidgetInputNotFoundError = class extends Error {
    constructor(input) {
      super(`The widget ${input} input was not found.`);
    }
  };
  var _Widget = class _Widget {
    constructor(element) {
      __publicField(this, "element");
      __publicField(this, "id", "");
      __publicField(this, "file", null);
      __publicField(this, "raw", null);
      this.element = element;
      this.buildWidget();
      this.addEvents();
      _Widget.pushInstance(this);
    }
    static pushInstance(instance) {
      _Widget.instances.push(instance);
    }
    static getInstance(element) {
      const root = element.closest(`.${widgetClasses.root}`);
      if (!root || !root.getAttribute("data-widget")) {
        return null;
      }
      const id = root.getAttribute("data-widget");
      const items = _Widget.instances.filter((item) => item.id === id);
      if (!items.length) {
        return null;
      }
      return items[0];
    }
    static handleEmptyMarkerClick(e) {
      const widget = _Widget.getInstance(e.target);
      if (!widget) {
        return;
      }
      widget.fileInput.click();
    }
    static handleFileInputChange(e) {
      var _a;
      const widget = _Widget.getInstance(e.target);
      if (!widget) {
        return;
      }
      if (!((_a = widget.fileInput.files) == null ? void 0 : _a.length)) {
        return;
      }
      widget.file = widget.fileInput.files[0];
      widget.render();
    }
    static handleImagePreviewClick(e) {
      if (!e || !e.target) {
        return;
      }
      const targetElement = e.target;
      const widget = _Widget.getInstance(targetElement);
      if (!widget) {
        return;
      }
      if (targetElement.closest(`.${widgetClasses.deleteIcon}`)) {
        const element = targetElement.closest(`.${widgetClasses.preview}`);
        if (!element) {
          return;
        }
        return widget.removeImage(element);
      }
      if (targetElement.closest(`.${widgetClasses.previewIcon}`)) {
        const element = targetElement.closest(`.${widgetClasses.preview}`);
        if (!element) {
          return;
        }
        return widget.previewImage(element);
      }
      widget == null ? void 0 : widget.fileInput.click();
    }
    get fileInput() {
      const input = this.element.querySelector("input[type=file]");
      if (!input) {
        throw new WidgetInputNotFoundError("file");
      }
      return input;
    }
    get checkboxInput() {
      return this.element.querySelector("input[type=checkbox]");
    }
    get emptyMarker() {
      return this.element.querySelector(".iuw-empty");
    }
    get canDelete() {
      return this.element.getAttribute("data-candelete") === "true";
    }
    get canPreview() {
      return this.element.getAttribute("data-canpreview") === "true";
    }
    get previews() {
      return this.element.querySelectorAll(`.${widgetClasses.preview}`);
    }
    addEvents() {
      this.fileInput.addEventListener("change", _Widget.handleFileInputChange);
      if (!this.emptyMarker) {
        return;
      }
      this.emptyMarker.addEventListener("click", _Widget.handleEmptyMarkerClick);
    }
    buildWidget() {
      this.id = this.fileInput.id;
      this.element.setAttribute("data-widget", this.id);
      this.raw = this.element.getAttribute("data-raw");
      this.render();
    }
    updateStates() {
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
      this.previews.forEach((item) => {
        var _a;
        return (_a = item.parentElement) == null ? void 0 : _a.removeChild(item);
      });
      const url = this.file ? URL.createObjectURL(this.file) : this.raw;
      if (!url) {
        return;
      }
      this.element.appendChild(renderPreview(url, this.canDelete, this.canPreview));
      this.previews.forEach((item) => item.addEventListener("click", _Widget.handleImagePreviewClick));
    }
    removeImage(imageElement) {
      var _a;
      (_a = imageElement.parentElement) == null ? void 0 : _a.removeChild(imageElement);
      if (this.checkboxInput) {
        this.checkboxInput.checked = true;
      }
      this.fileInput.value = "";
      this.file = null;
      this.raw = null;
      this.render();
    }
    previewImage(imageElement) {
      let image = imageElement.querySelector("img");
      if (!image) {
        return;
      }
      image = image.cloneNode(true);
      PreviewModal.getInstance().show(image);
    }
  };
  __publicField(_Widget, "instances", []);
  var Widget = _Widget;

  // src/widget.ts
  window.initializeWidgets = (element) => {
    Array.from(element.querySelectorAll(`.${widgetClasses.root}`)).map((item) => new Widget(item));
  };
  document.addEventListener("DOMContentLoaded", () => {
    window.initializeWidgets(document);
    if (window && window.django && window.django.jQuery) {
      const $ = window.django.jQuery;
      $(document).on("formset:added", (e, rows) => {
        if (!rows || !rows.length) {
          rows = [e.target];
        }
        if (!rows || !rows.length) {
          return;
        }
        window.initializeWidgets(rows[0]);
      });
    }
    ;
  });
})();
