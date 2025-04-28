from playwright.sync_api import Page, ElementHandle
from .preview_modal_pe import PreviewModalPE

class PreviewModalPO:
    def __init__(self, page: Page):
        self.page = page
        self.page_elements = PreviewModalPE(page)

    def get_visible_modal_for(self, preview: ElementHandle):
        preview_img = preview.query_selector('img')

        preview_modal = self.page_elements.get_modal(True, 3000)
        if preview_modal.get_attribute("class") != "iuw-modal visible":
            return None

        img = preview_modal.query_selector("img")
        if img.get_attribute("src") != preview_img.get_attribute("src"):
            return None

        return preview_modal

    def click_on_modal_image(self, modal: ElementHandle):
        self.page_elements.get_image(modal).click()

    def click_on_modal_close_button(self, modal: ElementHandle):
        self.page_elements.get_close_button(modal).click()
