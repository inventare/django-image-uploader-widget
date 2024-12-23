from django.db import models

from image_uploader_widget.postgres.fields import ImageListField


class TestNonRequired(models.Model):
    image = models.ImageField("Image", null=True, blank=True)

    def __str__(self):
        return "Example Model"

    class Meta:
        verbose_name = "Test Non Required"


class TestNonRequiredInline(models.Model):
    class Meta:
        verbose_name = "Test Non Required Inline"


class TestNonRequiredInlineItem(models.Model):
    parent = models.ForeignKey(TestNonRequiredInline, on_delete=models.CASCADE)
    image = models.ImageField("Image", null=True, blank=True)


class TestNonRequiredTabularInline(models.Model):
    class Meta:
        verbose_name = "Test Non Required Tabular Inline"


class TestNonRequiredTabularInlineItem(models.Model):
    parent = models.ForeignKey(TestNonRequiredTabularInline, on_delete=models.CASCADE)
    image = models.ImageField("Image", null=True, blank=True)


class TestRequired(models.Model):
    image = models.ImageField("Image")

    def __str__(self):
        return "Example Model"

    class Meta:
        verbose_name = "Test Required"


class TestRequiredInline(models.Model):
    class Meta:
        verbose_name = "Test Required Inline"


class TestRequiredInlineItem(models.Model):
    parent = models.ForeignKey(TestRequiredInline, on_delete=models.CASCADE)
    image = models.ImageField("Image")


class TestRequiredTabularInline(models.Model):
    class Meta:
        verbose_name = "Test Non Required Tabular Inline"


class TestRequiredTabularInlineItem(models.Model):
    parent = models.ForeignKey(TestRequiredTabularInline, on_delete=models.CASCADE)
    image = models.ImageField("Image")


class Inline(models.Model):
    class Meta:
        verbose_name = "Test With Inline"


class InlineItem(models.Model):
    parent = models.ForeignKey(Inline, related_name="items", on_delete=models.CASCADE)
    image = models.ImageField("Image")


class OrderedInline(models.Model):
    class Meta:
        verbose_name = "Test With Ordered Inline"


class OrderedInlineItem(models.Model):
    parent = models.ForeignKey(
        OrderedInline, related_name="items", on_delete=models.CASCADE
    )
    image = models.ImageField("Image", upload_to="admin_test")
    order = models.PositiveIntegerField("Order", default=1)


class CustomInline(models.Model):
    class Meta:
        verbose_name = "Test Customized Inline"


class CustomInlineItem(models.Model):
    parent = models.ForeignKey(
        CustomInline, related_name="items", on_delete=models.CASCADE
    )
    image = models.ImageField("Image")


class CustomWidget(models.Model):
    image = models.ImageField("Image")

    class Meta:
        verbose_name = "Test Custom Widget"


class TestWithArrayField(models.Model):
    images = ImageListField(blank=True, null=True, upload_to="admin_test")

    class Meta:
        verbose_name = "Test With Array Field"
