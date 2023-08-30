from django.core.files import File
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import invisibility_of_element_located
from image_uploader_widget_demo.demo_application import models
from utils.tests import IUWTestCase

class InlineEditorUIRegressionTestCase(IUWTestCase):
    @property
    def admin_add_url(self):
        return self.get_url_from_path('/admin/demo_application/inline/add/')

    def get_edit_url(self, id):
        return self.get_url_from_path("/admin/demo_application/inline/%s/change/" % id)
    
    def test_empty_marker(self):
        self.selenium.get(self.admin_add_url)

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        
        self.wait(0.4)

        self.assertMatchSnapshot(root, 'in_test_empty_marker')

    def test_empty_marker_hover(self):
        self.selenium.get(self.admin_add_url)

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        empty = root.find_element(By.CSS_SELECTOR, '.iuw-empty')

        self.hover_and_wait(empty, 0.4)

        self.assertMatchSnapshot(root, 'in_test_empty_marker_hover')
