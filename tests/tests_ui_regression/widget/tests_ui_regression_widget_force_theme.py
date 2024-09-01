from django.core.files import File
from django.test import tag

from tests import models, test_case


@tag("functional", "functional_widget", "widget")
class FunctionalWidgetForceThemeTests(test_case.IUWTestCase):
    def goto_add_page(self, theme="light"):
        url = f"{self.live_server_url}/test-htmx-{theme}/?destination=/test-htmx-image-widget/optional/"
        self.page.goto(url)

    def load_widget(self):
        button = self.page.query_selector(".btn-load")
        button.click()
        self.wait(0.4)

    @tag("currently")
    def test_force_light_theme(self):
        self.page.emulate_media(color_scheme="dark")

        self.goto_add_page()
        self.load_widget()

        root = self.page.query_selector(".iuw-root")
        file_input = root.query_selector("input[type=file]")
        file_input.set_input_files(self.image2)

        self.wait(0.5)

        self.assert_match_snapshot(root, "wo_test_ui_test_force_light_theme")
        self.page.emulate_media(color_scheme="light")

    @tag("currently")
    def test_force_dark_theme(self):
        self.page.emulate_media(color_scheme="light")

        self.goto_add_page("dark")
        self.load_widget()

        root = self.page.query_selector(".iuw-root")
        file_input = root.query_selector("input[type=file]")
        file_input.set_input_files(self.image2)

        self.wait(0.5)

        self.assert_match_snapshot(root, "wo_test_ui_test_force_dark_theme")
        self.page.emulate_media(color_scheme="light")
