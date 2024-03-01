import json
from typing import Any
from django import forms
from django.contrib.postgres.forms import SplitArrayWidget
from django.core.files.storage import default_storage

class ImageUploaderArrayWidget(SplitArrayWidget):
    template_name = "postgres/widgets/image_array.html"
    drop_text = ""
    empty_text = ""
    empty_icon = ""
    drop_icon = ""

    def get_drop_text(self):
        return self.drop_text
    
    def get_empty_text(self):
        return self.empty_text

    def get_empty_icon(self):
        return self.empty_icon
    
    def get_drop_icon(self):
        return self.drop_icon

    def __init__(
        self,
        drop_text = "",
        empty_text = "",
        empty_icon = "",
        drop_icon = "",
        **kwargs
    ):
        self.drop_text = drop_text
        self.empty_text = empty_text
        self.empty_icon = empty_icon
        self.drop_icon = drop_icon

        widget = forms.ClearableFileInput()
        super().__init__(widget, 0, **kwargs)

    def _get_image(self, path):
        return default_storage.url(path)

    def get_files_from_value(self, value: Any) -> str | None:
        value = super().format_value(value)
        if isinstance(value, str):
            splited = value.split(',')
            return [self._get_image(name) for name in splited]
        return value

    def get_context(self, name, value, attrs = None):
        value = self.get_files_from_value(value)
        value = value or []
        self.size = len(value)
        
        context = super(ImageUploaderArrayWidget, self).get_context(name, value, attrs)
        if not context:
            context = {}

        for i in range(0, len(value)):
            context['widget']['subwidgets'][i]['value'] = value[i]

        print(context)

        return {
            **context,
            'inline_admin_formset': {
                'inline_formset_data': json.dumps({
                    'name': context['widget']['name'],
                    'options': {
                        'prefix': context['widget']['name'],
                    }
                }),
                'formset': {
                    'prefix': context['widget']['name'],
                },
            },
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
                'admin/js/image-uploader-inline.js',
            ),
            css={
                'screen': (
                    'admin/css/image-uploader-inline.css',
                ),
            },
        )