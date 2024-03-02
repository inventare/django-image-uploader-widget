from django import forms
from django.contrib.postgres.forms import SplitArrayField
from image_uploader_widget.widgets import ImageUploaderWidget
from image_uploader_widget.postgres.widget import ImageUploaderArrayWidget
from .models import CustomWidget, TestWithArrayField

class TestForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageUploaderWidget(),
        }
        fields = '__all__'

class TestCustomForm(forms.ModelForm):
    class Meta:
        model = CustomWidget
        widgets = {
            'image': ImageUploaderWidget(
                drop_icon="@drop_icon@",
                drop_text="@drop_text@",
                empty_icon="@empty_icon@",
                empty_text="@empty_text@",
            ),
        }
        fields = '__all__'
