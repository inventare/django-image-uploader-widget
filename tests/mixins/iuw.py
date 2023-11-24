from playwright.sync_api import expect

class _AssertInputFileClicked:
    def __init__(self, test_case):
        self.test_case = test_case

    def __enter__(self):
        injected_javascript = (
            'async () => {'
            '   window.result = false;'
            f'   const input = document.querySelector("{self.test_case.input_selector}");'
            '   input.addEventListener("click", (e) => { e.preventDefault(); window.result = true; });'
            '};'
        )
        self.test_case.page.evaluate(injected_javascript)
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        self.test_case.assertEqual(str(self.test_case.page.evaluate_handle('window.result')), 'true')


class IUWMixin:
    input_selector = ".form-row.field-image input[type=file]"

    def assert_input_file_clicked(self):
        return _AssertInputFileClicked(self)
    
    def find_widget_form_row(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.form-row.field-image')

    def find_widget_root(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.form-row.field-image .iuw-root')
    
    def find_widget_preview(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-image-preview')
    
    def find_empty_marker(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-empty')

    def find_preview_icon(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-preview-icon')
    
    def get_preview_modal(self, visible=True, timout=3000, black_overlay=False):
        class_name = ''
        if visible:
            class_name = '.visible'

        preview_modal = self.page.wait_for_selector(f'#iuw-modal-element{class_name}', timeout=timout)

        if black_overlay:
            self.page.evaluate("document.getElementById('iuw-modal-element').style.background = '#000';")

        return preview_modal

    def assert_preview_modal(self, preview_img):
        preview_modal = self.get_preview_modal(True, 3000)
        self.assertIsNotNone(preview_modal)
        self.assertEqual(preview_modal.get_attribute('class'), 'iuw-modal visible')

        img = preview_modal.query_selector('img')
        self.assertIsNotNone(img)
        self.assertEqual(img.get_attribute("src"), preview_img.get_attribute("src"))

    def assert_preview_modal_close(self):
        preview_modal = self.get_preview_modal(True, 0)
        close_button = preview_modal.query_selector('.iuw-modal-close')
        close_button.click()

        locator = self.page.locator('#iuw-modal-element')
        expect(locator).not_to_be_visible(timeout=3000)
    
    def wait_for_empty_marker(self, element=None, timeout=3000):
        if not element:
            element = self.page
        return element.wait_for_selector('.iuw-empty', timeout=timeout)
