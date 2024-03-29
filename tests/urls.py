from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, re_path, reverse

urlpatterns = (
    [
        re_path("admin/", admin.site.urls),
        path("", lambda _: redirect(reverse("admin:index"))),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
