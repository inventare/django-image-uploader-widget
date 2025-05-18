import time

from django.core.files import File
from django.test import tag
from django.urls import reverse

from tests.app.widget import models
from tests.pom.component import WidgetPO
from tests.utils.dark_mode import dark_theme
from tests.utils.images import get_mock_image
from tests.utils.test_case import TestCase


@tag("ui")
class UIWidgetRequiredTests(TestCase):
    def setUp(self):
        super().setUp()
        self.widget_po = WidgetPO(self.page)

    def goto_add_page(self):
        self.admin_po.navigations.goto_add_url(models.Required)

    def init_item(self):
        item = models.Required()
        with open(get_mock_image("image1.png"), "rb") as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item

    def goto_change_page(self):
        item = self.init_item()
        self.admin_po.navigations.goto_change_url(item)
        return item

    def test_ui_empty_marker(self, dark=False):
        image_id = "wr_test_ui_empty_marker"
        if dark:
            image_id = f"{image_id}_dark"

        self.goto_add_page()
        self.widget_po.page_elements.empty_marker.hover()
        self.admin_po.change_form.page_elements.change_form_submit.hover()
        time.sleep(0.5)
        root = self.widget_po.page_elements.root
        self.assert_match_snapshot(root, image_id)

    def test_ui_empty_marker_dark(self):
        with dark_theme(self.page):
            self.test_ui_empty_marker(dark=True)

    def test_ui_empty_marker_hovered(self, dark=False):
        image_id = "wr_test_ui_empty_marker_hovered"
        if dark:
            image_id = f"{image_id}_dark"

        self.goto_add_page()
        time.sleep(0.5)

        self.widget_po.execute_hover_on_empty_marker()
        time.sleep(0.5)

        root = self.widget_po.page_elements.root
        self.assert_match_snapshot(root, image_id)

    def test_ui_empty_marker_hovered_dark(self):
        with dark_theme(self.page):
            self.test_ui_empty_marker_hovered(dark=True)

    def test_ui_initialized_with_data(self, dark=False):
        image_id = "wr_test_ui_initialized_with_data"
        if dark:
            image_id = f"{image_id}_dark"

        self.goto_change_page()

        root = self.widget_po.page_elements.root
        preview, *_ = self.widget_po.get_visible_thumbnails()
        preview.execute_hover()
        self.assert_match_snapshot(root, image_id)

    def test_ui_initialized_with_data_dark(self):
        with dark_theme(self.page):
            self.test_ui_initialized_with_data(dark=True)

    def test_ui_initialized_with_data_hover_preview(self, dark=False):
        image_id = "wr_test_ui_initialized_with_data_hover_preview"
        if dark:
            image_id = f"{image_id}_dark"

        self.goto_change_page()

        root = self.widget_po.page_elements.root
        preview, *_ = self.widget_po.get_visible_thumbnails()
        preview.execute_hover_on_preview()
        time.sleep(0.5)
        self.assert_match_snapshot(root, image_id)

    def test_ui_initialized_with_data_hover_preview_dark(self):
        with dark_theme(self.page):
            self.test_ui_initialized_with_data_hover_preview(dark=True)

    def test_ui_initialized_toggle_dark_theme(self):
        self.page.emulate_media(color_scheme="light")
        self.goto_change_page()

        root = self.widget_po.page_elements.root
        self.assert_match_snapshot(root, "wr_test_ui_initialized_toggle_dark_theme")
        toggle = self.page.query_selector("#header button.theme-toggle")
        toggle.click()
        time.sleep(0.5)

        self.assert_match_snapshot(root, "wr_test_ui_initialized_toggle_dark_theme2")

        self.page.emulate_media(color_scheme="light")

    def test_ui_initialized_toggle_dark_theme_inverted(self):
        with dark_theme(self.page):
            self.goto_change_page()

            root = self.widget_po.page_elements.root
            time.sleep(0.5)
            self.assert_match_snapshot(
                root, "wr_test_ui_initialized_toggle_dark_theme_inverted"
            )

            toggle = self.page.query_selector("#header button.theme-toggle")
            toggle.click()
            time.sleep(0.5)

            self.assert_match_snapshot(
                root, "wr_test_ui_initialized_toggle_dark_theme_inverted2"
            )

    def test_ui_initialized_with_data_preview(self, dark=False):
        image_id = "wr_test_ui_initialized_with_data_preview"
        if dark:
            image_id = f"{image_id}_dark"

        self.goto_change_page()

        preview, *_ = self.widget_po.get_visible_thumbnails()
        preview.execute_click_on_preview()
        time.sleep(0.5)

        modal = self.widget_po.modal.page_elements.get_modal(black_overlay=True)

        self.assert_match_snapshot(modal, "wr_test_ui_initialized_with_data_preview")

    def test_ui_initialized_with_data_preview_dark(self):
        with dark_theme(self.page):
            self.test_ui_initialized_with_data_preview(dark=True)
