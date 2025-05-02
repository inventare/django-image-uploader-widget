from typing import Union
from playwright.sync_api import Page, Locator
from tests.utils.images import get_mock_image
from tests.pom.component.preview_modal import PreviewModalPO
from .widget_pe import WidgetPE
from .widget_drag_po import WidgetDragPO
from .thumbnail import ThumbnailPO

class WidgetPO(WidgetDragPO):
    @property
    def data_raw(self):
        return self.page_elements.root.get_attribute("data-raw")

    def __init__(self, page: Union[Page, Locator]):
        self.page = page
        self.page_elements = WidgetPE(page)
        self.modal = PreviewModalPO(page)

    def is_empty_marker_visible(self):
        return self.page_elements.empty_marker.is_visible()

    def execute_click_on_empty_marker(self):
        self.page_elements.empty_marker.click()

    def get_visible_thumbnails(self):
        thumbs = self.page_elements.get_thumbnails()
        thumbs = list(filter(lambda item: item.is_visible(), thumbs))
        return list(map(lambda item: ThumbnailPO(item), thumbs))

    def is_input_empty(self):
        return self.page_elements.file_input.get_attribute("value") == None

    def execute_select_image(self, image: str):
        image = get_mock_image(image)
        self.page_elements.file_input.set_input_files(image)

    def is_delete_checkbox_checked(self):
        return self.page_elements.checkbox.is_checked()
