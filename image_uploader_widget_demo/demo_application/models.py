from django.db import models

class ExampleModel(models.Model):
    image = models.ImageField('Image', null = True, blank = True)

    def __str__(self):
        return 'Example Model'

    class Meta:
        verbose_name = 'Example Model'
        verbose_name_plural = 'Example Models'
