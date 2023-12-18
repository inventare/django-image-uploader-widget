---
sidebar_position: 4
---

# Multiple Instances of Same Form

On the issue [#112](https://github.com/inventare/django-image-uploader-widget/issues/112), [@tlcaputi](https://github.com/tlcaputi) asked about using the `django-image-uploader-widget` with several forms. The answer for this issue, motivated this documentation article.

The basic idea for this article is: we have an `view` with multiples instances of the same `ModelForm` with one (or more) `django-image-uploader-widget`. For example, we have a `Event` model, a `EventEditForm` model form, a `page` view and a `page.html` template:

```python
# models.py
from django.db import models

class Event(models.Model):
    event_title = models.CharField(max_length=200)
    headshot = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')
```

```python
# forms.py
from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget
from .models import Event

class EventEditForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
            'headshot': ImageUploaderWidget(),
        }
        fields = [
            'event_title',
            'headshot'
        ]
```

```python
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import EventEditForm

def page(request):
    if request.method == "GET":
        events = Event.objects.all()
        events_with_forms = []
        for event in events:
            events_with_forms.append({
                'event': event,
                'form': EventEditForm(instance=event),
            })
        return render(request, "page.html", {
            'events_with_form': events_with_forms,
            'new_event_form': EventEditForm(),
        })
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        if not event_id:
            form = EventEditForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')

        event = get_object_or_404(Event, pk=event_id)
        form = EventEditForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home')
```

```html
<!-- templates/page.html -->
{% load crispy_forms_filters %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    {{new_event_form.media}}
</head>
<body>

    {% for event in events_with_form %}
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}
            <input type="hidden" name="event_id" value="{{ event.event.id }}">
            {{ event.form|crispy }}
            <button type="submit">Update</button>
        </form>
    {% endfor %}

    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ new_event_form|crispy }}
        <button type="submit">Create</button>
    </form>
    
</body>
</html>
```

By default, this does not work, and the reason for this is: the field id is used to control the `django-image-uploader-widget` and the field id is the same for each form. To solve this problem we have to change the field id attribute for each field, and this can be does changing the ModelForm:

```python
# forms.py
from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget
from .models import Event

class EventEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            id = str(self.instance.pk)
            self.fields['headshot'].widget.attrs['id'] = "headshot_%s" % id
        
    class Meta:
        model = Event
        widgets = {
            'headshot': ImageUploaderWidget(),
        }
        fields = [
            'event_title',
            'headshot'
        ]
```

--- 

The original answer is disponible, also, in the [github issue](https://github.com/inventare/django-image-uploader-widget/issues/112#issuecomment-1771635753).

