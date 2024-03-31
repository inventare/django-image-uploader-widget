from typing import Any

from django import forms
from django.contrib.postgres.forms import SplitArrayField
from django.core.exceptions import ValidationError

from image_uploader_widget.postgres.widget import ImageUploaderArrayWidget
from image_uploader_widget.widgets import ImageUploaderWidget

from .models import CustomWidget, TestWithArrayField


class TestForm(forms.ModelForm):
    class Meta:
        widgets = {
            "image": ImageUploaderWidget(),
        }
        fields = "__all__"


class TestCustomForm(forms.ModelForm):
    class Meta:
        model = CustomWidget
        widgets = {
            "image": ImageUploaderWidget(
                drop_icon="@drop_icon@",
                drop_text="@drop_text@",
                empty_icon="@empty_icon@",
                empty_text="@empty_text@",
            ),
        }
        fields = "__all__"


class TestWithArrayFieldForm(forms.ModelForm):
    old_values = []

    def map_is_valid_images(self, value):
        if not isinstance(value, str):
            return False
        return value not in self.old_values

    def clean(self):
        data = super().clean()

        self.old_values = []
        if self.instance is not None:
            self.old_values = self.instance.images

        has_changed = any(list(map(self.map_is_valid_images, data.get("images"))))
        if has_changed:
            raise ValidationError("One of the non-changed value is corrupted.")

        return data

    class Meta:
        model = TestWithArrayField
        fields = "__all__"
