---
sidebar_position: 2
---

# Resumed

If you is an advanced user, only install the package:

```bash
pip install django-image-uploader-widget
```

and add the `image_uploader_widget` to the `INSTALLED_APPS` in the `settings.py`:

```python
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

And go to use it with your forms:


```python
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

![Image Uploader Widget](/img/tutorials/form_demo.png)
