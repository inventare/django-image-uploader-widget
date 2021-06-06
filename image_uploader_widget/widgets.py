from django import forms
from django.forms import widgets
from django.conf import settings

class ImageUploaderWidget(widgets.ClearableFileInput):
    template_name = 'widgets/image_uploader_widget.html'
    non_file_text = ''

    def __init__(self, non_file_text = 'Click here to select a file!', attrs = None):
        super(ImageUploaderWidget, self).__init__(attrs)
        self.non_file_text = non_file_text

    def get_context(self, name, value, attrs):
        context = super(ImageUploaderWidget, self).get_context(name, value, attrs)
        context['widget']['non_file_text'] = self.non_file_text
        return context

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        return forms.Media(
            js=(
                'admin/js/vendor/jquery/jquery%s.js' % extra,
                'admin/js/jquery.init.js',
                'widgets/image_uploader_widget.js',
            ),
            css={
                'screen': (
                    'widgets/image_uploader_widget.css',
                ),
            },
        )
