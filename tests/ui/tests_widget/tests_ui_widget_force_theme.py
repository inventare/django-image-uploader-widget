import time

from django.test import tag
from django.urls import reverse

from tests.pom.component import WidgetPO
from tests.utils.test_case import TestCase


@tag("ui")
class UIWidgetForceThemeTests(TestCase):
    def setUp(self):
        super().setUp()
        self.widget_po = WidgetPO(self.page)

    def goto_add_page(self, theme="light"):
        base = reverse(f"htmx-{theme}")
        dest = reverse("optional")
        url = f"{base}?destination={dest}"
        self.admin_po.navigations.goto(url)

    def load_widget(self):
        button = self.page.query_selector(".btn-load")
        button.click()
        time.sleep(0.4)

    def test_force_light_theme(self):
        self.page.emulate_media(color_scheme="dark")

        self.goto_add_page()
        self.load_widget()

        self.widget_po.execute_select_image("image2.png")

        time.sleep(0.5)

        self.assert_match_snapshot(
            self.widget_po.page_elements.root, "wo_test_ui_test_force_light_theme"
        )
        self.page.emulate_media(color_scheme="light")

    def test_force_dark_theme(self):
        self.page.emulate_media(color_scheme="light")

        self.goto_add_page("dark")
        self.load_widget()

        self.widget_po.execute_select_image("image2.png")

        time.sleep(0.5)

        self.assert_match_snapshot(
            self.widget_po.page_elements.root, "wo_test_ui_test_force_dark_theme"
        )
        self.page.emulate_media(color_scheme="light")
