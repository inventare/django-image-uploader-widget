from django.contrib.messages import SUCCESS, add_message
from django.shortcuts import render

from .forms import TestForm
from .models import TestNonRequired, TestRequired


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
            form = TestRequiredForm(instance=instance)
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


def render_base(request):
    destination = request.GET.get("destination")
    form = TestRequiredForm()
    context = {"destination": destination, "media": form.media}
    template = "test_htmx.html"
    return render(request, template, context=context)
