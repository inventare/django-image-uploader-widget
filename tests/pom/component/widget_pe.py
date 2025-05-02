from typing import Union
from playwright.sync_api import Page, Locator

class WidgetPE:
    def __init__(self, page: Union[Page, Locator]):
        self.page = page
        self.root = page.locator(".iuw-root")
        self.empty_marker = self.root.locator(".iuw-empty")
        self.drop_label = self.root.locator(".iuw-drop-label")
        self.file_input = self.root.locator("input[type=file]")
        self.checkbox = self.root.locator("input[type=checkbox]")

    def get_thumbnails(self):
        return self.root.locator('.iuw-image-preview').all()
