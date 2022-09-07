from django.contrib import admin

from . import models
from . import forms

@admin.register(models.TestNonRequired)
class TestNonRequiredAdmin(admin.ModelAdmin):
    form = forms.TestNonRequiredForm
