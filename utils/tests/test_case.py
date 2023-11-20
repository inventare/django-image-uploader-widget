from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.common.exceptions import NoAlertPresentException
from django.contrib.admin.tests import AdminSeleniumTestCase
from .admin import AdminMixin
from .image import ImageMixin
from .snapshot import SnapshotMixin

class IUWTestCase(AdminMixin, ImageMixin, SnapshotMixin, StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=2560,1440")

        cls.selenium = webdriver.Chrome(options=chrome_options)
    
    def setUp(self) -> None:
        self.light_mode()
        path = "%s%s" % (self.live_server_url, "/admin/login")
        self.selenium.get(path)
        self.login()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        
        cls.selenium.close()

    def dark_mode(self):
        self.selenium.execute_cdp_cmd('Emulation.setEmulatedMedia', {"features": [{"name": "prefers-color-scheme", "value": "dark"}]})

    def light_mode(self):
        self.selenium.execute_cdp_cmd('Emulation.setEmulatedMedia', {"features": [{"name": "prefers-color-scheme", "value": "default"}]})

    def get_widget_empty_marker(self):
        selector = ".form-row.field-image .iuw-empty"
        WebDriverWait(self.selenium, 10).until(element_to_be_clickable((By.CSS_SELECTOR, selector)))
        return self.selenium.find_element(By.CSS_SELECTOR, selector)
    
    def get_widget_form_row(self):
        return self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')

    def get_widget_root(self):
        return self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image .iuw-root')
    
    def get_widget_preview(self, root: WebElement):
        return root.find_element(By.CSS_SELECTOR, '.iuw-image-preview')
    
    def get_widget_preview_icon(self, root: WebElement):
        return root.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
    
    def get_widget_delete_icon(self, root: WebElement):
        return root.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')
    
    def get_preview_modal(self, black_overlay = False):
        if black_overlay:
            self.selenium.execute_script("document.getElementById('iuw-modal-element').style.background = '#000';")
            
        return self.selenium.find_element(By.ID, 'iuw-modal-element')

    def inject_input_file_clicked(self):
        injected_javascript = (
            'const callback = arguments[0];'
            'const input = document.querySelector(".form-row.field-image input[type=file]");'
            'input.addEventListener("click", (e) => { e.preventDefault(); alert("CLICKED"); });'
            'callback();'
        )
        self.selenium.execute_async_script(injected_javascript)
