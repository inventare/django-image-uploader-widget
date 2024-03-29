import datetime
import os
import pathlib
import posixpath
from typing import Optional

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import Storage, default_storage
from django.db.models import ImageField
from django.db.models.fields.files import FieldFile

from .forms import ImageListFormField


def validate_file_name(name, allow_relative_path=False):
    # TODO: when drop support for django 3.2, remove this function
    # and import from django

    # Remove potentially dangerous names
    if os.path.basename(name) in {"", ".", ".."}:
        raise SuspiciousFileOperation("Could not derive file name from '%s'" % name)

    if allow_relative_path:
        # Use PurePosixPath() because this branch is checked only in
        # FileField.generate_filename() where all file paths are expected to be
        # Unix style (with forward slashes).
        path = pathlib.PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            raise SuspiciousFileOperation(
                "Detected path traversal attempt in '%s'" % name
            )
    elif name != os.path.basename(name):
        raise SuspiciousFileOperation("File name '%s' includes path elements" % name)

    return name


class ImageListField(ArrayField):
    def __init__(
        self,
        *args,
        max_length: int = 150,
        storage: Optional[Storage] = None,
        upload_to: str = "",
        **kwargs,
    ):
        self.max_length = max_length or 150
        self.storage = storage or default_storage
        self.upload_to = upload_to or ""
        kwargs["base_field"] = ImageField(
            max_length=self.max_length, upload_to=upload_to
        )
        super().__init__(
            *args,
            **kwargs,
        )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        path = "image_uploader_widget.postgres.fields.ImageListField"
        kwargs.update(
            {
                "base_field": self.base_field.clone(),
                "size": self.size,
                "max_length": self.max_length,
                "upload_to": self.upload_to,
            }
        )
        return name, path, args, kwargs

    def generate_filename(self, instance, filename):
        """
        Apply (if callable) or prepend (if a string) upload_to to the filename,
        then delegate further processing of the name to the storage backend.
        Until the storage layer, all file paths are expected to be Unix style
        (with forward slashes).
        """
        if callable(self.upload_to):
            filename = self.upload_to(instance, filename)
        else:
            dirname = datetime.datetime.now().strftime(str(self.upload_to))
            filename = posixpath.join(dirname, filename)
        filename = validate_file_name(filename, allow_relative_path=True)
        return self.storage.generate_filename(filename)

    def _get_file(self, instance, file):
        if isinstance(file, str):
            return FieldFile(instance, self, file)

        field_file = FieldFile(instance, self, file.name)
        field_file.file = file
        field_file._committed = False
        return field_file

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        value = [self._get_file(model_instance, item) for item in value]

        for file in value:
            if file and not file._committed:
                file.save(file.name, file.file, save=False)

        return value

    def save_form_data(self, instance, data):
        if not data:
            data = []
        return super().save_form_data(instance, data)

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": ImageListFormField,
                **kwargs,
            }
        )
