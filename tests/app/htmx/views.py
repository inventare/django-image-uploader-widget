from django.contrib.messages import SUCCESS, add_message
from django.shortcuts import render
from django.urls import reverse
from tests.app.array_field.forms import TestWithArrayFieldForm
from tests.app.widget.models import NonRequired, Required
from tests.app.array_field.models import TestWithArrayField
from .forms import NonRequiredForm, RequiredForm

def widget_required(request, pk=None):
    instance = Required.objects.get(pk=pk) if pk else None
    if request.method == "POST":
        form = RequiredForm(
            instance=instance, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            form.save()
            instance = form.instance
            form = RequiredForm(instance=instance)
            add_message(request, SUCCESS, "Saved")
    else:
        form = RequiredForm(instance=instance)

    context = {
        "form": form,
        "instance": instance,
        "post_url": reverse('required'),
    }
    template = "test_htmx_widget.html"
    return render(request, template, context=context)


def widget_optional(request, pk=None):
    instance = NonRequired.objects.get(pk=pk) if pk else None
    if request.method == "POST":
        form = NonRequiredForm(
            instance=instance, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            form.save()
            instance = form.instance
            form = NonRequiredForm(instance=instance)
            add_message(request, SUCCESS, "Saved")
    else:
        form = NonRequiredForm(instance=instance)

    context = {
        "form": form,
        "instance": instance,
        "post_url": reverse('optional'),
    }
    template = "test_htmx_widget.html"
    return render(request, template, context=context)


def array_field_required(request, pk=None):
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
        "post_url": reverse('array'),
    }
    template = "test_htmx_widget.html"
    return render(request, template, context=context)


def base(request, extra_context=None):
    if not extra_context:
        extra_context = {}
    destination = request.GET.get("destination")
    form = RequiredForm()
    form2 = TestWithArrayFieldForm()
    context = {
        "destination": destination,
        "media": form.media + form2.media,
        **extra_context,
    }
    template = "test_htmx.html"
    return render(request, template, context=context)


def base_light(request):
    return base(request, extra_context={"theme": "iuw-light"})

def base_dark(request):
    return base(request, extra_context={"theme": "iuw-dark"})
