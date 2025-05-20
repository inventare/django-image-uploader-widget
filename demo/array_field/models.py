from django.db import models

from image_uploader_widget.postgres.fields import ImageListField


class TestWithArrayField(models.Model):
    images = ImageListField(blank=True, null=True, max_images=2, upload_to="admin_test")

    class Meta:
        verbose_name = "(Array Field) Default"
