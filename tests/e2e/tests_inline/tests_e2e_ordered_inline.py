from django.core.files import File
from django.test import tag

from tests.app.inline import models
from tests.e2e.base import BaseReorderTests
from tests.pom.component import InlinePO
from tests.utils.images import get_mock_image
from tests.utils.test_case import TestCase


class OrderedInlineEditorTestCase(BaseReorderTests, TestCase):
    def setUp(self):
        super().setUp()
        self.inline_po = InlinePO(self.page)

    def goto_add_page(self):
        self.admin_po.navigations.goto_add_url(models.OrderedInline)

    def goto_change_page(self):
        inline = models.OrderedInline.objects.create()

        self.item1 = models.OrderedInlineItem()
        self.item1.parent = inline
        self.item1.order = 1
        with open(get_mock_image("image1.png"), "rb") as f:
            self.item1.image.save("image.png", File(f))
        self.item1.save()

        self.item2 = models.OrderedInlineItem()
        self.item2.parent = inline
        self.item2.order = 2
        with open(get_mock_image("image2.png"), "rb") as f:
            self.item2.image.save("image2.png", File(f))
        self.item2.save()

        self.admin_po.navigations.goto_change_url(inline)

        return inline

    def get_images_to_validate(self):
        instance = models.OrderedInline.objects.order_by("id").last()
        data = models.OrderedInlineItem.objects.order_by("order").filter(
            parent=instance
        )
        return [x.image.url for x in data]
