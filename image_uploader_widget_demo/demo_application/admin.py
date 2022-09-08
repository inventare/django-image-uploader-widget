from django.contrib import admin
from . import models
from . import forms

@admin.register(models.TestNonRequired)
class TestNonRequiredAdmin(admin.ModelAdmin):
    form = forms.TestNonRequiredForm


class TestNonRequiredInlineItemAdmin(admin.StackedInline):
    model = models.TestNonRequiredInlineItem
    form = forms.TestNonRequiredForm
    extra = 0

@admin.register(models.TestNonRequiredInline)
class TestNonRequiredInlineAdmin(admin.ModelAdmin):
    inlines = [TestNonRequiredInlineItemAdmin]
