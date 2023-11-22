import uuid
import os
import time
from django.test import tag
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect
from django.contrib.auth import get_user_model

@tag('playwright')
class TestCase(StaticLiveServerTestCase):
    model = None

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

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

    def setUp(self):
        self.page = self.browser.new_page()
        self.login()

    def inject_input_file_clicked(self, input_selector = ".form-row.field-image input[type=file]"):
        injected_javascript = (
            'async () => {'
            '   window.result = false;'
            f'   const input = document.querySelector("{input_selector}");'
            '   input.addEventListener("click", (e) => { e.preventDefault(); window.result = true; });'
            '};'
        )
        self.page.evaluate(injected_javascript)

    def assert_input_file_clicked(self):
        self.assertEqual(str(self.page.evaluate_handle('window.result')), 'true')
    
    @property
    def image1(self):
        """gets the file path of the image1."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mocks_dir = os.path.join(base_dir, "utils", "tests", "mocks")
        image = os.path.join(mocks_dir, "image.png")
        return image
    
    @property
    def image2(self):
        """gets the file path of the image2."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mocks_dir = os.path.join(base_dir, "utils", "tests", "mocks")
        image = os.path.join(mocks_dir, "image2.png")
        return image
    
    def goto_add_page(self):
        self.page.goto(f"{self.live_server_url}/admin/tests/{self.model}/add")

    def goto_change_page(self, id: int):
        self.page.goto(f"{self.live_server_url}/admin/tests/{self.model}/{id}/change")

    def find_widget_form_row(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.form-row.field-image')

    def find_widget_root(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.form-row.field-image .iuw-root')
    
    def find_widget_preview(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-image-preview')
    
    def find_empty_marker(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-empty')

    def find_preview_icon(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-preview-icon')
    
    def submit_form(self, id: str):
        submit = self.page.query_selector(f'{id} [type="submit"]')
        submit.click()

    def assert_success_message(self):
        alert = self.page.wait_for_selector('.messagelist .success', timeout=3000)
        self.assertIsNotNone(alert)

    def get_preview_modal(self, visible=True, timout=3000):
        class_name = ''
        if visible:
            class_name = '.visible'

        preview_modal = self.page.wait_for_selector(f'#iuw-modal-element{class_name}', timeout=timout)
        return preview_modal

    def assert_preview_modal(self, preview_img):
        preview_modal = self.get_preview_modal(True, 3000)
        self.assertIsNotNone(preview_modal)
        self.assertEqual(preview_modal.get_attribute('class'), 'iuw-modal visible')

        img = preview_modal.query_selector('img')
        self.assertIsNotNone(img)
        self.assertEqual(img.get_attribute("src"), preview_img.get_attribute("src"))

    def assert_preview_modal_close(self):
        preview_modal = self.get_preview_modal(True, 0)
        close_button = preview_modal.query_selector('.iuw-modal-close')
        close_button.click()

        locator = self.page.locator('#iuw-modal-element')
        expect(locator).not_to_be_visible(timeout=3000)
    
    def wait(self, seconds: float) -> None:
        time.sleep(seconds)

