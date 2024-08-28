# Out of box HTMX Support for Widget

!!! warning "Version Information"

    Introduced at the 0.6.0 version.

The HTMX is, now, out of box supported, for **widget** and **array field widget**. Even though it has support out of the box, some precautions need to be taken. The media (*scripts* and *styles* of the widget) needs to be loaded in the parent document:

## Behaviour

On the version `0.6.0` the **JavaScript** of the widget was rewrited using event **Event bubbling** and the render part is moved to template system to support the widget behaviour without initialization needed.

## Usage Example

This usage example is taken form `tests` application that is used to run our e2e test cases. The parent view and template is created using:

```python
# views.py
def render_parent(request):
    form = TestRequiredForm()
    form2 = TestWithArrayFieldForm()
    context = {
        "media": form.media + form2.media,
    }
    template = "test_htmx.html"
    return render(request, template, context=context)
```

```html
<!-- test_htmx.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HTMX</title>
  {{ media }}
</head>
<body  hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>

  <button
    hx-get="/test-htmx-image-widget/required/"
    hx-target="this"
    hx-swap="outerHTML"
    hx-trigger="click"
    type="button"
    class="btn-load"
  >
    Load
  </button>

  <script src="https://unpkg.com/htmx.org@1.9.12"></script>
</body>
</html>
```

The widget view and template is created using:

```python
# views.py
def render_widget_required(request, pk=None):
    instance = TestRequired.objects.get(pk=pk) if pk else None
    if request.method == "POST":
        form = TestRequiredForm(
            instance=instance, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            form.save()
            instance = form.instance
            form = TestRequiredForm(instance=instance)
            add_message(request, SUCCESS, "Saved")
    else:
        form = TestRequiredForm(instance=instance)

    context = {
        "form": form,
        "instance": instance,
        "post_url": "test-htmx-image-widget/required",
    }
    template = "test_htmx_widget.html"
    return render(request, template, context=context)
```

```html
<!-- test_htmx_widget.html -->
<form
  hx-post="/test-htmx-image-widget/required/{% if instance %}{{ instance.pk }}/{% endif %}"
  hx-target="this"
  hx-swap="outerHTML"
  enctype="multipart/form-data"
  id="my-widget-form"
>
  {% if messages %}
    <ul class="messagelist">
      {% for message in messages %}
        <li class="{{ message.tags }}">{{ message }}</li>
      {% endfor %}
    </ul>
  {% endif %}

  {{ form }}

  <button class="btn-submit" type="submit">Submit</button>
</form>
```
