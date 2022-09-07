import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from image_uploader_widget_demo.demo_application import models

User = get_user_model()

class ImageUploaderWidget(StaticLiveServerTestCase):
    admin_url = '/admin/demo_application/testnonrequired/add/'
    url = ''

    def get_url(self, path):
        return "%s%s" % (self.live_server_url, path)

    @property
    def image_file(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mocks_dir = os.path.join(base_dir, "mocks")
        image = os.path.join(mocks_dir, "image.png")
        return image

    def setUp(self):
        self.url = self.get_url(self.admin_url)

        self.user = User.objects.create_superuser(
            'admin', 'admin@admin.com', 'admin'
        )
        
        self.selenium = webdriver.Chrome()
        self.selenium.get(self.get_url('/admin/login'))
        
        username = self.selenium.find_element(By.ID, "id_username")
        password = self.selenium.find_element(By.ID, "id_password")
        submit = self.selenium.find_element(By.XPATH, "//input[@type='submit']")

        username.send_keys('admin')
        password.send_keys('admin')
        submit.click()

    def test_empty_marker_click(self):
        """
        The empty marker must be visible and the file input click event should be
        called when click on the empty marker.
        """
        self.selenium.get(self.url)

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')

        injected_javascript = (
            'const callback = arguments[0];'
            'const input = document.querySelector(".form-row.field-image input[type=file]");'
            'input.addEventListener("click", (e) => { e.preventDefault(); alert("CLICKED"); });'
            'callback();'
        )
        self.selenium.execute_async_script(injected_javascript)

        empty_marker = form_row.find_element(By.CSS_SELECTOR, '.iuw-empty')
        self.assertTrue(empty_marker.is_displayed())

        empty_marker.click()
        self.selenium.switch_to.alert.accept()
        
    def test_non_required_file_input(self):
        """
        When send an image to the file input, should render an preview image with img tag,
        preview button and remove button.
        """
        itens = models.TestNonRequired.objects.all()
        self.assertEqual(len(itens), 0)

        self.selenium.get(self.url)

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 0)

        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]');

        self.assertEqual(file_input.get_attribute('value'), "")

        file_input.send_keys(self.image_file)

        self.assertEqual(file_input.get_attribute('value'), "C:\\fakepath\\image.png")

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        
        preview = previews[0]
        img = preview.find_element(By.TAG_NAME, 'img')
        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon');
        delete_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon');
        self.assertIsNotNone(img)
        self.assertIsNotNone(preview_button)
        self.assertIsNotNone(delete_button)

        submit = self.selenium.find_element(By.CSS_SELECTOR, '#testnonrequired_form [type="submit"]')
        submit.click()

        alert = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, ".messagelist .success"))
        self.assertIsNotNone(alert)
        itens = models.TestNonRequired.objects.all()
        self.assertEqual(len(itens), 1)
        item = itens[0]
        self.assertIsNotNone(item.image)


    def test_remove_button_with_non_saved_image(self):
        itens = models.TestNonRequired.objects.all()
        self.assertEqual(len(itens), 0)
        
        self.selenium.get(self.url)
        
        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]');
        
        self.assertEqual(file_input.get_attribute('value'), "")
        
        file_input.send_keys(self.image_file)

        self.assertEqual(file_input.get_attribute('value'), "C:\\fakepath\\image.png")

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        
        preview = previews[0]
        delete_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon');

        delete_button.click()

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        
        self.assertEqual(file_input.get_attribute('value'), "")
        self.assertEqual(len(previews), 0)
