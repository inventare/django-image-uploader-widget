# Out of box HTMX Support for Array Field

!!! warning "Version Information"

    Introduced at the 0.6.0 version.

## Behaviour

The behaviour for the out of box HTMX support for Array Field is a little bit different of the **widget**. The **array field** uses the base of inline admin to render the widget and the *drag and drop* support request initialization. Then to add out of box support, we decided to handle the initialization inside the `htmx:afterSwap` event:

```javascript
// image-uploader-inline.js
//
// ...
//
document.addEventListener('DOMContentLoaded', function() {
  initialize();
});
document.addEventListener('htmx:afterSwap', function(ev) {
  initialize(ev.target);
})
```

## Usage example

The usage example is the same of the widget. The parent view and template is created using:

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
    hx-get="/test-htmx-image-widget/array_field/"
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
def render_array_field_required(request, pk=None):
    instance = TestWithArrayField.objects.get(pk=pk) if pk else None
    if request.method == "POST":
        form = TestWithArrayFieldForm(
            instance=instance, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            form.save()
            instance = form.instance
            form = TestWithArrayFieldForm(instance=instance)
            add_message(request, SUCCESS, "Saved")
    else:
        form = TestWithArrayFieldForm(instance=instance)

    context = {
        "form": form,
        "instance": instance,
        "post_url": "test-htmx-image-widget/array_field",
    }
    template = "test_htmx_widget.html"
    return render(request, template, context=context)
```

```html
<!-- test_htmx_widget.html -->
<form
  hx-post="/test-htmx-image-widget/array_field/{% if instance %}{{ instance.pk }}/{% endif %}"
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
