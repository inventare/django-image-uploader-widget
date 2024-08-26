import json
from typing import Any, List

from django import forms
from django.contrib.postgres.forms import SplitArrayWidget
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile


class ImageUploaderArrayWidget(SplitArrayWidget):
    template_name = "image_uploader_widget/postgres/image_array.html"
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
        self, drop_text="", empty_text="", empty_icon="", drop_icon="", **kwargs
    ):
        self.drop_text = drop_text
        self.empty_text = empty_text
        self.empty_icon = empty_icon
        self.drop_icon = drop_icon

        widget = forms.ClearableFileInput()
        super().__init__(widget, 0, **kwargs)

    def _get_image(self, path):
        if isinstance(path, InMemoryUploadedFile):
            return None
        return default_storage.url(path)

    def get_files_from_value(self, value: Any) -> List[str]:
        return [self._get_image(name) for name in value]

    def get_context(self, name, value, attrs=None):
        value_raw = value or []
        value = list(filter(None, self.get_files_from_value([*value_raw])))
        self.size = len(value)

        context = super(ImageUploaderArrayWidget, self).get_context(name, value, attrs)
        if not context:
            context = {}

        for i in range(0, len(value)):
            context["widget"]["subwidgets"][i]["value"] = value[i]
            context["widget"]["subwidgets"][i]["value_raw"] = value_raw[i]

        return {
            **context,
            "inline_admin_formset": {
                "inline_formset_data": json.dumps(
                    {
                        "name": context["widget"]["name"],
                        "options": {
                            "prefix": context["widget"]["name"],
                        },
                    }
                ),
                "formset": {
                    "prefix": context["widget"]["name"],
                },
            },
            "custom": {
                "drop_text": self.get_drop_text(),
                "empty_text": self.get_empty_text(),
                "empty_icon": self.get_empty_icon(),
                "drop_icon": self.get_drop_icon(),
            },
        }

    def value_from_datadict(self, data, files, name):
        total_forms = int(data.get("images-TOTAL_FORMS"))
        result = []
        for i in range(0, total_forms):
            image_file = files.get(f"images-{i}-image")
            image_raw = data.get(f"images-{i}-RAW")
            image_delete = data.get(f"images-{i}-DELETE")
            if image_delete:
                continue

            if image_file:
                result = [*result, image_file]
            else:
                result = [*result, image_raw]

        return result

    @property
    def needs_multipart_form(self):
        return True

    @property
    def media(self):
        return forms.Media(
            js=(
                "image_uploader_widget/js/vendor/sortable.min.js",
                "image_uploader_widget/js/image-uploader-modal.js",
                "image_uploader_widget/js/image-uploader-inline.js",
            ),
            css={
                "screen": ("image_uploader_widget/css/image-uploader-inline.css",),
            },
        )
