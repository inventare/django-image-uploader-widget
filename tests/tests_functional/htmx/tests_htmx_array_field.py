import uuid

from django.core.files import File
from django.test.utils import tag

from tests import models
from tests.helpers.drag_drop_label_test_helper import DragDropLabelTestCaseMixin
from tests.helpers.reorder_test_helper import ReorderTestCaseMixin

from . import HTMXTestCase


@tag("e2e", "htmx", "array_field")
class HTMXWidgetArrayFieldDragDropTestCase(DragDropLabelTestCaseMixin, HTMXTestCase):
    skip_setup = True
    root_selector = ".iuw-inline-root"

    def goto_add_page(self):
        endpoint = "test-htmx/?destination=/test-htmx-image-widget/array_field/"
        self.page.goto(f"{self.live_server_url}/{endpoint}")
        self.load_htmx_widget()


@tag("e2e", "htmx", "array_field")
class HTMXWidgetArrayFieldReorderTestCase(ReorderTestCaseMixin, HTMXTestCase):
    skip_setup = True

    def goto_add_page(self):
        endpoint = "test-htmx/?destination=/test-htmx-image-widget/array_field/"
        self.page.goto(f"{self.live_server_url}/{endpoint}")
        self.load_htmx_widget()

    def goto_change_page(self):
        instance = models.TestWithArrayField.objects.order_by("id").last()
        endpoint = (
            f"test-htmx/?destination=/test-htmx-image-widget/array_field/{instance.pk}/"
        )
        self.page.goto(f"{self.live_server_url}/{endpoint}")
        self.load_htmx_widget()

    def get_images(self):
        instance = models.TestWithArrayField.objects.order_by("id").last()
        return instance.images


@tag("e2e", "htmx", "array_field")
class HTMXWidgetArrayFieldTestCase(HTMXTestCase):
    input_selector = ".temp_file"
    root_selector = ".iuw-inline-root"

    def goto_page(self):
        endpoint = "test-htmx/?destination=/test-htmx-image-widget/array_field/"
        self.page.goto(f"{self.live_server_url}/{endpoint}")

    def _have_empty_marker(self):
        empty = self.find_empty_marker(self.root)
        add_button = self.find_add_button(self.root)

        self.assertFalse(add_button.is_visible())
        self.assertIsNotNone(empty)
        self.assertTrue(empty.is_visible())

    def _click_on_empty(self):
        with self.assert_input_file_clicked(input_selector=self.input_selector):
            empty_marker = self.find_empty_marker()
            self.assertTrue(empty_marker.is_visible())
            empty_marker.click()

    def _upload_files(self):
        temp_file = self.root.query_selector(".temp_file")

        previews = self.find_inline_previews(self.root)
        self.assertEqual(len(previews), 0)

        temp_file.set_input_files(self.image1)
        previews = self.find_inline_previews(self.root)
        self.assertEqual(len(previews), 1)

        temp_file.set_input_files(self.image2)
        previews = self.find_inline_previews(self.root)
        self.assertEqual(len(previews), 2)

        for preview in previews:
            img = preview.query_selector("img")
            preview_button = self.find_preview_icon(preview)
            remove_button = self.find_delete_icon(preview)
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

    def _remove_not_uploaded_file(self):
        temp_file = self.root.query_selector(".temp_file")
        temp_file.set_input_files(self.image3)

        previews = self.find_inline_previews(self.root)
        self.assertEqual(len(previews), 3)

        self.find_delete_icon(previews[2]).click()
        self.assertEqual(len(self.find_inline_previews(self.root)), 2)

    def _goto_edit_page(self):
        endpoint = f"test-htmx/?destination=/test-htmx-image-widget/array_field/{self.item.pk}/"
        self.page.goto(f"{self.live_server_url}/{endpoint}")
        self.load_htmx_widget()
        self.root = self.find_inline_root()

        previews = self.find_inline_previews(self.root)
        self.assertEqual(len(previews), 2)

        for index, preview in enumerate(previews):
            img = preview.query_selector("img")
            preview_button = self.find_preview_icon(preview)
            remove_button = self.find_delete_icon(preview)
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

            src = img.get_attribute("src")
            if index == 0:
                self.assertTrue(self.item.images[0] in src)
            else:
                self.assertTrue(self.item.images[1] in src)

    def _remove_saved_image(self):
        previews = self.find_inline_previews(self.root)
        self.assertEqual(len(previews), 2)

        for preview in previews:
            self.find_delete_icon(preview).click()

        previews = self.find_inline_previews(self.root)
        self.assertEqual(len(previews), 0)

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        item = models.TestWithArrayField.objects.get(pk=self.item.pk)
        self.assertEqual(len(item.images), 0)

    def _click_preview_image(self):
        previews = self.find_inline_previews(self.root)
        self.assertEqual(len(previews), 2)

        selector = ".inline-related:not(.empty-form):not(.deleted) input[type=file]"
        for index, preview in enumerate(previews):
            with self.assert_input_file_clicked(selector, index):
                img = preview.query_selector("img")
                img.click()

    def _click_on_add_button(self):
        with self.assert_input_file_clicked(".temp_file"):
            add_button = self.find_add_button(self.root)
            self.assertTrue(add_button.is_visible())
            add_button.click()

    def _preview_modal(self):
        previews = self.find_inline_previews(self.root)
        self.assertEqual(len(previews), 2)

        for preview in previews:
            preview_img = preview.query_selector("img")
            self.find_preview_icon(preview).click()
            self.assert_preview_modal(preview_img)

            preview_modal = self.get_preview_modal(True, 3000)
            img = preview_modal.query_selector("img")
            img.click()
            self.wait(0.5)
            self.assertEqual(preview_modal.get_attribute("class"), "iuw-modal visible")

            self.assert_preview_modal_close()

    def _change_image(self):
        previews = self.find_inline_previews(self.root)
        self.assertEqual(len(previews), 2)

        url1 = self.item.images[0]
        preview = previews[0]
        preview_img = preview.query_selector("img")
        preview_src = preview_img.get_attribute("src")

        file_input = preview.query_selector("input[type=file]")
        file_input.set_input_files(self.image1)

        self.assertNotEqual(preview_src, preview_img.get_attribute("src"))

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        item = models.TestWithArrayField.objects.get(pk=self.item.pk)
        self.assertNotEqual(item.images[0], url1)

    def test_htmx_array_field_add_flow(self):
        self._have_empty_marker()
        self._click_on_empty()
        self._upload_files()
        self._remove_not_uploaded_file()
        self._click_preview_image()
        self._click_on_add_button()
        self._preview_modal()

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        self.item = models.TestWithArrayField.objects.first()
        self.assertIsNotNone(self.item)
        self.assertEqual(len(self.item.images), 2)
        for url in self.item.images:
            self.assertIsNotNone(url)

        self._goto_edit_page()
        self._change_image()

        endpoint = f"test-htmx/?destination=/test-htmx-image-widget/array_field/{self.item.pk}/"
        self.page.goto(f"{self.live_server_url}/{endpoint}")
        self.load_htmx_widget()
        self.root = self.find_inline_root()
        self._remove_saved_image()
