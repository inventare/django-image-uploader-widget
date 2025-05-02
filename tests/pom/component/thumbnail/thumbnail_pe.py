from playwright.sync_api import Locator

class ThumbnailPE:
    def __init__(self, thumb: Locator):
        self.thumb = thumb

        self.image = self.thumb.locator("img")
        self.preview = self.thumb.locator(".iuw-preview-icon")
        self.delete = self.thumb.locator(".iuw-delete-icon")
        self.file_input = self.thumb.locator("input[type=file]")
        self.checkbox_input = self.thumb.locator("input[type=checkbox]")
        self.order_input = self.thumb.locator('input[name$="order"]')
