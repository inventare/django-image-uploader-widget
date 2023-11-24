from django.contrib.auth import get_user_model
import uuid

class AdminMixin:
    model = None
    
    def goto_add_page(self):
        self.page.goto(f"{self.live_server_url}/admin/tests/{self.model}/add")

    def goto_change_page(self, id: int):
        self.page.goto(f"{self.live_server_url}/admin/tests/{self.model}/{id}/change")

    def setUp(self):
        self.page = self.browser.new_page()
        self.login()

    def _create_root_user(self):
        """
        Create an root user to login inside the django-admin.
        """
        User = get_user_model()
        username = str(uuid.uuid4()).replace('-', '')
        email = '%s@example.com' % username
        password = username
        user = User.objects.create_superuser(username, email, password)
        return user, username, password
    
    def login(self):
        _, username, password = self._create_root_user()

        self.page.goto(f"{self.live_server_url}/admin/login/")
        self.page.wait_for_selector('text=Django administration')
        self.page.fill('[name=username]', username)
        self.page.fill('[name=password]', password)
        self.page.click('text=Log in')

    def submit_form(self, id: str):
        submit = self.page.query_selector(f'{id} [type="submit"]')
        submit.click()

    def assert_success_message(self):
        alert = self.page.wait_for_selector('.messagelist .success', timeout=3000)
        self.assertIsNotNone(alert)
