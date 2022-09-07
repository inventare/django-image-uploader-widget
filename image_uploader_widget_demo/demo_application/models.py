from django.db import models

class TestNonRequired(models.Model):
    image = models.ImageField('Image', null = True, blank = True)

    def __str__(self):
        return 'Example Model'

    class Meta:
        verbose_name = 'Test Non Required'
        verbose_name_plural = 'Tests Non Required'
