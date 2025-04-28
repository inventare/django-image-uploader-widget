import time
from playwright.sync_api import expect
from tests.utils.test_case import TestCase
from tests.utils.assert_input_file_clicked import assert_input_file_clicked
from tests.pom.widget_common import WidgetCommonPO

class BaseWidgetTestCase(TestCase):
    """
    Common tests for widget (optional and required).
    """

    def setUp(self):
        super().setUp()
        self.widget_po = WidgetCommonPO(self.page)

    def test_empty_marker_click(self):
        """
        click on empty marker should fire file input click.
        """
        self.goto_add_page()

        self.assertTrue(self.widget_po.is_empty_marker_visible())
        with assert_input_file_clicked(self.page):
            self.widget_po.execute_click_on_empty_marker()

    def test_drop_label_with_leave(self):
        self.goto_add_page()

        self.assertFalse(self.widget_po.is_drop_label_visible())
        self.widget_po.execute_dragenter()
        self.assertTrue(self.widget_po.is_drop_label_visible())
        self.widget_po.execute_dragleave()
        self.assertFalse(self.widget_po.is_drop_label_visible())

    def test_drop_label_with_drop(self):
        self.goto_add_page()

        self.assertFalse(self.widget_po.is_drop_label_visible())
        self.widget_po.execute_dragenter()
        self.assertTrue(self.widget_po.is_drop_label_visible())
        self.widget_po.execute_drop()
        self.assertFalse(self.widget_po.is_drop_label_visible())

    def test_drop_label_with_dragend(self):
        self.goto_add_page()

        self.assertFalse(self.widget_po.is_drop_label_visible())
        self.widget_po.execute_dragenter()
        self.assertTrue(self.widget_po.is_drop_label_visible())
        self.widget_po.execute_dragend()
        self.assertFalse(self.widget_po.is_drop_label_visible())

    def test_click_on_preview_image(self):
        """
        click on the preview image should fire file input click.
        """
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_previews()), 0)

        self.widget_po.send_image_to_input("image2.png")
        preview, *_ = self.widget_po.get_visible_previews()

        with assert_input_file_clicked(self.page):
            self.widget_po.click_on_preview_iamge(preview)

    def test_click_on_expand_button(self):
        """
        click on the expand button on preview should open the modal.
        """
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_previews()), 0)

        self.widget_po.send_image_to_input("image2.png")
        preview, *_ = self.widget_po.get_visible_previews()
        self.widget_po.click_on_preview_expand_button(preview)

        modal = self.widget_po.modal.get_visible_modal_for(preview)
        self.assertIsNotNone(modal)

    def test_click_in_image_inside_modal(self):
        """
        click on image inside modal should not close it.
        """
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_previews()), 0)

        self.widget_po.send_image_to_input("image1.png")
        preview, *_ = self.widget_po.get_visible_previews()
        self.widget_po.click_on_preview_expand_button(preview)

        modal = self.widget_po.modal.get_visible_modal_for(preview)
        self.widget_po.modal.click_on_modal_image(modal)

        time.sleep(1)

        self.assertEqual(modal.get_attribute("class"), "iuw-modal visible")

    def test_click_close_button_inside_modal(self):
        """
        click on the close button inside modal should close it.
        """
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_previews()), 0)

        self.widget_po.send_image_to_input("image1.png")
        preview, *_ = self.widget_po.get_visible_previews()
        self.widget_po.click_on_preview_expand_button(preview)

        modal = self.widget_po.modal.get_visible_modal_for(preview)
        self.widget_po.modal.click_on_modal_close_button(modal)

        locator = self.page.locator("#iuw-modal-element")
        expect(locator).not_to_be_visible(timeout=3000)
