from django.db import models

class ExampleModel(models.Model):
    image = models.ImageField('Image', null = True, blank = True)
