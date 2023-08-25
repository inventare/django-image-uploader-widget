from django.contrib.auth import get_user_model
from django.core.files import File
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait
from image_uploader_widget_demo.demo_application import models
from utils.tests import IUWTestCase

User = get_user_model()

class RequiredWidgetTestCase(IUWTestCase):
    admin_add_url = '/admin/demo_application/testrequired/add/'

    def get_edit_url(self, id):
        return self.get_url_from_path("/admin/demo_application/testrequired/%s/change/" % id)
    
    def await_transition(self):
        pass

    def test_empty_marker_click(self):
        """
        should emit click event for the file input of the widget when
        click on the empty marker.
        """
        self.selenium.get(self.get_url_from_path(self.admin_add_url))

        WebDriverWait(self.selenium, 10).until(element_to_be_clickable((By.CSS_SELECTOR, ".iuw-empty")))
        #self.selenium.implicitly_wait(10)

        empty = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-empty')
        ActionChains(self.selenium).move_to_element(empty).perform()

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')

        self.assertMatchSnapshot(form_row, 'required_widget_empty')

