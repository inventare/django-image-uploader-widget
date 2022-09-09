from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from image_uploader_widget_demo.demo_application import models
from .base import IUWTestCase

class InlineEditorTestCase(IUWTestCase):
    admin_add_url = '/admin/demo_application/inline/add/'
    
    def test_have_empty_marker(self):
        self.selenium.get(self.get_url(self.admin_add_url))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        empty = root.find_element(By.CSS_SELECTOR, '.iuw-empty')

        self.selenium.implicitly_wait(1)

        self.assertIsNotNone(empty)
        self.assertTrue(empty.is_displayed())

    def test_click_on_empty_marker(self):
        self.selenium.get(self.get_url(self.admin_add_url))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        empty = root.find_element(By.CSS_SELECTOR, '.iuw-empty')

        injected_javascript = (
            'const callback = arguments[0];'
            'const input = document.querySelector(".temp_file");'
            'input.addEventListener("click", (e) => { e.preventDefault(); alert("CLICKED"); });'
            'callback();'
        )
        self.selenium.execute_async_script(injected_javascript)

        empty.click()

        self.selenium.switch_to.alert.accept()

    def test_send_images(self):
        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 0)

        self.selenium.get(self.get_url(self.admin_add_url))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        temp_file = root.find_element(By.CSS_SELECTOR, '.temp_file')

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form)')
        self.assertEqual(len(previews), 0)

        temp_file.send_keys(self.image_file)

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form)')
        self.assertEqual(len(previews), 1)
        
        temp_file.send_keys(self.image_file2)

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form)')
        self.assertEqual(len(previews), 2)

        for preview in previews:
            img = preview.find_element(By.TAG_NAME, 'img')
            preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
            remove_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

        submit = self.selenium.find_element(By.CSS_SELECTOR, '#inline_form [type="submit"]')
        submit.click()

        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 2)
        for item in items:
            self.assertIsNotNone(item.image)

    def test_remove_not_saved_inline(self):
        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 0)

        self.selenium.get(self.get_url(self.admin_add_url))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        temp_file = root.find_element(By.CSS_SELECTOR, '.temp_file')

        temp_file.send_keys(self.image_file)

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form)')
        self.assertEqual(len(previews), 1)
        preview = previews[0]

        remove_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')
        
        remove_button.click()
        
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form)')
        self.assertEqual(len(previews), 0)

        submit = self.selenium.find_element(By.CSS_SELECTOR, '#inline_form [type="submit"]')
        submit.click()

        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 0)
