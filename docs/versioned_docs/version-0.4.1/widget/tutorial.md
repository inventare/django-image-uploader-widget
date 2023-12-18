---
sidebar_position: 1
---

# Tutorial

First, we need of some context: the image uploader widget is a widget to handle image uploading with a beautiful interface with click to select file and a drop file behaviour handler. It is used with django forms.

This is a more long and for newbies tutorial of how to use this widget. If you is an advanced user, see the [Resumed](./resumed.md) version.

To write this tutorial of this documentation we go to create an empty django project, then if you don't want to see this part, skip to [using the widget section](#installing-the-widget). Another information is: we're assuming you already know the basics of **django** and already have it installed in your machine.

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

## Using the widget

We have two basic modes to use this widget:

1. creating a ORM `Model` and using an `ModelForm` to it setting the widget.

2. creating an custom `Form` with any other behaviour.

### With ModelForm

First, go to our ecommerce app models `ecommerce/models.py` and create a basic django model with an `ImageField`:

```python
# ecommerce/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
```

Now, we go to create our `ModelForm`. Create a empty file on `ecommerce/forms.py` to store our django forms. And create our own `ProductForm`:

```python
# ecommerce/forms.py
from django.forms import ModelForm
from ecommerce.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image']
```

And, here, we can declare the widget that our `image` field uses:

```python
# ecommerce/forms.py
from django.forms import ModelForm
from ecommerce.models import Product
from image_uploader_widget.widgets import ImageUploaderWidget

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image']
        widgets = {
            'image': ImageUploaderWidget()
        }
```

#### Creating and applying migrations

Our Model, declared in the above section, needs to be inserted on our database using the [migrations](https://docs.djangoproject.com/en/3.2/topics/migrations/). To create our migrations, we need to add our `ecommerce` app to `INSTALLED_APPS` on the `settings.py`:

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
    'ecommerce',
]

# ...
```

Now, we go to create the migrations using the command:

```bash
python manage.py makemigrations
```

If you found an `ecommerce.Product.image: (fields.E210) Cannot use ImageField because Pillow is not installed.` error, just run an:

```bash
pip install Pillow
```

and re-run the makemigrations command. Now, we go to apply the migrations with:

```bash
python manage.py migrate
```

And, now, we can run the development server to see our next steps coding:

```bash
python manage.py runserver
```

#### See it in the action

To see the widget in action, just go to the ecommerce app and create, in the `views.py`, an view that renders an form:

```python
# ecommerce/views.py
from django.shortcuts import render
from ecommerce.forms import ProductForm

def test_widget(request):
    context = { 'form': ProductForm() }
    return render(request, 'test_widget.html', context)
```

Now, we can create an `templates` folder in the `ecommerce` application and inside it we need to create a `test_widget.html`:

```html
<!-- ecommerce/templates/test_widget.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    {{ form.media }}
</head>
<body>

    {{ form.as_p }}
    
</body>
</html>
```

And register this view in the `core/urls.py`:

```python
# core/urls.py
from django.contrib import admin
from django.urls import path
from ecommerce.views import test_widget

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test_widget/', test_widget),
]
```

And go to the browser in `http://localhost:8000/test_widget/` and see the result:

![Image Uploader Widget](/img/tutorials/form_demo.png)


### With Form and custom behaviour

It's very like the above item and we need only to change some things in the `forms.py`:

```python
from django import forms
from ecommerce.models import Product
from image_uploader_widget.widgets import ImageUploaderWidget

class ProductForm(forms.Form):
    image = forms.ImageField(widget=ImageUploaderWidget())

    class Meta:
        fields = ['image']
```

And we not need to change nothing more. It works.

### Comments about using with django-admin

The use with **django-admin** is very like it: we only needs to create `ModelForm` for our models and in the `ModelAdmin` ([django documentation](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin)) we set our form ([here is an example](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form)).
