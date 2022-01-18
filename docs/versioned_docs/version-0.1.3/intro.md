---
sidebar_position: 1
---

# Introduction

The **django-image-uploader-widget** is a widget to **django**, specially **django-admin** to handle better image uploads with a modern and beautiful user interface.

## Features

Some of the features of this widget is:

- Beautiful user interface.
- Handle drop files from your file manager.
- Handle select file by click in the widget or by droping the image (previous item).
- Inline editor provided to work with multiple images.
- Modal to view the full image (The images are adjusted as cover in the preview box, then, in some cases, that is very useful).

![Drag and Drop Image](/img/beautiful.gif)

![Select by click](/img/click.gif)

![Inline handle](/img/inline_multiple.gif)

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

## Advanced Use Cases

Better writed widget use cases and more effective examples is comming. Other examples with the inline is comming. For now, check the `image_uploader_widget_demo` folder in the Github [repository](https://github.com/inventare/django-image-uploader-widget).
