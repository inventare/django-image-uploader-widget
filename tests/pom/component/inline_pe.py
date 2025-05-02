from typing import Union

from playwright.sync_api import Locator, Page


class InlinePE:
    def __init__(self, page: Union[Page, Locator]):
        self.page = page
        self.root = page.locator(".iuw-inline-root")
        self.temp_file_input = self.root.locator(".temp_file")
        self.add_image_button = self.root.locator(".iuw-add-image-btn")
        self.empty_marker = self.root.locator(".iuw-empty")
        self.drop_label = self.root.locator(".iuw-drop-label")

    def get_thumbnails(self):
        return self.root.locator(".inline-related:not(.empty-form):not(.deleted)").all()
