from django import forms

from image_uploader_widget.widgets import ImageUploaderWidget

class ExampleForm(forms.ModelForm):

    class Meta:
        widgets = {
            'image': ImageUploaderWidget(),
            'image2': ImageUploaderWidget(),
            'image3': ImageUploaderWidget(),
        }
        fields = '__all__'
