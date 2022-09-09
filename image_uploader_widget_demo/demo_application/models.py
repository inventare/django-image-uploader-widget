from django.db import models

class TestNonRequired(models.Model):
    image = models.ImageField('Image', null=True, blank=True)

    def __str__(self):
        return 'Example Model'

    class Meta:
        verbose_name = 'Test Non Required'

class TestNonRequiredInline(models.Model):
    class Meta:
        verbose_name = 'Test Non Required Inline'

class TestNonRequiredInlineItem(models.Model):
    parent = models.ForeignKey(TestNonRequiredInline, on_delete=models.CASCADE)
    image = models.ImageField('Image', null=True, blank=True)

class TestNonRequiredTabularInline(models.Model):
    class Meta:
        verbose_name = 'Test Non Required Tabular Inline'
    
class TestNonRequiredTabularInlineItem(models.Model):
    parent = models.ForeignKey(TestNonRequiredTabularInline, on_delete=models.CASCADE)
    image = models.ImageField('Image', null=True, blank=True)

class TestRequired(models.Model):
    image = models.ImageField('Image')

    def __str__(self):
        return 'Example Model'

    class Meta:
        verbose_name = 'Test Required'

class TestRequiredInline(models.Model):
    class Meta:
        verbose_name = 'Test Required Inline'

class TestRequiredInlineItem(models.Model):
    parent = models.ForeignKey(TestRequiredInline, on_delete=models.CASCADE)
    image = models.ImageField('Image')
