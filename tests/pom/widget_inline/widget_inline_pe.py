from playwright.sync_api import Page, Locator

class WidgetInlinePE:
    def __init__(self, page: Page | Locator):
        self.page = page
        self.root = page.locator(".iuw-inline-root")
        self.temp_file_input = self.root.locator(".temp_file")
        self.add_image_button = self.root.locator(".iuw-add-image-btn")
        self.empty_marker = self.root.locator(".iuw-empty")

    def get_previews(self):
        return self.root.locator('.inline-related:not(.empty-form):not(.deleted)').all()

    def get_delete_button(self, preview: Locator):
        return preview.locator(".iuw-delete-icon")

    def get_expand_button(self, preview: Locator):
        return preview.locator(".iuw-preview-icon")
