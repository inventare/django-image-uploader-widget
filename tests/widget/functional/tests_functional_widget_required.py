from django.contrib.auth import get_user_model
from django.core.files import File
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import invisibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from image_uploader_widget_demo.demo_application import models
from utils.tests import IUWTestCase

User = get_user_model()

class RequiredWidgetTestCase(IUWTestCase):
    @property
    def admin_add_url(self):
        path = '/admin/demo_application/testrequired/add/'
        return self.get_url_from_path(path)

    def get_edit_url(self, id):
        return self.get_url_from_path("/admin/demo_application/testrequired/%s/change/" % id)

    def init_item(self):
        item = models.TestRequired()
        with open(self.image1, 'rb') as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item
    
    def test_empty_marker_click(self):
        """
        should emit click event for the file input of the widget when
        click on the empty marker.
        """
        self.selenium.get(self.admin_add_url)

        self.inject_input_file_clicked()
        empty_marker = self.get_widget_empty_marker()
        self.assertTrue(empty_marker.is_displayed())

        empty_marker.click()
        self.assertEqual(self.selenium.switch_to.alert.text, "CLICKED")
        
    def test_required_file_input(self):
        """
        should create the preview image when file input value was changed and
        save item in database when submit the form.
        """
        self.selenium.get(self.admin_add_url)

        form_row = self.get_widget_form_row()

        with self.assertRaises(NoSuchElementException):
            preview = self.get_widget_preview(form_row)
        
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        self.assertEqual(file_input.get_attribute('value'), "")
        
        file_input.send_keys(self.image1)

        self.assertEqual(file_input.get_attribute('value'), "C:\\fakepath\\image.png")

        preview = self.get_widget_preview(form_row)
        img = preview.find_element(By.TAG_NAME, 'img')
        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        self.assertTrue(preview.is_displayed())
        self.assertIsNotNone(img)
        self.assertIsNotNone(preview_button)

        submit = self.selenium.find_element(By.CSS_SELECTOR, '#testrequired_form [type="submit"]')
        submit.click()

        alert = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, ".messagelist .success"))
        self.assertIsNotNone(alert)
        itens = models.TestRequired.objects.all()
        self.assertEqual(len(itens), 1)
        item = itens[0]
        self.assertIsNotNone(item.image)

    def test_image_with_database_data(self):
        """
        should create the preview with the value from the database when got the field initialized
        from database value.
        """
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview = self.get_widget_preview(root)

        self.assertIsNotNone(preview)
        self.assertEqual(root.get_attribute("data-raw"), item.image.url)

        empty_marker = root.find_element(By.CSS_SELECTOR, '.iuw-empty')
        self.assertFalse(empty_marker.is_displayed())

        img = preview.find_element(By.TAG_NAME, 'img')
        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        self.assertTrue(preview.is_displayed())
        self.assertIsNotNone(img)
        self.assertTrue(item.image.url in img.get_attribute('src'))
        self.assertIsNotNone(preview_button)

    def test_click_on_the_preview_image(self):
        """
        should emit the click event for the file input when click on the preview image.
        """
        self.selenium.get(self.admin_add_url)

        form_row = self.get_widget_form_row()
        with self.assertRaises(NoSuchElementException):
            preview = self.get_widget_preview(form_row)
            
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        file_input.send_keys(self.image2)
        
        self.inject_input_file_clicked()

        preview = self.get_widget_preview(form_row)
        self.assertIsNotNone(preview)
        img = preview.find_element(By.TAG_NAME, 'img')
        img.click()
        
        self.assertEqual(self.selenium.switch_to.alert.text, "CLICKED")

    def test_click_on_the_preview_button(self):
        """
        when click on the preview button, should open the preview modal
        with an img tag with the same src of the preview item.
        """
        self.selenium.get(self.admin_add_url)

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        file_input.send_keys(self.image2)
        
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        preview = previews[0]
        preview_img = preview.find_element(By.TAG_NAME, 'img')

        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        preview_button.click()
        
        preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))
        self.assertIsNotNone(preview_modal)
        self.assertEqual(preview_modal.get_attribute('class'), 'iuw-modal visible')

        img = preview_modal.find_element(By.TAG_NAME, 'img')
        self.assertIsNotNone(img)
        self.assertEqual(img.get_attribute("src"), preview_img.get_attribute("src"))

    def test_click_on_the_preview_button_and_image_on_modal(self):
        """
        when click on the preview button and open the preview modal, click on the image
        should not close the image preview modal.
        """
        self.selenium.get(self.admin_add_url)

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        file_input.send_keys(self.image1)
        
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        preview = previews[0]

        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        preview_button.click()
        
        preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))

        img = preview_modal.find_element(By.TAG_NAME, 'img')
        img.click()

        self.selenium.implicitly_wait(0.5)

        self.assertEqual(preview_modal.get_attribute("class"), "iuw-modal visible")

    def test_click_on_the_preview_button_and_close_on_modal(self):
        """
        when click on the preview button and open the preview modal, click on the close
        modal button should close the image preview modal.
        """
        self.selenium.get(self.admin_add_url)

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        file_input.send_keys(self.image1)
        
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        preview = previews[0]

        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        preview_button.click()
        
        preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))
        
        close_button = preview_modal.find_element(By.CSS_SELECTOR, '.iuw-modal-close')
        close_button.click()

        WebDriverWait(self.selenium, timeout=3).until(invisibility_of_element_located((By.CSS_SELECTOR, "#iuw-modal-element")));
