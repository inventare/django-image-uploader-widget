from playwright.sync_api import Page

class DjangoAdminChangeFormPE:
    def __init__(self, page: Page):
        self.change_form = page.locator(".change-form #content-main form")
        self.change_form_submit = self.change_form.locator('[type="submit"][name="_save"]')
