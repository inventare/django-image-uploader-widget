from django.contrib.auth import get_user_model
from django.core.files import File
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import invisibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from image_uploader_widget_demo.demo_application import models
from .base import IUWTestCase

User = get_user_model()

class RequiredWidgetTestCase(IUWTestCase):
    admin_add_url = '/admin/demo_application/testrequired/add/'

    def get_edit_url(self, id):
        return self.get_url("/admin/demo_application/testrequired/%s/change/" % id)

    def test_empty_marker_click(self):
        self.selenium.get(self.get_url(self.admin_add_url))

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
        self.assertEqual(self.selenium.switch_to.alert.text, "CLICKED")
        
    def test_required_file_input(self):
        itens = models.TestRequired.objects.all()
        self.assertEqual(len(itens), 0)

        self.selenium.get(self.get_url(self.admin_add_url))

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 0)

        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')

        self.assertEqual(file_input.get_attribute('value'), "")

        file_input.send_keys(self.image_file)

        self.assertEqual(file_input.get_attribute('value'), "C:\\fakepath\\image.png")

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        
        preview = previews[0]
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
        image_file = self.image_file
        item = models.TestRequired()
        with open(image_file, 'rb') as f:
            item.image.save("image.png", File(f))
        item.save()

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
        self.assertTrue(preview.is_displayed())
        self.assertIsNotNone(img)
        self.assertTrue(item.image.url in img.get_attribute('src'))
        self.assertIsNotNone(preview_button)

    def test_click_on_the_preview_image(self):
        self.selenium.get(self.get_url(self.admin_add_url))

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        file_input.send_keys(self.image_file)
        
        injected_javascript = (
            'const callback = arguments[0];'
            'const input = document.querySelector(".form-row.field-image input[type=file]");'
            'input.addEventListener("click", (e) => { e.preventDefault(); alert("CLICKED"); });'
            'callback();'
        )
        self.selenium.execute_async_script(injected_javascript)

        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        preview = previews[0]

        img = preview.find_element(By.TAG_NAME, 'img')
        img.click()
        
        self.assertEqual(self.selenium.switch_to.alert.text, "CLICKED")

    def test_click_on_the_preview_button(self):
        self.selenium.get(self.get_url(self.admin_add_url))

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        file_input.send_keys(self.image_file)
        
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
        self.selenium.get(self.get_url(self.admin_add_url))

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        file_input.send_keys(self.image_file)
        
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
        self.selenium.get(self.get_url(self.admin_add_url))

        form_row = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image')
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        file_input = form_row.find_element(By.CSS_SELECTOR, 'input[type=file]')
        file_input.send_keys(self.image_file)
        
        previews = form_row.find_elements(By.CSS_SELECTOR, '.iuw-image-preview')
        self.assertEqual(len(previews), 1)
        preview = previews[0]

        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        preview_button.click()
        
        preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))
        
        close_button = preview_modal.find_element(By.CSS_SELECTOR, '.iuw-modal-close')
        close_button.click()

        WebDriverWait(self.selenium, timeout=3).until(invisibility_of_element_located((By.CSS_SELECTOR, "#iuw-modal-element")));
