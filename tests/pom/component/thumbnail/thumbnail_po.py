from typing import Union

from playwright.sync_api import Locator

from tests.utils.images import get_mock_image

from .thumbnail_pe import ThumbnailPE


class ThumbnailPO:
    @property
    def src(self):
        return self.page_elements.image.get_attribute("src")

    def __init__(self, locator: Locator):
        self.locator = locator
        self.page_elements = ThumbnailPE(locator)

    def execute_click_on_image(self):
        self.page_elements.image.click()

    def execute_click_on_preview(self):
        self.page_elements.preview.click()

    def execute_click_on_delete(self):
        self.page_elements.delete.click()

    def is_valid(self, *, required=False):
        img = self.page_elements.image.element_handle()
        preview_button = self.page_elements.preview.element_handle()
        conditions = [img != None, preview_button != None]

        if not required:
            delete_button = self.page_elements.delete.element_handle()
            conditions += [delete_button != None]

        return all(conditions)

    def execute_select_image(self, image: str):
        image = get_mock_image(image)
        self.page_elements.file_input.set_input_files(image)

    def is_order_input_valid(self, value: Union[str, int]):
        order_input = self.page_elements.order_input
        conditions = [
            order_input.is_visible() == False,
            order_input.input_value() == str(value),
        ]
        return all(conditions)

    def execute_move_to(self, other: "ThumbnailPO", *, to_left: bool):
        self.page_elements.thumb.hover()
        self.page_elements.thumb.page.mouse.down()

        other.page_elements.thumb.hover(position={"x": 40 if to_left else 100, "y": 10})
        other.page_elements.thumb.page.mouse.up()
