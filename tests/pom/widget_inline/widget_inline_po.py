import time
from playwright.sync_api import Page, Locator
from tests.utils.images import get_mock_image
from tests.pom.preview_modal import PreviewModalPO
from .widget_inline_pe import WidgetInlinePE

class WidgetInlinePO:
    """
    Page Object utils for inline editor and array field.
    """

    def __init__(self, page: Page | Locator):
        self.page = page
        self.page_elements = WidgetInlinePE(page)
        self.modal = PreviewModalPO(page)

    def get_visible_previews(self):
        """Returns the visible previews on the inline editor."""
        previews = self.page_elements.get_previews()
        return list(
            filter(lambda item: item.is_visible(), previews)
        )

    def choice_image(self, image: str):
        image = get_mock_image(image)
        self.page_elements.temp_file_input.set_input_files(image)

    def click_on_preview_delete(self, preview: Locator):
        button = self.page_elements.get_delete_button(preview)
        button.click()

    def click_on_preview_expand(self, preview: Locator):
        button = self.page_elements.get_expand_button(preview)
        button.click()

    def is_empty_marker_visible(self):
        return self.page_elements.empty_marker.is_visible()

    def click_on_empty_marker(self):
        self.page_elements.empty_marker.click()

    def is_add_button_visible(self):
        return self.page_elements.add_image_button.is_visible()

    def click_on_add_button(self):
        self.page_elements.add_image_button.click()
