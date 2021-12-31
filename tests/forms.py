from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget

def get_form(required):
    class ImageOnlyForm(forms.Form):
        image = forms.ImageField(widget=ImageUploaderWidget(), required = required)
    return ImageOnlyForm()
