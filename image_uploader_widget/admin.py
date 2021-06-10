from django import forms
from django.contrib import admin
from django.conf import settings

class ImageUploaderInline(admin.StackedInline):
    template = 'admin/edit_inline/image_uploader.html'
    extra = 0

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        js = ['vendor/jquery/jquery%s.js' % extra, 'jquery.init.js', 'image_uploader_inline.js']
        return forms.Media(
            js=['admin/js/%s' % url for url in js],
            css={ 'screen': ['widgets/image_uploader_widget.css'] }
        )
