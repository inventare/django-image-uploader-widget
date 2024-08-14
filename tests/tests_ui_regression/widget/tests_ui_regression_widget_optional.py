import django
from django.core.files import File
from django.test.utils import tag

from tests import models, test_case


@tag("ui-regression", "widget")
class OptionaldWidgetTestCase(test_case.IUWTestCase):
    model = "testnonrequired"

    def init_item(self):
        item = models.TestNonRequired()
        with open(self.image2, "rb") as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item

    def goto_change_page(self):
        item = self.init_item()
        super().goto_change_page(item.id)
        return item

    def test_ui_empty_marker(self):
        self.goto_add_page()
        self.wait_for_empty_marker()
        self.wait(0.5)

        root = self.find_widget_root()
        self.assert_match_snapshot(root, "wo_test_ui_empty_marker")

    def test_ui_empty_marker_dark(self):
        self.page.emulate_media(color_scheme="dark")
        self.goto_add_page()

        self.wait_for_empty_marker()
        self.wait(0.5)

        root = self.find_widget_root()
        self.assert_match_snapshot(root, "wo_test_ui_empty_marker_dark")
        self.page.emulate_media(color_scheme="light")

    def test_ui_empty_marker_hovered(self):
        self.goto_add_page()

        empty = self.find_empty_marker()
        empty.hover()
        self.wait(0.5)

        root = self.find_widget_root()
        self.assert_match_snapshot(root, "wo_test_ui_empty_marker_hovered")

    def test_ui_empty_marker_hovered_dark(self):
        self.page.emulate_media(color_scheme="dark")
        self.goto_add_page()

        empty = self.find_empty_marker()
        empty.hover()
        self.wait(0.5)

        root = self.find_widget_root()
        self.assert_match_snapshot(root, "wo_test_ui_empty_marker_hovered_dark")
        self.page.emulate_media(color_scheme="light")

    def test_ui_initialized_with_data(self):
        self.goto_change_page()

        root = self.find_widget_root()
        preview = self.find_widget_preview(root)
        preview.hover()
        self.wait(0.5)

        self.assert_match_snapshot(root, "wo_test_ui_initialized_with_data")

    def test_ui_initialized_with_data_dark(self):
        self.page.emulate_media(color_scheme="dark")
        self.goto_change_page()

        root = self.find_widget_root()
        preview = self.find_widget_preview(root)
        preview.hover()
        self.wait(0.5)

        self.assert_match_snapshot(root, "wo_test_ui_initialized_with_data_dark")
        self.page.emulate_media(color_scheme="light")

    def test_ui_initialized_with_data_hover_preview(self):
        self.goto_change_page()

        root = self.find_widget_root()
        preview_icon = self.find_preview_icon(root)
        preview_icon.hover()
        self.wait(0.5)

        self.assert_match_snapshot(
            root, "wo_test_ui_initialized_with_data_hover_preview"
        )

    def test_ui_initialized_with_data_hover_preview_dark(self):
        self.page.emulate_media(color_scheme="dark")
        self.goto_change_page()

        root = self.find_widget_root()
        preview_icon = self.find_preview_icon(root)
        preview_icon.hover()
        self.wait(0.5)

        self.assert_match_snapshot(
            root, "wo_test_ui_initialized_with_data_hover_preview_dark"
        )
        self.page.emulate_media(color_scheme="light")

    def test_ui_initialized_with_data_hover_remove(self):
        self.goto_change_page()

        root = self.find_widget_root()
        delete_icon = self.find_delete_icon(root)
        delete_icon.hover()
        self.wait(0.5)

        self.assert_match_snapshot(
            root, "wo_test_ui_initialized_with_data_hover_remove"
        )

    def test_ui_initialized_with_data_hover_remove_dark(self):
        self.page.emulate_media(color_scheme="dark")
        self.goto_change_page()

        root = self.find_widget_root()
        delete_icon = self.find_delete_icon(root)
        delete_icon.hover()
        self.wait(0.5)

        self.assert_match_snapshot(
            root, "wo_test_ui_initialized_with_data_hover_remove_dark"
        )
        self.page.emulate_media(color_scheme="light")

    def test_ui_initialized_with_data_preview(self):
        self.goto_change_page()

        root = self.find_widget_root()
        preview_icon = self.find_preview_icon(root)
        preview_icon.click()
        self.wait(0.5)

        modal = self.get_preview_modal(black_overlay=True)
        self.assert_match_snapshot(modal, "wo_test_ui_initialized_with_data_preview")

    def test_ui_initialized_with_data_preview_dark(self):
        self.page.emulate_media(color_scheme="dark")
        self.goto_change_page()

        root = self.find_widget_root()
        preview_icon = self.find_preview_icon(root)
        preview_icon.click()
        self.wait(0.5)

        modal = self.get_preview_modal(black_overlay=True)
        self.assert_match_snapshot(
            modal, "wo_test_ui_initialized_with_data_preview_dark"
        )
        self.page.emulate_media(color_scheme="light")

    def test_ui_initialized_toggle_dark_theme(self):
        major, minor, _, _, _ = django.VERSION
        if major < 4 or minor < 2:
            # Theme toggle is added in django 4.2
            # https://docs.djangoproject.com/en/4.2/releases/4.2/#django-contrib-admin
            return

        self.page.emulate_media(color_scheme="light")
        self.goto_change_page()

        root = self.find_widget_root()
        self.assert_match_snapshot(root, "wo_test_ui_initialized_toggle_dark_theme")

        toggle = self.page.query_selector("#header button.theme-toggle")
        toggle.click()
        self.wait(0.5)

        self.assert_match_snapshot(root, "wo_test_ui_initialized_toggle_dark_theme2")
        self.page.emulate_media(color_scheme="light")

    def test_ui_initialized_toggle_dark_theme_inverted(self):
        major, minor, _, _, _ = django.VERSION
        if major < 4 or minor < 2:
            # Theme toggle is added in django 4.2
            # https://docs.djangoproject.com/en/4.2/releases/4.2/#django-contrib-admin
            return
        self.page.emulate_media(color_scheme="dark")
        self.goto_change_page()

        root = self.find_widget_root()
        self.assert_match_snapshot(
            root, "wo_test_ui_initialized_toggle_dark_theme_inverted"
        )

        toggle = self.page.query_selector("#header button.theme-toggle")
        toggle.click()
        self.wait(0.5)

        self.assert_match_snapshot(
            root, "wo_test_ui_initialized_toggle_dark_theme_inverted2"
        )
        self.page.emulate_media(color_scheme="light")
