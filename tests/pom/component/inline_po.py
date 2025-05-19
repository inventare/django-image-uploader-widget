from typing import Union

from playwright.sync_api import Locator, Page

from tests.pom.component.preview_modal import PreviewModalPO
from tests.utils.images import get_mock_image

from .inline_pe import InlinePE
from .thumbnail import ThumbnailPO
from .widget_drag_po import WidgetDragPO


class InlinePO(WidgetDragPO):
    """
    Page Object utils for inline editor and array field.
    """

    def __init__(self, page: Union[Page, Locator]):
        self.page = page
        self.page_elements = InlinePE(page)
        self.modal = PreviewModalPO(page)

    def get_visible_thumbnails(self):
        thumbs = self.page_elements.get_thumbnails()
        thumbs = list(filter(lambda item: item.is_visible(), thumbs))
        return list(map(lambda item: ThumbnailPO(item), thumbs))

    def execute_select_image(self, image: str):
        image = get_mock_image(image)
        self.page_elements.temp_file_input.set_input_files(image)

    def execute_select_multiple_images(self, images):
        images = [get_mock_image(img) for img in images]
        self.page_elements.temp_file_input.set_input_files(images)

    def is_add_button_visible(self):
        return self.page_elements.add_image_button.is_visible()

    def execute_click_on_add_button(self):
        self.page_elements.add_image_button.click()

    def execute_hover_on_add_button(self):
        self.page_elements.add_image_button.hover()

    def is_empty_marker_visible(self):
        return self.page_elements.empty_marker.is_visible()

    def execute_click_on_empty_marker(self):
        self.page_elements.empty_marker.click()

    def execute_hover_on_empty_marker(self):
        self.page_elements.empty_marker.hover()
