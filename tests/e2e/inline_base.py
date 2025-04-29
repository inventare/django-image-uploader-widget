import time
from playwright.sync_api import expect
from tests.utils.test_case import TestCase
from tests.utils.assert_input_file_clicked import assert_input_file_clicked
from tests.pom.widget_inline import WidgetInlinePO

class InlineBaseTestCase(TestCase):
    """
    Common tests for admin inline and array field.
    """

    def setUp(self):
        super().setUp()
        self.inline_po = WidgetInlinePO(self.page)

    def test_upload_same_file_delete_reupload(self):
        self.goto_add_page()

        self.inline_po.choice_image("image1.png")

        previews = self.inline_po.get_visible_previews()
        self.assertEqual(len(previews), 1)

        self.inline_po.click_on_preview_delete(previews[0])

        previews = self.inline_po.get_visible_previews()
        self.assertEqual(len(previews), 0)

        self.inline_po.choice_image("image1.png")
        previews = self.inline_po.get_visible_previews()
        self.assertEqual(len(previews), 1)

    def test_upload_same_file_two_times(self):
        self.goto_add_page()

        self.inline_po.choice_image("image1.png")

        previews = self.inline_po.get_visible_previews()
        self.assertEqual(len(previews), 1)

        self.inline_po.choice_image("image1.png")
        previews = self.inline_po.get_visible_previews()
        self.assertEqual(len(previews), 2)

    def test_empty_marker(self):
        self.goto_add_page()
        time.sleep(0.3)

        self.assertFalse(self.inline_po.is_add_button_visible())
        self.assertTrue(self.inline_po.is_empty_marker_visible())

    def test_click_empty_marker(self):
        self.goto_add_page()

        with assert_input_file_clicked(self.page, ".temp_file"):
            self.inline_po.click_on_empty_marker()

    def test_click_add_button(self):
        self.goto_change_page()

        previews = self.inline_po.get_visible_previews()
        self.assertEqual(len(previews), 2)
        self.assertTrue(self.inline_po.is_add_button_visible())

        with assert_input_file_clicked(self.page, ".temp_file"):
            self.inline_po.click_on_add_button()

    def test_click_on_expand_button(self):
        self.goto_change_page()

        preview, *_ = self.inline_po.get_visible_previews()
        self.inline_po.click_on_preview_expand(preview)

        modal = self.inline_po.modal.get_visible_modal_for(preview.element_handle())
        self.assertIsNotNone(modal)

    def test_click_in_image_inside_modal(self):
        self.goto_change_page()

        preview, *_ = self.inline_po.get_visible_previews()
        self.inline_po.click_on_preview_expand(preview)

        modal = self.inline_po.modal.get_visible_modal_for(preview.element_handle())
        self.inline_po.modal.click_on_modal_image(modal)

        time.sleep(1)

        self.assertEqual(modal.get_attribute("class"), "iuw-modal visible")

    def test_click_close_button_inside_modal(self):
        self.goto_change_page()

        preview, *_ = self.inline_po.get_visible_previews()
        self.inline_po.click_on_preview_expand(preview)

        modal = self.inline_po.modal.get_visible_modal_for(preview.element_handle())
        self.inline_po.modal.click_on_modal_close_button(modal)

        locator = self.page.locator("#iuw-modal-element")
        expect(locator).not_to_be_visible(timeout=3000)
