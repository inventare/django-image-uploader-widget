from playwright.sync_api import Page, ElementHandle

class PreviewModalPE:
    def __init__(self, page: Page):
        self.page = page

    def get_modal(self, visible = True, timeout=3000, black_overlay = False):
        class_name = ""
        if visible:
            class_name = ".visible"

        preview_modal = self.page.wait_for_selector(
            f"#iuw-modal-element{class_name}", timeout=timeout
        )

        if black_overlay:
            self.page.evaluate(
                "document.getElementById('iuw-modal-element').style.background = '#000';"
            )

        return preview_modal

    def get_image(self, modal: ElementHandle):
        return modal.query_selector('img')

    def get_close_button(self, modal: ElementHandle):
        return modal.query_selector('.iuw-modal-close')
