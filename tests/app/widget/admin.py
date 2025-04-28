from django.contrib import admin
from . import models, forms

@admin.register(models.NonRequired)
class NonRequiredAdmin(admin.ModelAdmin):
    form = forms.TestForm

class NonRequiredStackedInlineItemAdmin(admin.StackedInline):
    model = models.NonRequiredStackedInlineItem
    form = forms.TestForm
    extra = 0

@admin.register(models.NonRequiredStackedInline)
class NonRequiredStackedInlineAdmin(admin.ModelAdmin):
    inlines = [NonRequiredStackedInlineItemAdmin]

class NonRequiredTabularInlineItemAdmin(admin.TabularInline):
    model = models.NonRequiredTabularInlineItem
    form = forms.TestForm
    extra = 0

@admin.register(models.NonRequiredTabularInline)
class TestNonRequiredTabularInlineAdmin(admin.ModelAdmin):
    inlines = [NonRequiredTabularInlineItemAdmin]

@admin.register(models.Required)
class RequiredAdmin(admin.ModelAdmin):
    form = forms.TestForm

class RequiredStackedInlineItemAdmin(admin.StackedInline):
    model = models.RequiredStackedInlineItem
    form = forms.TestForm
    extra = 0

@admin.register(models.RequiredStackedInline)
class RequiredStackedInlineAdmin(admin.ModelAdmin):
    inlines = [RequiredStackedInlineItemAdmin]

class RequiredTabularInlineItemAdmin(admin.TabularInline):
    model = models.RequiredTabularInlineItem
    form = forms.TestForm
    extra = 0

@admin.register(models.RequiredTabularInline)
class RequiredTabularInlineAdmin(admin.ModelAdmin):
    inlines = [RequiredTabularInlineItemAdmin]

@admin.register(models.Custom)
class CustomAdmin(admin.ModelAdmin):
    form = forms.TestCustomForm
