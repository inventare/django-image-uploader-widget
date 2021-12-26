from django import forms
from django.contrib import admin
from django.conf import settings

class ImageUploaderInline(admin.StackedInline):
    template = 'admin/edit_inline/image_uploader.html'
    extra = 0

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        return forms.Media(
            js = [
                'admin/js/image-uploader-inline%s.js' % extra
            ],
            css = {
                'screen': [
                    'admin/css/image-uploader%s.css' % extra,
                ]
            }
        )
