from django.core.files import File
from django.test import tag

from tests.app.widget import models
from tests.utils.images import get_mock_image

from .base import BaseWidgetTestCase


@tag("new")
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

        self.assertEqual(len(self.widget_po.get_visible_thumbnails()), 0)
        self.assertTrue(self.widget_po.is_input_empty())

        self.widget_po.execute_select_image("image1.png")

        thumbs = self.widget_po.get_visible_thumbnails()
        thumb = thumbs[0]
        self.assertEqual(len(thumbs), 1)
        self.assertTrue(thumb.is_valid(required=False))

        self.admin_po.change_form.submit_form()

        items = models.NonRequired.objects.all()
        self.assertEqual(len(items), 1)
        self.assertIsNotNone(items[0].image)

    def test_remove_button_with_unsaved_image(self):
        self.goto_add_page()

        self.widget_po.execute_select_image("image2.png")

        thumbs = self.widget_po.get_visible_thumbnails()
        thumb = thumbs[0]
        self.assertEqual(len(thumbs), 1)
        self.assertTrue(thumb.is_valid(required=False))

        thumb.execute_click_on_delete()

        self.assertEqual(len(self.widget_po.get_visible_thumbnails()), 0)

    def test_remove_button_with_saved_image(self):
        self.goto_change_page()

        thumbs = self.widget_po.get_visible_thumbnails()
        thumb = thumbs[0]
        self.assertEqual(len(thumbs), 1)
        self.assertTrue(thumb.is_valid(required=False))
        self.assertFalse(self.widget_po.is_delete_checkbox_checked())

        thumb.execute_click_on_delete()

        self.assertEqual(len(self.widget_po.get_visible_thumbnails()), 0)
        self.assertTrue(self.widget_po.is_delete_checkbox_checked())

        self.admin_po.change_form.submit_form()

        items = models.NonRequired.objects.all()
        self.assertEqual(len(items), 1)
        self.assertFalse(bool(items[0].image))

    def test_initialized_widget(self):
        item = self.goto_change_page()

        thumbs = self.widget_po.get_visible_thumbnails()
        thumb = thumbs[0]
        self.assertEqual(len(thumbs), 1)
        self.assertTrue(thumb.is_valid(required=False))
        self.assertEqual(self.widget_po.data_raw, item.image.url)
        self.assertFalse(self.widget_po.is_empty_marker_visible())

        self.assertTrue(item.image.url in thumb.src)
