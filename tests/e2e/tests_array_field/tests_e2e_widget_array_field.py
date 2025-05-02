import uuid

from django.core.files import File
from django.test import tag

from tests.app.array_field import models
from tests.e2e.base import BaseReorderTests
from tests.e2e.inline_base import InlineBaseTestCase
from tests.utils.images import get_mock_image
from tests.utils.test_case import TestCase


@tag("new")
class ArrayFieldTestCase(BaseReorderTests, InlineBaseTestCase, TestCase):
    def goto_add_page(self):
        self.admin_po.navigations.goto_add_url(models.TestWithArrayField)

    def goto_change_page(self):
        images = []

        instance = None
        with open(get_mock_image("image1.png"), "rb") as f1:
            self.image1_name = f"{uuid.uuid4()}.png"
            images = [*images, File(f1, self.image1_name)]

            with open(get_mock_image("image2.png"), "rb") as f2:
                self.image2_name = f"{uuid.uuid4()}.png"
                images = [*images, File(f2, self.image2_name)]

                instance = models.TestWithArrayField.objects.create(images=images)

        self.admin_po.navigations.goto_change_url(instance)

        return instance

    def get_images_to_validate(self):
        instance = models.TestWithArrayField.objects.order_by("id").last()
        return instance.images

    def test_choose_files_and_save(self):
        self.assertEqual(len(models.TestWithArrayField.objects.all()), 0)
        self.goto_add_page()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 0)

        self.inline_po.execute_select_image("image1.png")
        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 1)

        self.inline_po.execute_select_image("image2.png")
        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)

        for thumb in thumbs:
            self.assertTrue(thumb.is_valid(required=False))

        self.admin_po.change_form.submit_form()

        item = models.TestWithArrayField.objects.first()
        self.assertIsNotNone(item)
        self.assertEqual(len(item.images), 2)
        for url in item.images:
            self.assertIsNotNone(url)

    def test_remove_unsaved_image(self):
        self.assertEqual(len(models.TestWithArrayField.objects.all()), 0)
        self.goto_add_page()

        self.inline_po.execute_select_image("image1.png")

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 1)

        thumbs[0].execute_click_on_delete()
        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 0)

        self.admin_po.change_form.submit_form()

        item = models.TestWithArrayField.objects.first()
        self.assertIsNotNone(item)
        self.assertEqual(len(item.images), 0)

    def test_remove_saved_images(self):
        item = self.goto_change_page()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)

        thumbs[0].execute_click_on_delete()
        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 1)
        thumbs[0].execute_click_on_delete()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 0)

        self.admin_po.change_form.submit_form()

        item = models.TestWithArrayField.objects.get(pk=item.pk)
        self.assertEqual(len(item.images), 0)

    def test_change_saved_image(self):
        item = self.goto_change_page()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)

        url1 = item.images[0]
        thumb = thumbs[0]
        thumb_img = thumb.page_elements.image
        thumb_src = thumb.src

        thumb.execute_select_image("image1.png")

        self.assertNotEqual(thumb_src, thumb_img.get_attribute("src"))

        self.admin_po.change_form.submit_form()

        item = models.TestWithArrayField.objects.get(pk=item.pk)
        self.assertNotEqual(item.images[0], url1)
