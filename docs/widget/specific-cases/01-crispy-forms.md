# Usage with django-crispy-forms

The `django-crispy-forms` not support, out of box, custom widgets and this is a problem of `django-crispy-forms`. Howere, inspired by [#203](https://github.com/inventare/django-image-uploader-widget/issues/203) issue, we decided to learn about the `crispy` package and document how to made custom widget work with it.

## FormHelper

The easy way to make a custom widget to work with `django-crispy-forms` is to define a `FormHelper` inside the `Form` instance:

```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms

class TestCrispyRequiredForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Div('image', template='image_uploader_widget/widget/image_uploader_widget.html'),
                    css_class='form-group col-md-6 mb-0',
                ),
                css_class='form-row'
            ),
        )

    class Meta:
        model = TestRequired
        widgets = {
            "image": ImageUploaderWidget(),
        }
        fields = "__all__"
```

The definition of the `ImageUploaderWidget()` inside the `widgets` meta property is important to render the correct media styles:

```html
{% load crispy_forms_tags %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
  {{ form.media }}
</head>
<body>

  {% crispy form %}

</body>
</html>
```

And, for the end of this article, the generated HTML should appear like this:

```html
<div class="form-row form-row">
    <div class="form-group col-md-6 mb-0">
        <!-- THE WIDGET IS RENDERED HERE! --->
        <div class="iuw-root  empty" ...>...</div>
    </div>
</div>
```

The JavaScript and Styles is inserted by `{{ form.media }}` and the `ImageUploaderWidget` should works.
