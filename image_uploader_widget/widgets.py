from django import forms
from django.forms import widgets

class ImageUploaderWidget(widgets.ClearableFileInput):
    template_name = 'admin/widgets/image_uploader_widget.html'
    drop_text = ""
    empty_text = ""
    empty_icon = ""
    drop_icon = ""

    def __init__(self, drop_text = "", empty_text = "",
        empty_icon = "", drop_icon = "", attrs = None):
        self.drop_text = drop_text
        self.empty_text = empty_text
        self.empty_icon = empty_icon
        self.drop_icon = drop_icon
        super(ImageUploaderWidget, self).__init__(attrs)

    def get_drop_text(self):
        return self.drop_text
    
    def get_empty_text(self):
        return self.empty_text

    def get_empty_icon(self):
        return self.empty_icon
    
    def get_drop_icon(self):
        return self.drop_icon

    def get_context(self, name, value, attrs = None):
        context = super(ImageUploaderWidget, self).get_context(name, value, attrs)
        if not context:
            context = {}
        
        return {
            **context,
            "custom": {
                "drop_text": self.get_drop_text(),
                "empty_text": self.get_empty_text(),
                "empty_icon": self.get_empty_icon(),
                "drop_icon": self.get_drop_icon(),
            }
        }

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
