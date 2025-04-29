from django.test import tag
from django.core.files import File
from tests.utils.images import get_mock_image
from tests.e2e.inline_base import InlineBaseTestCase
from tests.app.inline import models

@tag("new")
class InlineEditorTestCase(InlineBaseTestCase):
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
