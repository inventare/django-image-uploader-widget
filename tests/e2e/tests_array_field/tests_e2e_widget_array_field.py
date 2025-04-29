import uuid
from django.test import tag
from django.core.files import File
from tests.utils.images import get_mock_image
from tests.app.array_field import models
from tests.e2e.inline_base import InlineBaseTestCase

@tag("new")
class ArrayFieldTestCase(InlineBaseTestCase):
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
