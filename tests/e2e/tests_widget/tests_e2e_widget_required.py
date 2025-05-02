from django.core.files import File
from django.test import tag

from tests.app.widget import models
from tests.utils.images import get_mock_image
from tests.utils.test_case import TestCase

from .base import BaseWidgetTestCase


@tag("new")
class WidgetRequiredTestCase(BaseWidgetTestCase, TestCase):
    def goto_add_page(self):
        self.admin_po.navigations.goto_add_url(models.Required)

    def test_upload_file(self):
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_thumbnails()), 0)
        self.assertTrue(self.widget_po.is_input_empty())

        self.widget_po.execute_select_image("image1.png")

        thumbs = self.widget_po.get_visible_thumbnails()
        thumb = thumbs[0]
        self.assertEqual(len(thumbs), 1)
        self.assertTrue(thumb.is_valid(required=True))

        self.admin_po.change_form.submit_form()

        items = models.Required.objects.all()
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertIsNotNone(item.image)

    def test_initialized_widget(self):
        item = models.Required()
        with open(get_mock_image("image1.png"), "rb") as f:
            item.image.save("image.png", File(f), False)
        item.save()

        self.admin_po.navigations.goto_change_url(item)

        self.assertFalse(self.widget_po.is_empty_marker_visible())
        thumbs = self.widget_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 1)

        thumb = thumbs[0]
        self.assertTrue(thumb.is_valid(required=True))
        self.assertEqual(self.widget_po.data_raw, item.image.url)
        self.assertTrue(item.image.url in thumb.src)
