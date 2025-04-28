from playwright.sync_api import Page
from django.db import models
from django.urls import reverse

class DjangoAdminNavigationsPO:
    def __init__(self, page: Page, live_server_url: str):
        self.page = page
        self.live_server_url = live_server_url

    def _get_url(self, url: str):
        if self.live_server_url.endswith("/"):
            new_url = self.live_server_url
        else:
            new_url = self.live_server_url + "/"
        if url[0] == "/":
            url = url[1:]
        return f"{new_url}{url}"

    def get_add_url(self, entity):
        if isinstance(entity, models.Model):
            entity = entity.__class__

        opts = entity._meta
        info = opts.app_label, opts.model_name
        url = reverse("admin:%s_%s_add" % info)
        return self._get_url(url)

    def get_change_url(self, entity):
        opts = entity._meta
        info = opts.app_label, opts.model_name
        url = reverse("admin:%s_%s_change" % info, kwargs={ 'object_id': entity.pk })
        return self._get_url(url)

    def get_login_url(self):
        return self._get_url(reverse('admin:login'))

    def goto_add_url(self, entity):
        url = self.get_add_url(entity)
        self.page.goto(url)

    def goto_change_url(self, entity):
        url = self.get_change_url(entity)
        self.page.goto(url)

    def goto_admin_login(self):
        self.page.goto(self.get_login_url())
