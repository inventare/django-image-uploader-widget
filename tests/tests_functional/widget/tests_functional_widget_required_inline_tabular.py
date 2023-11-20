from django.test.utils import tag
from selenium.webdriver.common.by import By
from tests import models
from utils.tests import IUWTestCase
from unittest import skip

@tag('functional')
@skip()
class RequiredWidgetTabularInlineTestCase(IUWTestCase):
    @property
    def admin_add_url(self):
        path = '/testrequiredtabularinline/add/'
        return self.get_url_from_path(path)
    
    def test_build_new_widget(self):
        """
        Test an basic flow of widget creation inside tabular inline.
        """
        itens = models.TestRequiredTabularInlineItem.objects.all()
        self.assertEqual(len(itens), 0)

        self.selenium.get(self.admin_add_url)

        inlines = self.selenium.find_elements(By.CSS_SELECTOR, '.tabular .form-row:not(.empty-form)')
        self.assertEqual(len(inlines), 0)

        add_row = self.selenium.find_element(By.CSS_SELECTOR, '.add-row a')
        add_row.click()
        add_row.click()

        inlines = self.selenium.find_elements(By.CSS_SELECTOR, '.tabular .form-row:not(.empty-form)')
        self.assertEqual(len(inlines), 2)

        for inline in inlines:
            iuw = inline.find_element(By.CSS_SELECTOR, '.iuw-root')
            file_input = iuw.find_element(By.CSS_SELECTOR, 'input[type=file]')

            self.assertIsNotNone(iuw)
            self.assertIsNotNone(file_input)

            file_input.send_keys(self.image1)

            self.assertEqual(file_input.get_attribute('value'), "C:\\fakepath\\image.png")

            preview = iuw.find_element(By.CSS_SELECTOR, '.iuw-image-preview')
            img = preview.find_element(By.TAG_NAME, 'img')
            preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
            self.assertTrue(preview.is_displayed())
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)

        submit = self.selenium.find_element(By.CSS_SELECTOR, '#testrequiredtabularinline_form [type="submit"]')
        submit.click()

        itens = models.TestRequiredTabularInlineItem.objects.all()
        self.assertEqual(len(itens), 2)
        for item in itens:
            self.assertIsNotNone(item.image)
