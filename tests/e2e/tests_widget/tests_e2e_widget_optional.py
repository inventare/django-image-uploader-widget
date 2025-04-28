from django.test import tag
from django.core.files import File
from tests.app.widget import models
from tests.utils.images import get_mock_image
from .base import BaseWidgetTestCase

@tag('new')
class WidgetOptionalTestCase(BaseWidgetTestCase):
    def goto_add_page(self):
        self.admin_po.navigations.goto_add_url(models.NonRequired)

    def goto_change_page(self):
        item = models.NonRequired()
        with open(get_mock_image("image2.png"), "rb") as f:
            item.image.save("image.png", File(f), False)
        item.save()
        self.admin_po.navigations.goto_change_url(item)
        return item

    def test_upload_file(self):
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_previews()), 0)
        self.assertTrue(self.widget_po.is_input_empty())

        self.widget_po.send_image_to_input("image1.png")

        previews = self.widget_po.get_visible_previews()
        preview = previews[0]
        self.assertEqual(len(previews), 1)
        self.assertTrue(self.widget_po.is_preview_valid(preview, required=False))

        self.admin_po.change_form.submit_form()

        items = models.NonRequired.objects.all()
        self.assertEqual(len(items), 1)
        self.assertIsNotNone(items[0].image)

    def test_remove_button_with_unsaved_image(self):
        self.goto_add_page()

        self.widget_po.send_image_to_input("image2.png")

        previews = self.widget_po.get_visible_previews()
        preview = previews[0]
        self.assertEqual(len(previews), 1)
        self.assertTrue(self.widget_po.is_preview_valid(preview, required=False))

        self.widget_po.click_on_preview_delete_button(preview)

        self.assertEqual(len(self.widget_po.get_visible_previews()), 0)

    def test_remove_button_with_saved_image(self):
        self.goto_change_page()

        previews = self.widget_po.get_visible_previews()
        preview = previews[0]
        self.assertEqual(len(previews), 1)
        self.assertTrue(self.widget_po.is_preview_valid(preview, required=False))
        self.assertFalse(self.widget_po.is_delete_checkbox_checked())

        self.widget_po.click_on_preview_delete_button(preview)

        self.assertEqual(len(self.widget_po.get_visible_previews()), 0)
        self.assertTrue(self.widget_po.is_delete_checkbox_checked())

        self.admin_po.change_form.submit_form()

        items = models.NonRequired.objects.all()
        self.assertEqual(len(items), 1)
        self.assertFalse(bool(items[0].image))

    def test_initialized_widget(self):
        item = self.goto_change_page()

        root = self.widget_po.page_elements.root
        previews = self.widget_po.get_visible_previews()
        preview = previews[0]
        self.assertEqual(len(previews), 1)
        self.assertTrue(self.widget_po.is_preview_valid(preview, required=False))
        self.assertEqual(root.get_attribute("data-raw"), item.image.url)
        self.assertFalse(self.widget_po.is_empty_marker_visible())

        img = preview.query_selector("img")
        self.assertTrue(item.image.url in img.get_attribute("src"))
