from django.contrib import admin
from image_uploader_widget.admin import ImageUploaderInline

from . import models
from . import forms

class ExampleModelImageAdmin(ImageUploaderInline):
    model = models.ExampleModelImage
    fields = ['image']

class AnotherModalImagesExampleAdmin(ImageUploaderInline):
    model = models.AnotherModalImagesExample
    fields = ['image']

class ExampleAdmin(admin.ModelAdmin):
    form = forms.ExampleForm
    inlines = [
        ExampleModelImageAdmin,
        AnotherModalImagesExampleAdmin
    ]

admin.site.register(models.ExampleModel, ExampleAdmin)
