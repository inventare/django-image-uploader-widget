import os
import time
import uuid

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from match_snapshot import MatchSnapshot
from playwright.sync_api import expect, sync_playwright


class _AssertInputFileClicked:
    def __init__(
        self,
        test_case,
        input_selector=".form-row.field-image input[type=file]",
        index=0,
    ):
        self.test_case = test_case
        self.input_selector = input_selector
        self.index = index

    def __enter__(self):
        injected_javascript = (
            "async () => {"
            "   window.result = false;"
            f'  const inputs = document.querySelectorAll("{self.input_selector}");'
            f"  const input = inputs[{self.index}];"
            '   input.addEventListener("click", (e) => { e.preventDefault(); window.result = true; });'
            "};"
        )
        self.test_case.page.evaluate(injected_javascript)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.test_case.assertEqual(
            str(self.test_case.page.evaluate_handle("window.result")), "true"
        )


class _DarkMode:
    def __init__(self, test_case):
        self.test_case = test_case

    def __enter__(self):
        self.test_case.page.emulate_media(color_scheme="dark")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.test_case.page.emulate_media(color_scheme="light")


class IUWTestCase(MatchSnapshot, StaticLiveServerTestCase):
    model = None

    def _get_mock_image(self, name: str):
        base_dir = os.path.dirname(__file__)
        mocks_dir = os.path.join(base_dir, "__mocks__")
        return os.path.join(mocks_dir, name)

    @property
    def image1(self):
        """Get the file path of the image1."""
        return self._get_mock_image("image1.png")

    @property
    def image2(self):
        """Get the file path of the image2."""
        return self._get_mock_image("image2.png")

    @property
    def image3(self):
        """Get the file path of the image2."""
        return self._get_mock_image("image3.png")

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

    def wait(self, seconds: float) -> None:
        """
        Wait for a time.

        Args:
            - seconds: the time to wait, in seconds.
        """
        time.sleep(seconds)

    def goto_add_page(self):
        """
        Navigate the playwright to the add page for the model.
        """
        self.page.goto(f"{self.live_server_url}/admin/tests/{self.model}/add")

    def goto_change_page(self, id: int):
        """
        Navigate the playwright to the change page for the model.

        Args:
            - id: the entity id to change.
        """
        self.page.goto(f"{self.live_server_url}/admin/tests/{self.model}/{id}/change")

    def setUp(self):
        self.page = self.browser.new_page()
        self.login()

    def _create_root_user(self):
        """
        Create an root user to login inside the django-admin.
        """
        User = get_user_model()
        username = str(uuid.uuid4()).replace("-", "")
        email = "%s@example.com" % username
        password = username
        user = User.objects.create_superuser(username, email, password)
        return user, username, password

    def login(self):
        """
        Create an root user and login into the django-admin.
        """
        _, username, password = self._create_root_user()

        self.page.goto(f"{self.live_server_url}/admin/login/")
        self.page.wait_for_selector("text=Django administration")
        self.page.fill("[name=username]", username)
        self.page.fill("[name=password]", password)
        self.page.click("text=Log in")

    def submit_form(self, id: str):
        """Submit the form by clicking on an button or input with type=submit."""
        submit = self.page.query_selector(f'{id} [type="submit"]')
        submit.click()

    def assert_success_message(self):
        """Wait and assert for the success message on the django-admin."""
        alert = self.page.wait_for_selector(".messagelist .success", timeout=3000)
        self.assertIsNotNone(alert)

    def assert_input_file_clicked(
        self, input_selector=".form-row.field-image input[type=file]", index=0
    ):
        return _AssertInputFileClicked(self, input_selector, index)

    def dark_theme(self):
        return _DarkMode(self)

    def find_widget_form_row(self, element=None):
        if not element:
            element = self.page
        return element.query_selector(".form-row.field-image")

    def find_widget_root(self, element=None):
        if not element:
            element = self.page
        return element.query_selector(".form-row.field-image .iuw-root")

    def find_inline_root(self, element=None):
        if not element:
            element = self.page
        return element.query_selector(".iuw-inline-root")

    def find_widget_preview(self, element=None):
        if not element:
            element = self.page
        return element.query_selector(".iuw-image-preview")

    def find_inline_previews(self, element=None):
        if not element:
            element = self.page
        return element.query_selector_all(
            ".inline-related:not(.empty-form):not(.deleted)"
        )

    def find_inline_order(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('input[name$="order"]')

    def find_deleted_inline_previews(self, element=None):
        if not element:
            element = self.page
        return element.query_selector_all(".inline-related:not(.empty-form).deleted")

    def find_empty_marker(self, element=None):
        if not element:
            element = self.page
        return element.query_selector(".iuw-empty")

    def find_preview_icon(self, element=None):
        if not element:
            element = self.page
        return element.query_selector(".iuw-preview-icon")

    def find_delete_icon(self, element=None):
        if not element:
            element = self.page
        return element.query_selector(".iuw-delete-icon")

    def find_add_button(self, element=None):
        if not element:
            element = self.page
        return element.query_selector(".iuw-add-image-btn")

    def find_drop_label(self, element=None):
        if not element:
            element = self.page
        return element.query_selector(".iuw-drop-label")

    def find_drop_zone(self, element=None):
        if not element:
            element = self.page
        return element.query_selector(".iuw-drop-label")

    def get_preview_modal(self, visible=True, timout=3000, black_overlay=False):
        class_name = ""
        if visible:
            class_name = ".visible"

        preview_modal = self.page.wait_for_selector(
            f"#iuw-modal-element{class_name}", timeout=timout
        )

        if black_overlay:
            self.page.evaluate(
                "document.getElementById('iuw-modal-element').style.background = '#000';"
            )

        return preview_modal

    def assert_preview_modal(self, preview_img):
        preview_modal = self.get_preview_modal(True, 3000)
        self.assertIsNotNone(preview_modal)
        self.assertEqual(preview_modal.get_attribute("class"), "iuw-modal visible")

        img = preview_modal.query_selector("img")
        self.assertIsNotNone(img)
        self.assertEqual(img.get_attribute("src"), preview_img.get_attribute("src"))

    def assert_preview_modal_close(self):
        preview_modal = self.get_preview_modal(True, 0)
        close_button = preview_modal.query_selector(".iuw-modal-close")
        close_button.click()

        locator = self.page.locator("#iuw-modal-element")
        expect(locator).not_to_be_visible(timeout=3000)

    def wait_for_empty_marker(self, element=None, timeout=3000):
        if not element:
            element = self.page
        return element.wait_for_selector(".iuw-empty", timeout=timeout)
