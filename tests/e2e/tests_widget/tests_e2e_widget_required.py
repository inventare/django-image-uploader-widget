from django.test import tag
from django.core.files import File
from tests.utils.assert_input_file_clicked import assert_input_file_clicked
from tests.app.widget import models
from tests.utils.images import get_mock_image
from .base import BaseWidgetTestCase

@tag('new')
class WidgetRequiredTestCase(BaseWidgetTestCase):
    def goto_add_page(self):
        self.admin_po.navigations.goto_add_url(models.Required)

    def test_upload_file(self):
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_previews()), 0)
        self.assertTrue(self.widget_po.is_input_empty())

        self.widget_po.send_image_to_input("image1.png")

        previews = self.widget_po.get_visible_previews()
        preview = previews[0]
        self.assertEqual(len(previews), 1)
        self.assertTrue(self.widget_po.is_preview_valid(preview, required=True))

        self.admin_po.change_form.submit_form()

        items = models.Required.objects.all()
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertIsNotNone(item.image)

    def test_initialized_widget(self):
        """
        should widget correctly initialized when open the page to edit.
        """
        item = models.Required()
        with open(get_mock_image("image1.png"), "rb") as f:
            item.image.save("image.png", File(f), False)
        item.save()

        self.admin_po.navigations.goto_change_url(item)

        root = self.widget_po.page_elements.root
        previews = self.widget_po.get_visible_previews()
        preview = previews[0]
        self.assertEqual(len(previews), 1)
        self.assertTrue(self.widget_po.is_preview_valid(preview, required=True))
        self.assertEqual(root.get_attribute("data-raw"), item.image.url)
        self.assertFalse(self.widget_po.is_empty_marker_visible())

        img = preview.query_selector("img")
        self.assertTrue(item.image.url in img.get_attribute("src"))
