from django.contrib import admin

from image_uploader_widget.admin import ImageUploaderInline, OrderedImageUploaderInline

from . import forms, models


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


class OrderedInlineEditor(OrderedImageUploaderInline):
    model = models.OrderedInlineItem


@admin.register(models.OrderedInline)
class OrderedInlineAdmin(admin.ModelAdmin):
    inlines = [OrderedInlineEditor]


class CustomInlineEditor(ImageUploaderInline):
    model = models.CustomInlineItem
    add_image_text = "add_image_text"
    drop_text = "drop_text"
    empty_text = "empty_text"

    def get_empty_icon(self):
        return "empty_icon"

    def get_add_icon(self):
        return "add_icon"

    def get_drop_icon(self):
        return "drop_icon"


@admin.register(models.CustomInline)
class CustomInlineAdmin(admin.ModelAdmin):
    inlines = [CustomInlineEditor]


@admin.register(models.CustomWidget)
class CustomWidgetAdmin(admin.ModelAdmin):
    form = forms.TestCustomForm


@admin.register(models.TestWithArrayField)
class TestWithArrayFieldAdmin(admin.ModelAdmin):
    form = forms.TestWithArrayFieldForm
