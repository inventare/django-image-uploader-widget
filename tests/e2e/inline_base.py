from django.test import tag
from tests.utils.test_case import TestCase
from tests.app.inline import models
from tests.pom.widget_inline import WidgetInlinePO

@tag("new")
class InlineBaseTestCase(TestCase):
    def test_upload_same_file_delete_reupload(self):
        self.admin_po.navigations.goto_add_url(models.Inline)

        inline_po = WidgetInlinePO(self.page)
        inline_po.choice_image("image1.png")

        previews = inline_po.get_visible_previews()
        self.assertEqual(len(previews), 1)

        inline_po.click_on_preview_delete(previews[0])

        previews = inline_po.get_visible_previews()
        self.assertEqual(len(previews), 0)

        inline_po.choice_image("image1.png")
        previews = inline_po.get_visible_previews()
        self.assertEqual(len(previews), 1)

    def test_upload_same_file_two_times(self):
        self.admin_po.navigations.goto_add_url(models.Inline)

        inline_po = WidgetInlinePO(self.page)
        inline_po.choice_image("image1.png")

        previews = inline_po.get_visible_previews()
        self.assertEqual(len(previews), 1)

        inline_po.choice_image("image1.png")
        previews = inline_po.get_visible_previews()
        self.assertEqual(len(previews), 2)

