from django import forms
from django.forms import widgets

class ImageUploaderWidget(widgets.ClearableFileInput):
    template_name = 'admin/widgets/image_uploader_widget.html'

    def __init__(self, attrs = None):
        super(ImageUploaderWidget, self).__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super(ImageUploaderWidget, self).get_context(name, value, attrs)
        return context

    @property
    def media(self):
        return forms.Media(
            js=(
                'admin/js/image-uploader-widget.js'
            ),
            css={
                'screen': (
                    'admin/css/image-uploader-widget.css'
                ),
            },
        )
