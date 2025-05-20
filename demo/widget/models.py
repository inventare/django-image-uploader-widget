from django.db import models

# Optional


class NonRequired(models.Model):
    image = models.ImageField("Image", null=True, blank=True)

    def __str__(self):
        return "Example Model"

    class Meta:
        verbose_name = "(Widget) Non Required"


class NonRequiredStackedInline(models.Model):
    class Meta:
        verbose_name = "(Widget) Non Required inside Stacked Inline"


class NonRequiredStackedInlineItem(models.Model):
    parent = models.ForeignKey(NonRequiredStackedInline, on_delete=models.CASCADE)
    image = models.ImageField("Image", null=True, blank=True)


class NonRequiredTabularInline(models.Model):
    class Meta:
        verbose_name = "(Widget) Non Required inside Tabular Inline"


class NonRequiredTabularInlineItem(models.Model):
    parent = models.ForeignKey(NonRequiredTabularInline, on_delete=models.CASCADE)
    image = models.ImageField("Image", null=True, blank=True)


# Required


class Required(models.Model):
    image = models.ImageField("Image")

    def __str__(self):
        return "Example Model"

    class Meta:
        verbose_name = "(Widget) Required"


class RequiredStackedInline(models.Model):
    class Meta:
        verbose_name = "(Widget) Required inside Stacked Inline"


class RequiredStackedInlineItem(models.Model):
    parent = models.ForeignKey(RequiredStackedInline, on_delete=models.CASCADE)
    image = models.ImageField("Image")


class RequiredTabularInline(models.Model):
    class Meta:
        verbose_name = "(Widget) Required inside Tabular Inline"


class RequiredTabularInlineItem(models.Model):
    parent = models.ForeignKey(RequiredTabularInline, on_delete=models.CASCADE)
    image = models.ImageField("Image")


# Custom


class Custom(models.Model):
    image = models.ImageField("Image")

    class Meta:
        verbose_name = "(Widget) Custom"
