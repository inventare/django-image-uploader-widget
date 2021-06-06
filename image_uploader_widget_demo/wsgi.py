import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "image_uploader_widget_demo.settings")

application = get_wsgi_application()