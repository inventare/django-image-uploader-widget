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

        self.assertIsNotNone(empty)
        self.assertTrue(empty.is_displayed())

    """
    def test_click_on_empty_marker(self):
        self.selenium.get(self.get_url(self.admin_add_url))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        empty = root.find_element(By.CSS_SELECTOR, '.iuw-empty')

        #empty.click()
        #temp_file = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, ".temp_file"))
        
        injected_javascript = (
            'const callback = arguments[0];'
            'const input = document.querySelector(".temp_file");'
            'input.addEventListener("click", (e) => { e.preventDefault(); alert("CLICKED"); });'
            'callback();'
        )
        self.selenium.execute_async_script(injected_javascript)

        #self.selenium.switch_to.alert.accept()
    """