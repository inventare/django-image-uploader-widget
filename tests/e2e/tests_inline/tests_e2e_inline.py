from django.core.files import File
from django.test import tag

from tests.app.inline import models
from tests.e2e.inline_base import InlineBaseTestCase
from tests.utils.images import get_mock_image
from tests.utils.test_case import TestCase


@tag("new")
class InlineEditorTestCase(InlineBaseTestCase, TestCase):
    def goto_add_page(self):
        self.admin_po.navigations.goto_add_url(models.Inline)

    def goto_change_page(self):
        inline = models.Inline.objects.create()

        self.item1 = models.InlineItem()
        self.item1.parent = inline
        with open(get_mock_image("image1.png"), "rb") as f:
            self.item1.image.save("image.png", File(f))
        self.item1.save()

        self.item2 = models.InlineItem()
        self.item2.parent = inline
        with open(get_mock_image("image2.png"), "rb") as f:
            self.item2.image.save("image2.png", File(f))
        self.item2.save()

        self.admin_po.navigations.goto_change_url(inline)

        return inline

    def test_choose_files_and_save(self):
        self.assertEqual(len(models.InlineItem.objects.all()), 0)
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

        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 2)
        for item in items:
            self.assertIsNotNone(item.image)

    def test_remove_non_saved_itens(self):
        self.assertEqual(len(models.InlineItem.objects.all()), 0)
        self.goto_add_page()

        self.inline_po.execute_select_image("image1.png")
        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 1)

        thumbs[0].execute_click_on_delete()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 0)

        self.admin_po.change_form.submit_form()

        self.assertEqual(len(models.InlineItem.objects.all()), 0)

    def test_remove_saved_itens(self):
        self.goto_change_page()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)

        thumbs[0].execute_click_on_delete()
        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 1)

        thumbs[0].execute_click_on_delete()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 0)

        self.admin_po.change_form.submit_form()

        self.assertEqual(len(models.InlineItem.objects.all()), 0)

    def test_should_change_image_of_item_when_change_image_on_inline(self):
        self.goto_change_page()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)

        url1 = self.item1.image.url

        thumb = thumbs[0]
        thumb_img = thumb.page_elements.image
        thumb_src = thumb.src

        thumb.execute_select_image("image1.png")
        self.assertNotEqual(thumb_src, thumb_img.get_attribute("src"))

        self.admin_po.change_form.submit_form()

        item1 = models.InlineItem.objects.filter(pk=self.item1.pk).first()
        self.assertNotEqual(item1.image.url, url1)
