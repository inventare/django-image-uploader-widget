from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path

urlpatterns = (
    [
        re_path('admin/', admin.site.urls),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
