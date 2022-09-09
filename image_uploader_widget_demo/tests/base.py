import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

User = get_user_model()

class IUWTestCase(StaticLiveServerTestCase):
    def get_url(self, path):
        return "%s%s" % (self.live_server_url, path)

    @property
    def image_file(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mocks_dir = os.path.join(base_dir, "mocks")
        image = os.path.join(mocks_dir, "image.png")
        return image

    def setUp(self):
        self.user = User.objects.create_superuser(
            'admin', 'admin@admin.com', 'admin'
        )
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.selenium = webdriver.Chrome(options=chrome_options)
        self.selenium.get(self.get_url('/admin/login'))
        
        username = self.selenium.find_element(By.ID, "id_username")
        password = self.selenium.find_element(By.ID, "id_password")
        submit = self.selenium.find_element(By.XPATH, "//input[@type='submit']")

        username.send_keys('admin')
        password.send_keys('admin')
        submit.click()
