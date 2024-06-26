# Getting started

The **django-image-uploader-widget** is a widget to **django**, specially **django-admin** to handle better image uploads with a modern and beautiful user interface.

## Features

Some of the features of this widget is:

- Beautiful user interface.
- Handle drop files from your file manager.
- Handle select file by click in the widget or by droping the image (previous item).
- Inline editor provided to work with multiple images.
- Modal to view the full image (The images are adjusted as cover in the preview box, then, in some cases, that is very useful).

<div class="images-container" markdown="block">

![Drag and Drop Image](./images/beautiful.gif){ loading=lazy }

</div>

<div class="images-container" markdown="block">

![Select by click](./images/click.gif){ loading=lazy }

</div>

<div class="images-container" markdown="block">

![Inline handle](./images/inline_multiple.gif){ loading=lazy }

</div>

## Getting Started

To get started, install this plugin with the pip package manager:

```sh
pip install django-image-uploader-widget
```

then, go to the `settings.py` file and add the `image_uploader_widget` to the installed apps:

```python
INSTALLED_APPS = [
    'my_app.apps.MyAppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'image_uploader_widget',
]
```

## Using

Now, you must be able to use the widget in your forms:

```python
# forms.py
from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget

class ExampleForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageUploaderWidget(),
        }
        fields = '__all__'
```

## Code Example

For code direct examples, check the `image_uploader_widget_demo` folder in the Github [repository](https://github.com/inventare/django-image-uploader-widget).

