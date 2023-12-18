---
sidebar_position: 3
---

# Accept Input Attribute

When working with **HTML** `<input />` element, we have an `accept=""` attribute that works defining the visible file types into the file picker dialog. An better, and complete, description of this attribute can be found at [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/accept).

To define this attribute, with the `ImageUploaderWidget`, we can set the `attrs` property when instantiate the `ImageUploaderWidget`, like:

```python
from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget
from .models import CustomWidget

class TestForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageUploaderWidget(attrs={ 'accept': 'image/png' }),
        }
        fields = '__all__'
```
