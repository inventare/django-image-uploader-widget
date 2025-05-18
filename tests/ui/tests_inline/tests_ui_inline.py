import time

from django.core.files import File
from django.test import tag
from django.urls import reverse

from tests.app.inline import models
from tests.pom.component import InlinePO
from tests.utils.dark_mode import dark_theme
from tests.utils.images import get_mock_image
from tests.utils.test_case import TestCase


@tag("ui")
class UIInlineAdminTests(TestCase):
    def setUp(self):
        super().setUp()
        self.inline_po = InlinePO(self.page)

    def init_item(self, only_one=False):
        inline = models.Inline.objects.create()

        self.item1 = models.InlineItem()
        self.item1.parent = inline
        with open(get_mock_image("image1.png"), "rb") as f:
            self.item1.image.save("image.png", File(f))
        self.item1.save()

        if not only_one:
            self.item2 = models.InlineItem()
            self.item2.parent = inline
            with open(get_mock_image("image2.png"), "rb") as f:
                self.item2.image.save("image2.png", File(f))
            self.item2.save()

        return inline

    def goto_change_page(self, only_one=False):
        item = self.init_item(only_one)
        self.admin_po.navigations.goto_change_url(item)
        return item

    def goto_add_page(self):
        self.admin_po.navigations.goto_add_url(models.Inline)

    def test_empty_marker(self):
        self.goto_add_page()

        root = self.inline_po.page_elements.root
        time.sleep(0.5)

        self.assert_match_snapshot(root, "in_test_empty_marker")

    def test_empty_marker_hover(self):
        self.goto_add_page()

        root = self.inline_po.page_elements.root
        self.inline_po.execute_hover_on_empty_marker()
        time.sleep(0.5)

        self.assert_match_snapshot(root, "in_test_empty_marker_hover")

    def test_with_images_data(self):
        self.goto_change_page()

        root = self.inline_po.page_elements.root
        self.assert_match_snapshot(root, "in_test_with_images_data")

    def test_with_images_hover_preview(self):
        self.goto_change_page()

        root = self.inline_po.page_elements.root
        thumbs = self.inline_po.get_visible_thumbnails()
        thumbs[0].execute_hover()
        time.sleep(0.5)

        self.assert_match_snapshot(root, "in_test_with_images_hover_preview")

    def test_hover_preview_icon(self):
        self.goto_change_page()

        root = self.inline_po.page_elements.root
        thumbs = self.inline_po.get_visible_thumbnails()
        thumbs[0].execute_hover_on_preview()
        time.sleep(0.5)

        self.assert_match_snapshot(root, "in_test_hover_preview_icon")

    def test_hover_delete_icon(self):
        self.goto_change_page()

        root = self.inline_po.page_elements.root
        thumbs = self.inline_po.get_visible_thumbnails()
        thumbs[0].execute_hover_on_delete()
        time.sleep(0.5)

        self.assert_match_snapshot(root, "in_test_hover_delete_icon")

    def test_show_preview_modal(self):
        self.goto_change_page()

        thumbs = self.inline_po.get_visible_thumbnails()
        thumbs[0].execute_click_on_preview()
        time.sleep(0.5)

        modal = self.inline_po.modal.page_elements.get_modal(black_overlay=True)
        self.assert_match_snapshot(modal, "in_test_show_preview_modal")

    def test_hover_add_button(self):
        self.goto_change_page()

        root = self.inline_po.page_elements.root
        self.inline_po.execute_hover_on_add_button()
        time.sleep(0.5)

        self.assert_match_snapshot(root, "in_test_hover_add_button")

    def has_scrollbars(self) -> bool:
        return self.page.evaluate(
            """() => {
                var element = document.querySelector(".iuw-inline-root");
                return element.scrollWidth > element.clientWidth;
            }"""
        )

    def test_add_button_on_small_screen(self):
        self.goto_change_page()
        self.page.set_viewport_size({"width": 800, "height": 800})

        time.sleep(0.5)

        self.assertTrue(self.has_scrollbars())

        add_button = self.page.query_selector(".iuw-add-image-btn")
        self.assert_match_snapshot(add_button, "in_test_add_button_on_small_screen")

    def test_ui_initialized_toggle_dark_theme(self):
        self.page.emulate_media(color_scheme="light")
        self.goto_change_page()

        root = self.inline_po.page_elements.root
        self.assert_match_snapshot(root, "in_test_ui_initialized_toggle_dark_theme")

        self.page.query_selector("#header button.theme-toggle").click()
        time.sleep(0.5)

        self.assert_match_snapshot(root, "in_test_ui_initialized_toggle_dark_theme2")

        self.page.emulate_media(color_scheme="light")
