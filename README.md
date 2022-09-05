# django-image-uploader-widget

A beautiful image uploader widget for django/django-admin.

![Beautiful image uploader widget](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/beautiful.gif)

![Multiple behaviours](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/click.gif)

![Multiple files handling](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/static/img/inline_multiple.gif)

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

##  Usage

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
