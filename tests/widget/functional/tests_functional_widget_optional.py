from django.contrib.auth import get_user_model
from django.core.files import File
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import invisibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from image_uploader_widget_demo.demo_application import models
from utils.tests import IUWTestCase

User = get_user_model()

class OptionalWidgetTestCase(IUWTestCase):
    @property
    def admin_add_url(self):
        return self.get_url_from_path('/admin/demo_application/testnonrequired/add/')

    def get_edit_url(self, id):
        return self.get_url_from_path("/admin/demo_application/testnonrequired/%s/change/" % id)

    def init_item(self):
        item = models.TestNonRequired()
        with open(self.image2, 'rb') as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item
    
    def test_empty_marker_click(self):
        """
        The empty marker must be visible and the file input click event should be
        emited when click on the empty marker.
        """
        self.selenium.get(self.admin_add_url)

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')

        self.inject_input_file_clicked()

        empty_marker = form_row.find_element(By.CSS_SELECTOR, '.iuw-empty')
        self.assertTrue(empty_marker.is_displayed())

        empty_marker.click()
        self.assertEqual(self.selenium.switch_to.alert.text, "CLICKED")
        
    def test_non_required_file_input(self):
        """
        When send an image to the file input, should render an preview image with img tag,
        preview button and remove button.
        """
        itens = models.TestNonRequired.objects.all()
        self.assertEqual(len(itens), 0)

        self.selenium.get(self.admin_add_url)

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 0)

        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')

        self.assertEqual(file_input.get_attribute('value'), "")

        file_input.send_keys(self.image1)

        self.assertEqual(file_input.get_attribute('value'), "C:\\fakepath\\image.png")

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        
        preview = previews[0]
        img = preview.find_element(By.TAG_NAME, 'img')
        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        delete_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')
        self.assertTrue(preview.is_displayed())
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
        """
        Should remove the preview image when click on the remove
        without saved item.
        """
        itens = models.TestNonRequired.objects.all()
        self.assertEqual(len(itens), 0)
        
        self.selenium.get(self.admin_add_url)
        
        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        
        self.assertEqual(file_input.get_attribute('value'), "")
        
        file_input.send_keys(self.image2)

        self.assertEqual(file_input.get_attribute('value'), "C:\\fakepath\\image2.png")

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        
        preview = previews[0]
        delete_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')

        delete_button.click()

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        
        self.assertEqual(file_input.get_attribute('value'), "")
        self.assertEqual(len(previews), 0)

    def test_image_with_database_data(self):
        """
        Should create the preview item from the database data when gots editing
        an item.
        """
        item = self.init_item()

        self.selenium.get(self.get_edit_url(item.id))

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        root = form_row.find_element(By.CSS_SELECTOR, '.iuw-root')

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        self.assertEqual(root.get_attribute("data-raw"), item.image.url)

        empty_marker = form_row.find_element(By.CSS_SELECTOR, '.iuw-empty')
        self.assertFalse(empty_marker.is_displayed())

        preview = previews[0]
        img = preview.find_element(By.TAG_NAME, 'img')
        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        delete_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')
        self.assertTrue(preview.is_displayed())
        self.assertIsNotNone(img)
        self.assertTrue(item.image.url in img.get_attribute('src'))
        self.assertIsNotNone(preview_button)
        self.assertIsNotNone(delete_button)        

    def test_delete_saved_image(self):
        """
        Should check the delete checkbox when click on the remove button for a
        saved image item and submit the form should remove it from the database.
        """
        item = self.init_item()

        self.selenium.get(self.get_edit_url(item.id))

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        checkbox = form_row.find_element(By.CSS_SELECTOR, '[type=checkbox]')
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        preview = previews[0]

        self.assertFalse(checkbox.is_selected())

        delete_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')

        delete_button.click()

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 0)

        self.assertTrue(checkbox.is_selected())

        submit = self.selenium.find_element(By.CSS_SELECTOR, '#testnonrequired_form [type="submit"]')
        submit.click()

        itens = models.TestNonRequired.objects.all()
        self.assertEqual(len(itens), 1)
        item = itens[0]
        self.assertFalse(bool(item.image))

    def test_click_on_the_preview_image(self):
        """
        Should emit the click event for the file input when click on the preview image.
        """
        self.selenium.get(self.admin_add_url)

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        file_input.send_keys(self.image1)
        
        self.inject_input_file_clicked()

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        preview = previews[0]

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

        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        preview_button.click()
        
        preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))
        self.assertIsNotNone(preview_modal)
        self.assertEqual(preview_modal.get_attribute('class'), 'iuw-modal visible')

        img = preview_modal.find_element(By.TAG_NAME, 'img')
        self.assertIsNotNone(img)

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
        file_input.send_keys(self.image2)
        
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        preview = previews[0]

        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        preview_button.click()
        
        preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))
        
        close_button = preview_modal.find_element(By.CSS_SELECTOR, '.iuw-modal-close')
        close_button.click()

        WebDriverWait(self.selenium, timeout=3).until(invisibility_of_element_located((By.CSS_SELECTOR, "#iuw-modal-element")));
