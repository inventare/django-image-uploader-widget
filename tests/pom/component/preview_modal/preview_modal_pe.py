from playwright.sync_api import Page, Locator

class PreviewModalPE:
    def __init__(self, page: Page):
        self.page = page

    def get_modal(self, *, visible=True, timeout=3000, black_overlay=False):
        class_name = ""
        if visible:
            class_name = ".visible"

        selector = f"#iuw-modal-element{class_name}"

        preview_modal = self.page.locator(selector)
        preview_modal.wait_for(timeout=timeout)

        if black_overlay:
            self.page.evaluate(
                "document.getElementById('iuw-modal-element').style.background = '#000';"
            )

        return preview_modal

    def get_image(self, modal: Locator):
        return modal.locator('img')

    def get_close_button(self, modal: Locator):
        return modal.locator('.iuw-modal-close')
