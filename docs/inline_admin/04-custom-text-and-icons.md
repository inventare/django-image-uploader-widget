# Custom Text and Icons

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
