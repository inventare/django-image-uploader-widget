import uuid
import os
from django.test import tag
from django.core.files import File
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from django.contrib.auth import get_user_model
from tests import models

@tag('playwright')
class MyTests(StaticLiveServerTestCase):
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

    def init_item(self):
        item = models.TestRequired()
        with open(self.image1, 'rb') as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item

    def test_empty_marker_click(self):
        self.page.goto(f"{self.live_server_url}/admin/tests/testrequired/add")
        self.inject_input_file_clicked()
        self.page.query_selector('.form-row.field-image .iuw-empty').click()
        self.assert_input_file_clicked()

    def test_required_file_input(self):
        self.page.goto(f"{self.live_server_url}/admin/tests/testrequired/add")

        form_row = self.page.query_selector('.form-row.field-image')
        preview = form_row.query_selector('.iuw-image-preview')
        self.assertEqual(preview, None)

        file_input = form_row.query_selector('input[type=file]')
        self.assertEqual(file_input.get_attribute('value'), None)
        file_input.set_input_files(self.image1)

        preview = form_row.query_selector('.iuw-image-preview')
        img = preview.query_selector('img')
        preview_button = preview.query_selector('.iuw-preview-icon')
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertIsNotNone(preview_button)

        submit = self.page.query_selector('#testrequired_form [type="submit"]')
        submit.click()

        alert = self.page.wait_for_selector('.messagelist .success', timeout=3000)
        self.assertIsNotNone(alert)
        itens = models.TestRequired.objects.all()
        self.assertEqual(len(itens), 1)
        item = itens[0]
        self.assertIsNotNone(item.image)

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

    def test_image_with_database_data(self):
        item = self.init_item()
        self.page.goto(f"{self.live_server_url}/admin/tests/testrequired/{item.id}/change")

        root = self.find_widget_root()
        preview = self.find_widget_preview(root)

        self.assertIsNotNone(preview)
        self.assertEqual(root.get_attribute("data-raw"), item.image.url)

        empty_marker = self.find_empty_marker(root)
        self.assertFalse(empty_marker.is_visible())
        
        img = preview.query_selector('img')
        preview_button = self.find_preview_icon(preview)
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertTrue(item.image.url in img.get_attribute('src'))
        self.assertIsNotNone(preview_button)
