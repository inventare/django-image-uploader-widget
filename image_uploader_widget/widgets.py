from django import forms
from django.forms import widgets

class ImageUploaderWidget(widgets.ClearableFileInput):
    template_name = 'admin/widgets/image_uploader_widget.html'

    @property
    def media(self):
        return forms.Media(
            js=(
                'admin/js/image-uploader-modal.js',
                'admin/js/image-uploader-widget.js',
            ),
            css={
                'screen': (
                    'admin/css/image-uploader-widget.css',
                ),
            },
        )
