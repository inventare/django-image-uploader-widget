from django.test import tag
from django.core.files import File
from tests import models, TestCase

@tag('playwright')
class WidgetRequiredTests(TestCase):
    model = 'testrequired'

    def init_item(self):
        item = models.TestRequired()
        with open(self.image1, 'rb') as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item

    def goto_change_page(self):
        item = self.init_item()
        super().goto_change_page(item.id)
        return item

    def test_empty_marker_click(self):
        self.goto_add_page()
        self.inject_input_file_clicked()
        self.page.query_selector('.form-row.field-image .iuw-empty').click()
        self.assert_input_file_clicked()

    def test_required_file_input(self):
        self.goto_add_page()

        form_row = self.page.query_selector('.form-row.field-image')
        preview = form_row.query_selector('.iuw-image-preview')
        self.assertEqual(preview, None)

        file_input = form_row.query_selector('input[type=file]')
        self.assertEqual(file_input.get_attribute('value'), None)
        file_input.set_input_files(self.image1)

        preview = form_row.query_selector('.iuw-image-preview')
        img = preview.query_selector('img')
        preview_button = preview.query_selector('.iuw-preview-icon')
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertIsNotNone(preview_button)

        self.submit_form('#testrequired_form')

        self.assert_success_message()
        itens = models.TestRequired.objects.all()
        self.assertEqual(len(itens), 1)
        item = itens[0]
        self.assertIsNotNone(item.image)

    def test_image_with_database_data(self):
        item = self.goto_change_page()

        root = self.find_widget_root()
        preview = self.find_widget_preview(root)

        self.assertIsNotNone(preview)
        self.assertEqual(root.get_attribute("data-raw"), item.image.url)

        empty_marker = self.find_empty_marker(root)
        self.assertFalse(empty_marker.is_visible())
        
        img = preview.query_selector('img')
        preview_button = self.find_preview_icon(preview)
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertTrue(item.image.url in img.get_attribute('src'))
        self.assertIsNotNone(preview_button)

    def test_click_on_the_preview_image(self):
        self.goto_add_page()

        form_row = self.find_widget_form_row()
        self.assertIsNone(self.find_widget_preview(form_row))
        
        file_input = form_row.query_selector('input[type=file]')
        file_input.set_input_files(self.image2)

        self.inject_input_file_clicked()

        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)
        img = preview.query_selector('img')
        img.click()
        self.assert_input_file_clicked()
        
    def test_click_on_the_preview_button(self):
        self.goto_add_page()

        form_row = self.find_widget_form_row()
        preview = self.find_widget_preview(form_row)
        self.assertIsNone(preview)
        file_input = form_row.query_selector('input[type=file]')
        file_input.set_input_files(self.image2)
        
        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)
        preview_img = preview.query_selector('img')

        preview_button = self.find_preview_icon(preview)
        preview_button.click()
        
        self.assert_preview_modal(preview_img)

    def test_click_on_the_preview_button_and_image_on_modal(self):
        self.goto_add_page()

        form_row = self.find_widget_form_row()
        preview = self.find_widget_preview(form_row)
        self.assertIsNone(preview)
        file_input = form_row.query_selector('input[type=file]')
        file_input.set_input_files(self.image1)
        
        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)
        preview_img = preview.query_selector('img')

        preview_button = self.find_preview_icon(preview)
        preview_button.click()

        self.assert_preview_modal(preview_img)
        
    def test_click_on_the_preview_button_and_close_on_modal(self):
        self.goto_add_page()

        form_row = self.find_widget_form_row()
        preview = self.find_widget_preview(form_row)
        self.assertIsNone(preview)
        file_input = form_row.query_selector('input[type=file]')
        file_input.set_input_files(self.image1)
        
        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)
        preview_img = preview.query_selector('img')

        preview_button = self.find_preview_icon(preview)
        preview_button.click()
        
        self.assert_preview_modal(preview_img)
        self.assert_preview_modal_close()
