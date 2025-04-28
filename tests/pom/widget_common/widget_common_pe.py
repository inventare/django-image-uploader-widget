from playwright.sync_api import Page, ElementHandle, Locator

class WidgetCommonPE:
    def __init__(self, page: Page | Locator):
        self.page = page
        self.form_row = page.locator(".form-row.field-image")
        self.root = page.locator(".iuw-root")
        self.empty_marker = self.root.locator(".iuw-empty")
        self.drop_label = self.root.locator(".iuw-drop-label")
        self.file_input = self.root.locator("input[type=file]")
        self.checkbox = self.root.locator("input[type=checkbox]")

    def get_previews(self):
        root = self.root.element_handle()
        return root.query_selector_all('.iuw-image-preview')

    def get_preview_image(self, preview: ElementHandle | Locator):
        if isinstance(preview, Locator):
            preview = preview.element_handle()
        return preview.query_selector('img')

    def get_preview_expand_button(self, preview: ElementHandle | Locator):
        if isinstance(preview, Locator):
            preview = preview.element_handle()
        return preview.query_selector(".iuw-preview-icon")

    def get_delete_button(self, preview: ElementHandle | Locator):
        if isinstance(preview, Locator):
            preview = preview.element_handle()
        return preview.query_selector(".iuw-delete-icon")
