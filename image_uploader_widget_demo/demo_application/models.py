from django.db import models

class ExampleModel(models.Model):
    image = models.ImageField('Image', null = True, blank = True)

    image2 = models.ImageField('Image 2')

    image3 = models.ImageField('Image 3', null = True, blank = True)

    def __str__(self):
        return 'Example Model'

    class Meta:
        verbose_name = 'Example Model'
        verbose_name_plural = 'Example Models'

class ExampleModelImage(models.Model):
    example = models.ForeignKey(ExampleModel, on_delete = models.CASCADE)
    image = models.ImageField('Image')

class AnotherModalImagesExample(models.Model):
    example = models.ForeignKey(ExampleModel, on_delete = models.CASCADE)
    image = models.ImageField('Image')

class StackedExample(models.Model):
    example = models.ForeignKey(ExampleModel, on_delete = models.CASCADE)
    title = models.CharField('Example', max_length = 100)
    text = models.TextField('Text')
    image = models.ImageField('Image')
