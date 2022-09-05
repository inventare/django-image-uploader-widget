from django import forms
from django.contrib import admin

class ImageUploaderInline(admin.StackedInline):
    template = 'admin/edit_inline/image_uploader.html'
    extra = 0

    @property
    def media(self):
        return forms.Media(
            js = [
                'admin/js/image-uploader-modal.js',
                'admin/js/image-uploader-inline.js',
            ],
            css = {
                'screen': [
                    'admin/css/image-uploader-inline.css',
                ]
            }
        )
