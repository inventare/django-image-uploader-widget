# Text And Icons

To customize the image uploader widget or inline you can set some variables (this feature is based on the issue [#77](https://github.com/inventare/django-image-uploader-widget/issues/77)). In this page we talk about how to, easy, change the texts and icons on that lib.


## Widget

For the widget, to customize the icon and the text we need to set some variables in the `ImageUploaderWidget` constructor, like it:

```python
# ...
class TestCustomForm(forms.ModelForm):
    class Meta:
        model = CustomWidget
        widgets = {
            'image': ImageUploaderWidget(
                drop_icon="<svg ...></svg>",
                drop_text="Custom Drop Text",
                empty_icon="<svg ...></svg>",
                empty_text="Custom Empty Marker Text",
            ),
        }
        fields = '__all__'
```

In this example, we set all four properties (`drop_icon`, `drop_text`, `empty_icon` and `empty_text`) for the widget. In the icons is possible to use the `django.shortcuts.render` ([REF](https://docs.djangoproject.com/en/4.1/topics/http/shortcuts/#render)) to renderize the icon from an HTML template.

Another way for customize it is create an new widget class based on that and use it for your forms:

```python
class MyCustomWidget(ImageUploaderWidget):
    drop_text = ""
    empty_text = ""

    def get_empty_icon(self):
        return render(...)
    
    def get_drop_icon(self):
        return render(...)

class TestCustomForm(forms.ModelForm):
    class Meta:
        model = CustomWidget
        widgets = {
            'image': MyCustomWidget()
        }
        fields = '__all__'
```

## Inline Editor

To customize the text and the icons of the inline editor is a little bit faster too. We can set some variables on the `InlineAdmin` of your model, like this:

```python
class CustomInlineEditor(ImageUploaderInline):
    model = models.CustomInlineItem
    add_image_text = "add_image_text"
    drop_text = "drop_text"
    empty_text = "empty_text"

    def get_empty_icon(self):
        return render(...)

    def get_add_icon(self):
        return render(...)

    def get_drop_icon(self):
        return render(...)

@admin.register(models.CustomInline)
class CustomInlineAdmin(admin.ModelAdmin):
    inlines = [CustomInlineEditor]
```
