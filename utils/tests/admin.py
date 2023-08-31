import uuid
from selenium.webdriver.common.by import By
from django.contrib.auth import get_user_model

class AdminMixin:
    """
    Provides an mixin to help working with django-admin.
    """

    def get_url_from_path(self, path: str) -> str:
        """
        Gets an url from the live-server url and the path name.

        :Args:
            - path: the path to gets the url.
        """
        return "%s%s" % (self.live_server_url, path)
    
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
        """
        Navigate to login page, fill the form and submit the login credentials.
        """
        _, username, password = self._create_root_user()

        self.selenium.get(self.get_url_from_path('/admin/login'))
        
        username_input = self.selenium.find_element(By.ID, "id_username")
        password_input = self.selenium.find_element(By.ID, "id_password")
        submit = self.selenium.find_element(By.XPATH, "//input[@type='submit']")

        username_input.send_keys(username)
        password_input.send_keys(password)
        submit.click()
