from django.contrib import admin
from . import models
from . import forms

@admin.register(models.TestNonRequired)
class TestNonRequiredAdmin(admin.ModelAdmin):
    form = forms.TestForm

class TestNonRequiredInlineItemAdmin(admin.StackedInline):
    model = models.TestNonRequiredInlineItem
    form = forms.TestForm
    extra = 0

@admin.register(models.TestNonRequiredInline)
class TestNonRequiredInlineAdmin(admin.ModelAdmin):
    inlines = [TestNonRequiredInlineItemAdmin]

class TestNonRequiredTabularInlineItemAdmin(admin.TabularInline):
    model = models.TestNonRequiredTabularInlineItem
    form = forms.TestForm
    extra = 0

@admin.register(models.TestNonRequiredTabularInline)
class TestNonRequiredTabularInlineAdmin(admin.ModelAdmin):
    inlines = [TestNonRequiredTabularInlineItemAdmin]

@admin.register(models.TestRequired)
class TestRequiredAdmin(admin.ModelAdmin):
    form = forms.TestForm
