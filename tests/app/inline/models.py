from django.db import models


class Inline(models.Model):
    class Meta:
        verbose_name = "(Inline) Default"


class InlineItem(models.Model):
    parent = models.ForeignKey(Inline, related_name="items", on_delete=models.CASCADE)
    image = models.ImageField("Image")


class OrderedInline(models.Model):
    class Meta:
        verbose_name = "(Inline) Ordered"


class OrderedInlineItem(models.Model):
    parent = models.ForeignKey(
        OrderedInline, related_name="items", on_delete=models.CASCADE
    )
    image = models.ImageField("Image", upload_to="admin_test")
    order = models.PositiveIntegerField("Order", default=1)


class CustomInline(models.Model):
    class Meta:
        verbose_name = "(Inline) Custom"


class CustomInlineItem(models.Model):
    parent = models.ForeignKey(
        CustomInline, related_name="items", on_delete=models.CASCADE
    )
    image = models.ImageField("Image")
