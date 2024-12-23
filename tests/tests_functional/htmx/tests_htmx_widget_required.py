from django.core.files import File
from django.test import tag

from tests import models
from tests.helpers.drag_drop_label_test_helper import DragDropLabelTestCaseMixin

from . import HTMXTestCase


@tag("e2e", "htmx")
class HTMXWidgetRequiredDragDropTestCase(DragDropLabelTestCaseMixin, HTMXTestCase):
    skip_setup = True
    root_selector = ".iuw-root"

    def goto_add_page(self):
        self.page.goto(f"{self.live_server_url}/test-htmx/")
        self.load_htmx_widget()


@tag("e2e", "htmx")
class HTMXWidgetRequiredAddTestCase(HTMXTestCase):
    def goto_page(self):
        self.page.goto(f"{self.live_server_url}/test-htmx/")

    def _click_on_empty(self):
        with self.assert_input_file_clicked(input_selector=self.input_selector):
            empty_marker = self.find_empty_marker()
            self.assertTrue(empty_marker.is_visible())
            empty_marker.click()

    def _upload_image(self):
        preview = self.find_widget_preview(self.root)
        self.assertFalse(preview.is_visible())

        file_input = self.root.query_selector("input[type=file]")
        self.assertEqual(file_input.get_attribute("value"), None)
        file_input.set_input_files(self.image1)

        preview = self.find_widget_preview(self.root)
        img = preview.query_selector("img")
        preview_button = preview.query_selector(".iuw-preview-icon")
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertIsNotNone(preview_button)

    def _click_on_preview(self):
        with self.assert_input_file_clicked(input_selector=self.input_selector):
            preview = self.find_widget_preview(self.root)
            img = preview.query_selector("img")
            img.click()

    def _preview_modal(self):
        preview = self.find_widget_preview(self.root)
        preview_img = preview.query_selector("img")
        preview_button = self.find_preview_icon(preview)
        preview_button.click()
        self.assert_preview_modal(preview_img)

        preview_modal = self.get_preview_modal(True, 3000)
        img = preview_modal.query_selector("img")
        img.click()

        self.wait(0.5)
        self.assertEqual(preview_modal.get_attribute("class"), "iuw-modal visible")

        self.assert_preview_modal_close()

    def test_htmx_widget_required_add_page_flow(self):
        self._click_on_empty()
        self._upload_image()
        self._click_on_preview()
        self._preview_modal()

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        items = models.TestRequired.objects.all()
        self.assertEqual(len(items), 1)
        self.item = items[0]
        self.assertIsNotNone(self.item.image)

        endpoint = (
            f"test-htmx/?destination=/test-htmx-image-widget/required/{self.item.pk}/"
        )
        self.page.goto(f"{self.live_server_url}/{endpoint}")
        self.load_htmx_widget()
        self.root = self.page.query_selector(self.root_selector)
        self.item = items[0]

        preview = self.find_widget_preview(self.root)
        self.assertIsNotNone(preview)
        self.assertEqual(self.root.get_attribute("data-raw"), self.item.image.url)

        empty_marker = self.find_empty_marker(self.root)
        self.assertFalse(empty_marker.is_visible())

        img = preview.query_selector("img")
        preview_button = self.find_preview_icon(preview)
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertTrue(self.item.image.url in img.get_attribute("src"))
        self.assertIsNotNone(preview_button)
