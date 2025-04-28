from django.contrib import admin
from . import forms, models

@admin.register(models.TestWithArrayField)
class TestWithArrayFieldAdmin(admin.ModelAdmin):
    form = forms.TestWithArrayFieldForm
