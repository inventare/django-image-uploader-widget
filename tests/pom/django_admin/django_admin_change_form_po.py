from playwright.sync_api import Page
from .django_admin_change_form_pe import DjangoAdminChangeFormPE

class DjangoAdminChangeFormPO:
    def __init__(self, page: Page):
        self.page = page
        self.page_elements = DjangoAdminChangeFormPE(page)

    def submit_form(self):
        self.page_elements.change_form_submit.click()
        self.page.wait_for_selector(".messagelist .success", timeout=3000)
