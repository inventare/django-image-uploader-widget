from django import forms
from django.core.exceptions import ValidationError

from .models import TestWithArrayField


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
