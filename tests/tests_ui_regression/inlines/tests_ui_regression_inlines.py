import django
from django.core.files import File
from django.test import tag

from tests import models, test_case


@tag("ui-regression", "inline")
class InlineEditorUIRegressionTestCase(test_case.IUWTestCase):
    model = "inline"

    def init_item(self, only_one=False):
        inline = models.Inline.objects.create()

        self.item1 = models.InlineItem()
        self.item1.parent = inline
        with open(self.image1, "rb") as f:
            self.item1.image.save("image.png", File(f))
        self.item1.save()

        if not only_one:
            self.item2 = models.InlineItem()
            self.item2.parent = inline
            with open(self.image2, "rb") as f:
                self.item2.image.save("image2.png", File(f))
            self.item2.save()

        return inline

    def goto_change_page(self, only_one=False):
        item = self.init_item(only_one)
        super().goto_change_page(item.id)
        return item

    def test_empty_marker(self):
        self.goto_add_page()
        self.wait_for_empty_marker()

        root = self.find_inline_root()
        self.wait(0.5)

        self.assert_match_snapshot(root, "in_test_empty_marker")

    def test_empty_marker_hover(self):
        self.goto_add_page()
        self.wait_for_empty_marker()

        root = self.find_inline_root()
        self.find_empty_marker().hover()
        self.wait(0.5)

        self.assert_match_snapshot(root, "in_test_empty_marker_hover")

    def test_with_images_data(self):
        self.goto_change_page()

        root = self.find_inline_root()
        self.assert_match_snapshot(root, "in_test_with_images_data")

    def test_with_images_hover_preview(self):
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        previews[0].hover()
        self.wait(0.5)

        self.assert_match_snapshot(root, "in_test_with_images_hover_preview")

    def test_hover_preview_icon(self):
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.find_preview_icon(previews[0]).hover()
        self.wait(0.5)

        self.assert_match_snapshot(root, "in_test_hover_preview_icon")

    def test_show_preview_modal(self):
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.find_preview_icon(previews[0]).click()
        self.wait(0.5)

        modal = self.get_preview_modal(black_overlay=True)
        self.assert_match_snapshot(modal, "in_test_show_preview_modal")

    def test_hover_delete_icon(self):
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.find_delete_icon(previews[0]).hover()
        self.wait(0.5)

        self.assert_match_snapshot(root, "in_test_hover_delete_icon")

    def test_hover_add_button(self):
        self.goto_change_page()

        root = self.find_inline_root()
        self.find_add_button(root).hover()
        self.wait(0.5)

        self.assert_match_snapshot(root, "in_test_hover_add_button")

    def test_add_button_on_small_screen(self):
        self.goto_change_page()
        self.page.set_viewport_size({"width": 800, "height": 800})

        self.wait(0.5)

        has_scrollbars = self.page.evaluate(
            """() => {
            var element = document.querySelector(".iuw-inline-root");
            return element.scrollWidth > element.clientWidth;
        }"""
        )
        self.assertTrue(has_scrollbars)

        add_button = self.page.query_selector(".iuw-add-image-btn")
        self.assert_match_snapshot(add_button, "in_test_add_button_on_small_screen")

    def test_ui_initialized_toggle_dark_theme(self):
        major, minor, _, _, _ = django.VERSION
        if major < 4 or minor < 2:
            # Theme toggle is added in django 4.2
            # https://docs.djangoproject.com/en/4.2/releases/4.2/#django-contrib-admin
            return

        self.page.emulate_media(color_scheme="light")
        self.goto_change_page()

        root = self.find_inline_root()
        self.assert_match_snapshot(root, "in_test_ui_initialized_toggle_dark_theme")

        self.page.query_selector("#header button.theme-toggle").click()
        self.wait(0.3)

        self.assert_match_snapshot(root, "in_test_ui_initialized_toggle_dark_theme2")

        self.page.emulate_media(color_scheme="light")
