from playwright.sync_api import expect

class _AssertInputFileClicked:
    def __init__(self, test_case, input_selector=".form-row.field-image input[type=file]", index=0):
        self.test_case = test_case
        self.input_selector = input_selector
        self.index = index

    def __enter__(self):
        injected_javascript = (
            'async () => {'
            '   window.result = false;'
            f'  const inputs = document.querySelectorAll("{self.input_selector}");'
            f'  const input = inputs[{self.index}];'
            '   input.addEventListener("click", (e) => { e.preventDefault(); window.result = true; });'
            '};'
        )
        self.test_case.page.evaluate(injected_javascript)
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        self.test_case.assertEqual(str(self.test_case.page.evaluate_handle('window.result')), 'true')


class IUWMixin:
    def assert_input_file_clicked(self, input_selector=".form-row.field-image input[type=file]", index=0):
        return _AssertInputFileClicked(self, input_selector, index)
    
    def find_widget_form_row(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.form-row.field-image')

    def find_widget_root(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.form-row.field-image .iuw-root')
    
    def find_inline_root(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-inline-root')
    
    def find_widget_preview(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-image-preview')
    
    def find_inline_previews(self, element=None):
        if not element:
            element = self.page
        return element.query_selector_all('.inline-related:not(.empty-form):not(.deleted)')
    
    def find_deleted_inline_previews(self, element=None):
        if not element:
            element = self.page
        return element.query_selector_all('.inline-related:not(.empty-form).deleted')
    
    def find_empty_marker(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-empty')

    def find_preview_icon(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-preview-icon')
    
    def find_delete_icon(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-delete-icon')
    
    def find_add_button(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-add-image-btn')
    
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
