# Max number of images

!!! warning "Version Information"

    Introduced at the 1.1.0 version.

!!! warning "Database Information"

    Supported only on PostgreSQL Database's.

We introduced a `kwarg` called `max_images` on `ImageListField` field to limit the number of images that user can choose by picker. The default value is `1000` (only because this value are, previous, hardcoded value on the html template). The usage is:

```python
from django.db import models
from image_uploader_widget.postgres import ImageListField

class TestWithArrayField(models.Model):
    images = ImageListField(blank=True, null=True, max_images=2, upload_to="admin_test")

    class Meta:
        verbose_name = "Test With Array Field"
```

!!! warning "Validation"

    The limit, for now, is only on front-end widget. If you want to validate in server-side, do it by yourself for now.
