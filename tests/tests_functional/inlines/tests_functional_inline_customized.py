from django.test import tag
from selenium.webdriver.common.by import By
from utils.tests import IUWTestCase

@tag('functional')
class CustomizedInlineEditorTestCase(IUWTestCase):
    @property
    def admin_add_url(self):
        return self.get_url_from_path('/custominline/add/')

    def test_have_customized_itens(self):
        self.selenium.get(self.admin_add_url)

        self.selenium.implicitly_wait(1)

        empty = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-empty')
        dropzone = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-drop-label')
        add = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-add-image-btn')

        empty_text = empty.get_attribute("textContent").strip().replace(" ", "").replace("\n", "")
        dropzone_text = dropzone.get_attribute("textContent").strip().replace(" ", "").replace("\n", "")
        add_text = add.get_attribute("textContent").strip().replace(" ", "").replace("\n", "")
        
        self.assertEqual(empty_text, "empty_icon" + "empty_text")
        self.assertEqual(dropzone_text, "drop_icon" + "drop_text")
        self.assertEqual(add_text, "add_icon" + "add_image_text")