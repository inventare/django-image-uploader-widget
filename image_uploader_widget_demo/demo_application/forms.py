from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget

class TestForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageUploaderWidget(),
        }
        fields = '__all__'

class TestCustomForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageUploaderWidget(
                drop_icon="drop_icon",
                drop_text="drop_text",
                empty_icon="empty_icon",
                empty_text="empty_text",
            ),
        }
        fields = '__all__'
