---
sidebar_position: 1
---

# Tutorial

First, we need of some context: the image uploader inline is an inline admin editor (like the [StackedInline](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.StackedInline) or the [TabularInline](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.TabularInline) of the original django). This inline editor is created to make an multiple images manager widget using an model with an image field.

## Creating a django project

First, create a project folder. Here we call it as `my-ecommerce`:

```bash
mkdir my-ecommerce
cd my-ecommerce
```

And, now, create a django project in this folder:

```bash
django-admin startproject core .
```

And, then, we have the folder structure:

```
| - my-ecommerce
  | - core
    | - asgi.py
    | - __init__.py
    | - settings.py
    | - urls.py
    | - wsgi.py
  | - manage.py
```

Create our **django** application by running the command:

```
python manage.py startapp ecommerce
```

And, now, we have a new, and more complex, folder structure:

```
| - my-ecommerce
  | - core
    | - asgi.py
    | - __init__.py
    | - settings.py
    | - urls.py
    | - wsgi.py
  | - ecommerce
    | - migrations
      | - __init__.py
    | - admin.py
    | - apps.py
    | - __init__.py
    | - models.py
    | - tests.py
    | - views.py
  | - manage.py
```

## Installing the widget

To install the widget, is possible to use the same instructions of the [Introduction](../intro.md), and the first step is to install the package with pip:

```bash
pip install django-image-uploader-widget
```

then, add it to the `INSTALLED_APPS` on the `settings.py`, in the case of this example: `core/settings.py` file. To understand better the Applications, see the django documentation: [Applications](https://docs.djangoproject.com/en/3.2/ref/applications/).

```python
# core/settings.py
# ...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'image_uploader_widget',
]

# ...
```

### Warning

**Observation**: note that the application name to be added on the `INSTALLED_APPS` are not equals to the pip package name / install name.

## Using the inline editor

This inline editor is created to be used directly with the django-admin interface. To show how to use it, go to create two basic models inside the `ecommerce` app (Add your app, `ecommerce` in my case, at `INSTALLED_APPS` is recommended):

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

    def __str__(self):
        return str(self.image)
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
```

Now, inside our admin, we can create an primary ModelAdmin for the product:

```python
# ecommerce/admin.py
from django.contrib import admin
from ecommerce.models import Product, ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
```

And, now, we can define our inline widget:

```python
# ecommerce/admin.py
from django.contrib import admin
from ecommerce.models import Product, ProductImage
from image_uploader_widget.admin import ImageUploaderInline

class ProductImageAdmin(ImageUploaderInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
```

And we got the inline editor working as well:

![Image Uploader Widget](/img/tutorials/admin_demo.png)
