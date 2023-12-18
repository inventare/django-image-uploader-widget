---
sidebar_position: 2
---

# Ordered Images Admin

:::success Versioning
Introduced at the 0.4.1 version.
:::

The first thing needed to understand the ordered version of the `ImageUploaderInline` is read the [inline tutorial](./tutorial.md). This page has a documentation of how to extend the `ImageUploaderInline` with order field to allow to reorder, by clicking and dragging, the images inside the inline.

![Behaviour of drag and drop reorder](/img/behaviour_reorder.gif)

## Adding Order Field to Model

Add a `PositiveIntegerField` to the model to store the order of the images inside the admin.

```python
# ecommerce/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField("image")
    order = models.PositiveIntegerField('Order', default=1)

    def __str__(self):
        return str(self.image)
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
```

## Change inline to OrderedImageUploaderInline

Inside the `admin.py`, change the inline from `ImageUploaderInline` to `OrderedImageUploaderInline` and setup some configs:

```python
# ecommerce/admin.py
from django.contrib import admin
from ecommerce.models import Product, ProductImage
from image_uploader_widget.admin import ImageUploaderInline

class ProductImageAdmin(OrderedImageUploaderInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

```

## Attributes

| Attribute   | Type  | Default Value | Description                                                                 |
| ----------- | ----- | ------------- | --------------------------------------------------------------------------- |
| order_field | `str` | `"order"`     | The name of field that represents the order of images.                      |
| template    | `str` | `"admin/edit_inline/ordered_image_uploader.html"` | The template path to render the widget. |

All the attributes from the `ImageUploaderInline` are present too. For example, is possible to change the name of the used `order_field` by adding it's attribute to the `OrderedImageUploaderInline`:

```python
from image_uploader_widget.admin import ImageUploaderInline

class MyInlineAdminAdmin(OrderedImageUploaderInline):
    model = MyModel
    order_field = "my_custom_field"

```
