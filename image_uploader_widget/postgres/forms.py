from itertools import chain

from django import forms
from django.contrib.postgres.utils import prefix_validation_error
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .widget import ImageUploaderArrayWidget


class ImageListFormField(forms.Field):
    default_error_messages = {
        "item_invalid": _("Item %(name)s in the array did not validate:"),
    }

    def __init__(self, **kwargs):
        kwargs.pop("base_field")
        self.max_length = kwargs.pop("max_length") or 150

        self.required = False
        self.base_field = forms.ImageField(max_length=self.max_length)
        widget = ImageUploaderArrayWidget()
        kwargs.setdefault("widget", widget)
        super().__init__(**kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        return [self.base_field.to_python(item) for item in value]

    def clean(self, value):
        cleaned_data = []
        errors = []

        max_size = len(value)
        for index in range(max_size):
            item = value[index]
            if isinstance(item, str):
                cleaned_data.append(item)
                continue

            file_name = item.name
            try:
                cleaned_item = self.base_field.clean(item)
                cleaned_data.append(cleaned_item)
            except ValidationError as error:
                errors.append(
                    prefix_validation_error(
                        error,
                        self.error_messages["item_invalid"],
                        code="item_invalid",
                        params={"name": file_name},
                    )
                )
                cleaned_data.append(None)
            else:
                errors.append(None)

        errors = list(filter(None, errors))
        if errors:
            raise ValidationError(list(chain.from_iterable(errors)))
        return cleaned_data

    def has_changed(self, initial, data):
        try:
            data = self.to_python(data)
        except ValidationError:
            pass
        else:
            if initial in self.empty_values and data in self.empty_values:
                return False
        return super().has_changed(initial, data)
