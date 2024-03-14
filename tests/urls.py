from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, path, reverse
from django.shortcuts import redirect

urlpatterns = (
    [
        re_path('admin/', admin.site.urls),
        path('', lambda _: redirect(reverse('admin:index'))),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
