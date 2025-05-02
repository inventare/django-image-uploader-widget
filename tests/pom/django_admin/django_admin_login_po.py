from playwright.sync_api import Page

from .django_admin_login_pe import DjangoAdminLoginPE


class DjangoAdminLoginPO:
    def __init__(self, page: Page):
        self.page = page
        self.page_elements = DjangoAdminLoginPE(page)

    def execute_login(self, username: str, password: str):
        self.page.wait_for_selector("text=Django administration")

        self.page_elements.username_input.fill(username)
        self.page_elements.password_input.fill(password)
        self.page_elements.login_button.click()
