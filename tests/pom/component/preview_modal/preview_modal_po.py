from playwright.sync_api import Page, Locator
from tests.pom.component.thumbnail import ThumbnailPO
from .preview_modal_pe import PreviewModalPE

class PreviewModalPO:
    def __init__(self, page: Page):
        self.page = page
        self.page_elements = PreviewModalPE(page)

    def get_visible_modal_for(self, thumb: ThumbnailPO):
        thumb_img = thumb.page_elements.image

        preview_modal = self.page_elements.get_modal(
            visible=True,
            timeout=3000,
            black_overlay=False,
        )
        if preview_modal.get_attribute("class") != "iuw-modal visible":
            return None

        img = preview_modal.locator("img")
        if img.get_attribute("src") != thumb_img.get_attribute("src"):
            return None

        return preview_modal

    def execute_click_on_image(self, modal: Locator):
        self.page_elements.get_image(modal).click()

    def execute_click_on_close_button(self, modal: Locator):
        self.page_elements.get_close_button(modal).click()
