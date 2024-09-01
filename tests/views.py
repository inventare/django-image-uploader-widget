from django.contrib.messages import SUCCESS, add_message
from django.shortcuts import render

from .forms import TestForm, TestWithArrayFieldForm
from .models import TestNonRequired, TestRequired, TestWithArrayField


class TestRequiredForm(TestForm):
    class Meta(TestForm.Meta):
        model = TestRequired


class TestNonRequiredForm(TestForm):
    class Meta(TestForm.Meta):
        model = TestNonRequired


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


def render_widget_optional(request, pk=None):
    instance = TestNonRequired.objects.get(pk=pk) if pk else None
    if request.method == "POST":
        form = TestNonRequiredForm(
            instance=instance, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            form.save()
            instance = form.instance
            form = TestNonRequiredForm(instance=instance)
            add_message(request, SUCCESS, "Saved")
    else:
        form = TestNonRequiredForm(instance=instance)

    context = {
        "form": form,
        "instance": instance,
        "post_url": "test-htmx-image-widget/optional",
    }
    template = "test_htmx_widget.html"
    return render(request, template, context=context)


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


def render_base(request, extra_context=None):
    if not extra_context:
        extra_context = {}
    destination = request.GET.get("destination")
    form = TestRequiredForm()
    form2 = TestWithArrayFieldForm()
    context = {
        "destination": destination,
        "media": form.media + form2.media,
        **extra_context,
    }
    template = "test_htmx.html"
    return render(request, template, context=context)


def render_base_light(request):
    return render_base(request, extra_context={"theme": "iuw-light"})


def render_base_dark(request):
    return render_base(request, extra_context={"theme": "iuw-dark"})
