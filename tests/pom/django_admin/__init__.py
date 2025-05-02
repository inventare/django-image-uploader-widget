import uuid
from playwright.sync_api import Page
from django.contrib.auth import get_user_model
from .django_admin_navigations_po import DjangoAdminNavigationsPO
from .django_admin_login_po import DjangoAdminLoginPO
from .django_admin_change_form_po import DjangoAdminChangeFormPO

class DjangoAdminPO:
    """
    Page Object to work with `django-admin` pages used to help with e2e tests.
    """

    def __init__(self, page: Page, live_server_url: str):
        self.navigations = DjangoAdminNavigationsPO(page, live_server_url)
        self.login = DjangoAdminLoginPO(page)
        self.change_form = DjangoAdminChangeFormPO(page)

    def create_root_user(self):
        User = get_user_model()
        username = str(uuid.uuid4()).replace("-", "")
        email = "%s@example.com" % username
        password = username
        user = User.objects.create_superuser(username, email, password)
        return user, username, password

    def create_user_and_execute_login(self):
        _, username, password = self.create_root_user()
        self.navigations.goto_admin_login()
        self.login.execute_login(username, password)

__all__ = ['DjangoAdminPO']
