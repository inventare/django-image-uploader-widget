# Use ImageListField to store Multiple Images

!!! warning "Version Information"

    Introduced at the 0.5.0 version.

!!! warning "Database Information"

    Supported only on PostgreSQL Database's.

The `widget` only supports ImageField and this is a limitation to upload only one image per widget. The `inline admin` support multiple images upload but it is only supported by the `django.contrib.admin` pages.

Some comments, like the [Discussion #97](https://github.com/inventare/django-image-uploader-widget/discussions/97), [Issue #146](https://github.com/inventare/django-image-uploader-widget/issues/146) and [Issue #110](https://github.com/inventare/django-image-uploader-widget/issues/110) make some feature requests and the Issue #146 takes one proposition: uses the `ArrayField`. The `ArrayField` is a `PostgreSQL` specific field and support for storing multiple values into one field.

## Experimental for Now?

Currently, we have added support, addaptating the `inline admin` feature to work widget-like and add support for the `ArrayField` to store images using the `storage` and save it path to an `ArrayField`. This is, really, a little experimental for now, and can contains some bugs. If your found one: open a Issue reporting.

!!! warning "Attention Point"

    See the attention point on the [Prevent Raw Images Path Change](./prevent-raw-change.md) page.

## Usage

Instead of `widget` or `inline admin` that we only set the `widget` and `inline admin` for the created model, in this part, we need to customize the model.

```python
from django.db import models
from image_uploader_widget.postgres import ImageListField

class TestWithArrayField(models.Model):
    images = ImageListField(blank=True, null=True, upload_to="admin_test")

    class Meta:
        verbose_name = "Test With Array Field"
```

This is really simple and is not needed to create more customizations. The widget and form is automatic created for the custom multiple images widget.
