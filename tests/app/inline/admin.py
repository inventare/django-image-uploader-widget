from django.contrib import admin

from image_uploader_widget.admin import ImageUploaderInline, OrderedImageUploaderInline

from . import models


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
