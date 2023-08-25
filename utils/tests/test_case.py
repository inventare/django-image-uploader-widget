from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
