from django.contrib import admin
from image_uploader_widget.admin import ImageUploaderInline
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

class TestRequiredInlineItemAdmin(admin.StackedInline):
    model = models.TestRequiredInlineItem
    form = forms.TestForm
    extra = 0

@admin.register(models.TestRequiredInline)
class TestRequiredInlineAdmin(admin.ModelAdmin):
    inlines = [TestRequiredInlineItemAdmin]

class TestRequiredTabularInlineItemAdmin(admin.TabularInline):
    model = models.TestRequiredTabularInlineItem
    form = forms.TestForm
    extra = 0

@admin.register(models.TestRequiredTabularInline)
class TestRequiredTabularInlineAdmin(admin.ModelAdmin):
    inlines = [TestRequiredTabularInlineItemAdmin]

class InlineEditor(ImageUploaderInline):
    model = models.InlineItem

@admin.register(models.Inline)
class InlineAdmin(admin.ModelAdmin):
    inlines = [InlineEditor]
