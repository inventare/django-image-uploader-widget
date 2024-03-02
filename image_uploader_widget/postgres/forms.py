from itertools import chain
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.postgres.utils import prefix_validation_error
from django.utils.translation import gettext_lazy as _
from .widget import ImageUploaderArrayWidget

class ImageListFormField(forms.Field):
    default_error_messages = {
        "item_invalid": _("Item %(nth)s in the array did not validate:"),
    }

    def __init__(self, *, remove_trailing_nulls=False, **kwargs):
        kwargs.pop('base_field')
        self.max_length = kwargs.pop('max_length') or 255

        self.required = False
        self.base_field = forms.ImageField(max_length=255)
        self.remove_trailing_nulls = remove_trailing_nulls
        widget = ImageUploaderArrayWidget()
        kwargs.setdefault("widget", widget)
        super().__init__(**kwargs)

    def _remove_trailing_nulls(self, values):
        index = None
        if self.remove_trailing_nulls:
            for i, value in reversed(list(enumerate(values))):
                if value in self.base_field.empty_values:
                    index = i
                else:
                    break
            if index is not None:
                values = values[:index]
        return values, index

    def to_python(self, value):
        value = super().to_python(value)
        return [self.base_field.to_python(item) for item in value]

    def clean(self, value):
        print("ON CLEAN")
        cleaned_data = []
        errors = []
        
        max_size = len(value)
        for index in range(max_size):
            item = value[index]
            if isinstance(item, str):
                cleaned_data.append(item)
                continue

            try:
                cleaned_data.append(self.base_field.clean(item))
            except ValidationError as error:
                errors.append(
                    prefix_validation_error(
                        error,
                        self.error_messages["item_invalid"],
                        code="item_invalid",
                        params={"nth": index + 1},
                    )
                )
                cleaned_data.append(None)
            else:
                errors.append(None)
        cleaned_data, null_index = self._remove_trailing_nulls(cleaned_data)
        if null_index is not None:
            errors = errors[:null_index]
        errors = list(filter(None, errors))
        if errors:
            raise ValidationError(list(chain.from_iterable(errors)))
        return cleaned_data

    def has_changed(self, initial, data):
        print("OIE?")
        try:
            data = self.to_python(data)
        except ValidationError:
            pass
        else:
            data, _ = self._remove_trailing_nulls(data)
            if initial in self.empty_values and data in self.empty_values:
                return False
        return super().has_changed(initial, data)

