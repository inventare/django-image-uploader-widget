# django-image-uploader-widget

## Introduction

A beautiful image uploader widget for **django** and **django-admin**.

### Basic Preview

![Widget-Dark](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/widget_dark.png#gh-dark-mode-only)![Widget-Light](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/widget_light.png#gh-light-mode-only)

![Widget-Dark-Image](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/widget_dark_image.png#gh-dark-mode-only)![Widget-Light-Image](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/widget_light_image.png#gh-light-mode-only)

### Widget Behaviour

![Behaviour-Dark](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/behaviour_dark.gif#gh-dark-mode-only)![Behaviour-Light](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/behaviour_light.gif#gh-light-mode-only)

### Theme Toggle With Django 4.2+

![Theme-Toggle](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/behaviour_theme_toggle.gif)

### Django-Admin Inline Widget for Multiple Files Handling

![Admin-Behaviour-Dark](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/behaviour_inline_dark.gif#gh-dark-mode-only)![Admin-Behaviour-Light](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/behaviour_inline_light.gif#gh-light-mode-only)

## Documentation

To understand this package and how to use it you can access the package [documentation](https://inventare.github.io/django-image-uploader-widget/).

## Installing

Install via pip package manager:

```bash
pip install django-image-uploader-widget
```

Add to installed apps, in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'image_uploader_widget',
    # ...
]
```

##  Usage

### With Admin

```python
# admin.py
from django.contrib import admin
from django.db import models
from image_uploader_widget.widgets import ImageUploaderWidget
from .models import YourModel


@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }
```

### With ModelForm

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
