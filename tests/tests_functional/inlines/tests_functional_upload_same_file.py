from django.core.files import File
from django.test import tag

from tests import models, test_case


@tag("functional", "inline", "functional_inline")
class InlineUploadSameFileEditorTests(test_case.IUWTestCase):
    model = "inline"

    def init_item(self, only_one=False):
        inline = models.Inline.objects.create()

        self.item1 = models.InlineItem()
        self.item1.parent = inline
        with open(self.image1, "rb") as f:
            self.item1.image.save("image.png", File(f))
        self.item1.save()

        if not only_one:
            self.item2 = models.InlineItem()
            self.item2.parent = inline
            with open(self.image2, "rb") as f:
                self.item2.image.save("image2.png", File(f))
            self.item2.save()

        return inline

    def goto_change_page(self, only_one=False):
        item = self.init_item(only_one)
        super().goto_change_page(item.id)
        return item

    def test_should_remove_and_upload_same_image(self):
        self.assertEqual(len(models.InlineItem.objects.all()), 0)
        self.goto_add_page()

        root = self.find_inline_root()
        temp_file = root.query_selector(".temp_file")
        temp_file.set_input_files(self.image1)

        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        self.find_delete_icon(previews[0]).click()
        self.assertEqual(len(self.find_inline_previews(root)), 0)

        temp_file.set_input_files(self.image1)
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)
