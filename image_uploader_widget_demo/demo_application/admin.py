from django.contrib import admin

from . import models
from . import forms

class ExampleAdmin(admin.ModelAdmin):
    form = forms.ExampleForm

admin.site.register(models.ExampleModel, ExampleAdmin)
