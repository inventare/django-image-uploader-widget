from playwright.sync_api import Page


class DjangoAdminLoginPE:
    def __init__(self, page: Page):
        self.username_input = page.locator("[name=username]")
        self.password_input = page.locator("[name=password]")
        self.login_button = page.locator("text=Log in")
