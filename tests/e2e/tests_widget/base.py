import time
from playwright.sync_api import expect
from tests.utils.test_case import TestCase
from tests.utils.assert_input_file_clicked import assert_input_file_clicked
from tests.pom.component import WidgetPO
from tests.e2e.base import BaseDragDropTests, BaseEmptyMarkerTests

class BaseWidgetTestCase(
    BaseEmptyMarkerTests,
    BaseDragDropTests,
    TestCase,
):
    """
    Common tests for widget (optional and required).
    """

    def setUp(self):
        super().setUp()
        self.widget_po = WidgetPO(self.page)

    def test_click_on_thumb_image(self):
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_thumbnails()), 0)

        self.widget_po.execute_select_image("image2.png")
        thumb, *_ = self.widget_po.get_visible_thumbnails()

        with assert_input_file_clicked(self.page):
            thumb.execute_click_on_image()

    def test_click_on_preview_button(self):
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_thumbnails()), 0)

        self.widget_po.execute_select_image("image2.png")
        thumb, *_ = self.widget_po.get_visible_thumbnails()
        thumb.execute_click_on_preview()

        modal = self.widget_po.modal.get_visible_modal_for(thumb)
        self.assertIsNotNone(modal)

    def test_click_on_image_inside_modal(self):
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_thumbnails()), 0)

        self.widget_po.execute_select_image("image1.png")
        thumb, *_ = self.widget_po.get_visible_thumbnails()
        thumb.execute_click_on_preview()

        modal = self.widget_po.modal.get_visible_modal_for(thumb)
        self.widget_po.modal.execute_click_on_image(modal)

        time.sleep(1)

        self.assertEqual(modal.get_attribute("class"), "iuw-modal visible")

    def test_click_close_button_inside_modal(self):
        self.goto_add_page()

        self.assertEqual(len(self.widget_po.get_visible_thumbnails()), 0)

        self.widget_po.execute_select_image("image1.png")
        thumb, *_ = self.widget_po.get_visible_thumbnails()
        thumb.execute_click_on_preview()

        modal = self.widget_po.modal.get_visible_modal_for(thumb)
        self.widget_po.modal.execute_click_on_close_button(modal)

        locator = self.page.locator("#iuw-modal-element")
        expect(locator).not_to_be_visible(timeout=3000)
