import time

from playwright.sync_api import expect

from tests.e2e.base import BaseDragDropTests, BaseEmptyMarkerTests
from tests.pom.component import InlinePO
from tests.utils.assert_input_file_clicked import assert_input_file_clicked
from tests.utils.test_case import TestCase


class InlineBaseTestCase(
    BaseEmptyMarkerTests,
    BaseDragDropTests,
    TestCase,
):
    empty_marker_file_input_selector = ".temp_file"

    def setUp(self):
        super().setUp()
        self.inline_po = InlinePO(self.page)

    def test_choose_same_file_delete_and_choose_again(self):
        self.goto_add_page()

        self.inline_po.execute_select_image("image1.png")

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 1)

        thumbs[0].execute_click_on_delete()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 0)

        self.inline_po.execute_select_image("image1.png")
        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 1)

    def test_choose_same_file_two_times(self):
        self.goto_add_page()

        self.inline_po.execute_select_image("image1.png")

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 1)

        self.inline_po.execute_select_image("image1.png")
        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)

    def test_initial_state(self):
        self.goto_add_page()
        time.sleep(0.3)

        self.assertFalse(self.inline_po.is_add_button_visible())
        self.assertTrue(self.inline_po.is_empty_marker_visible())

    def test_click_add_button(self):
        self.goto_change_page()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)
        self.assertTrue(self.inline_po.is_add_button_visible())

        with assert_input_file_clicked(
            self.page, self.empty_marker_file_input_selector
        ):
            self.inline_po.execute_click_on_add_button()

    def test_click_on_expand_button(self):
        self.goto_change_page()

        thumb, *_ = self.inline_po.get_visible_thumbnails()
        thumb.execute_click_on_preview()

        modal = self.inline_po.modal.get_visible_modal_for(thumb)
        self.assertIsNotNone(modal)

    def test_click_in_image_inside_modal(self):
        self.goto_change_page()

        thumb, *_ = self.inline_po.get_visible_thumbnails()
        thumb.execute_click_on_preview()

        modal = self.inline_po.modal.get_visible_modal_for(thumb)
        self.inline_po.modal.execute_click_on_image(modal)

        time.sleep(1)

        self.assertEqual(modal.get_attribute("class"), "iuw-modal visible")

    def test_click_close_button_inside_modal(self):
        self.goto_change_page()

        thumb, *_ = self.inline_po.get_visible_thumbnails()
        thumb.execute_click_on_preview()

        modal = self.inline_po.modal.get_visible_modal_for(thumb)
        self.inline_po.modal.execute_click_on_close_button(modal)

        locator = self.page.locator("#iuw-modal-element")
        expect(locator).not_to_be_visible(timeout=3000)

    def test_initialized_widget(self):
        self.goto_change_page()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)

        for thumb in thumbs:
            self.assertTrue(thumb.is_valid(required=False))

    def test_click_on_thumb_image(self):
        self.goto_change_page()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)

        selector = ".inline-related:not(.empty-form):not(.deleted) input[type=file]"

        for index in range(0, len(thumbs)):
            with assert_input_file_clicked(self.page, selector, index):
                thumbs[index].execute_click_on_image()
