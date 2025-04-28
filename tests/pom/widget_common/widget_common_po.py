import time
from playwright.sync_api import Page, ElementHandle, Locator
from tests.utils.images import get_mock_image
from tests.pom.preview_modal import PreviewModalPO
from .widget_common_pe import WidgetCommonPE

class WidgetCommonPO:
    def __init__(self, page: Page | ElementHandle):
        self.page = page
        self.page_elements = WidgetCommonPE(page)
        self.modal = PreviewModalPO(page)

    def is_empty_marker_visible(self):
        return self.page_elements.empty_marker.is_visible()

    def is_drop_label_visible(self):
        return self.page_elements.drop_label.is_visible()

    def execute_click_on_empty_marker(self):
        self.page_elements.empty_marker.click()

    def execute_dragenter(self):
        data_transfer = self.page.evaluate_handle("() => new DataTransfer()")
        self.page_elements.root.dispatch_event("dragenter", {"dataTransfer": data_transfer})
        time.sleep(0.5)

    def execute_dragleave(self):
        data_transfer = self.page.evaluate_handle("() => new DataTransfer()")
        self.page_elements.root.dispatch_event("dragleave", {"dataTransfer": data_transfer})
        time.sleep(0.5)

    def execute_drop(self):
        data_transfer = self.page.evaluate_handle("() => new DataTransfer()")
        self.page_elements.root.dispatch_event("drop", {"dataTransfer": data_transfer})
        time.sleep(0.5)

    def execute_dragend(self):
        data_transfer = self.page.evaluate_handle("() => new DataTransfer()")
        self.page_elements.root.dispatch_event("drop", {"dataTransfer": data_transfer})
        time.sleep(0.5)

    def get_visible_previews(self):
        previews = self.page_elements.get_previews()
        return list(
            filter(lambda item: item.is_visible(), previews)
        )

    def click_on_preview_iamge(self, preview: ElementHandle | Locator):
        self.page_elements.get_preview_image(preview).click()

    def click_on_preview_expand_button(self, preview: ElementHandle | Locator):
        self.page_elements.get_preview_expand_button(preview).click()

    def click_on_preview_delete_button(self, preview: ElementHandle | Locator):
        self.page_elements.get_delete_button(preview).click()

    def is_preview_valid(self, preview: ElementHandle | Locator, *, required: bool):
        img = self.page_elements.get_preview_image(preview)
        preview_button = self.page_elements.get_preview_expand_button(preview)
        conditions = [
            img != None,
            preview_button != None
        ]
        if not required:
            delete_button = self.page_elements.get_delete_button(preview)
            conditions += [delete_button != None]
        return all(conditions)

    def is_input_empty(self):
        return self.page_elements.file_input.get_attribute("value") == None

    def send_image_to_input(self, image: str):
        image = get_mock_image(image)
        self.page_elements.file_input.set_input_files(image)

    def is_delete_checkbox_checked(self):
        return self.page_elements.checkbox.is_checked()
