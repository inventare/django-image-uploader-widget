from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from .admin import AdminMixin
from .image import ImageMixin
from .snapshot import SnapshotMixin

class IUWTestCase(AdminMixin, ImageMixin, SnapshotMixin, StaticLiveServerTestCase):
    headless = True

    def setUp(self):
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument("--window-size=2560,1440")

        self.selenium = webdriver.Chrome(options=chrome_options)
        self.selenium.get(self.get_url_from_path('/admin/login'))

        self.login()

    def get_widget_empty_marker(self):
        selector = ".form-row.field-image .iuw-empty"
        WebDriverWait(self.selenium, 10).until(element_to_be_clickable((By.CSS_SELECTOR, selector)))
        return self.selenium.find_element(By.CSS_SELECTOR, selector)
    
    def get_widget_root(self):
        return self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image .iuw-root')
    
    def get_widget_preview(self, root: WebElement):
        return root.find_element(By.CSS_SELECTOR, '.iuw-image-preview')
    
    def get_preview_modal(self):
        return self.selenium.find_element(By.ID, 'iuw-modal-element')
