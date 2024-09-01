from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, re_path, reverse

from . import views

urlpatterns = (
    [
        re_path("admin/", admin.site.urls),
        path("test-htmx-image-widget/required/", views.render_widget_required),
        path("test-htmx-image-widget/required/<pk>/", views.render_widget_required),
        path("test-htmx-image-widget/optional/", views.render_widget_optional),
        path("test-htmx-image-widget/optional/<pk>/", views.render_widget_optional),
        path("test-htmx-image-widget/array_field/", views.render_array_field_required),
        path(
            "test-htmx-image-widget/array_field/<pk>/",
            views.render_array_field_required,
        ),
        path("test-htmx/", views.render_base),
        path("test-htmx-light/", views.render_base_light),
        path("test-htmx-dark/", views.render_base_dark),
        path("", lambda _: redirect(reverse("admin:index"))),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
