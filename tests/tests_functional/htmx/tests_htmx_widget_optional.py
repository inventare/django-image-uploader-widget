from django.core.files import File
from django.test.utils import tag

from tests import models, test_case


@tag("functional", "functional_widget", "widget", "htmx")
class HTMXWidgetOptionalTestCase(test_case.IUWTestCase):
    def goto_add_page(self):
        self.page.goto(
            f"{self.live_server_url}/test-htmx/?destination=/test-htmx-image-widget/optional/"
        )

    def goto_change_page(self):
        item = self.init_item()
        self.page.goto(
            f"{self.live_server_url}/test-htmx/?destination=/test-htmx-image-widget/optional/{item.pk}/"
        )
        return item

    def init_item(self):
        item = models.TestNonRequired()
        with open(self.image1, "rb") as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item

    def load_widget(self):
        button = self.page.query_selector(".btn-load")
        button.click()
        self.wait(0.4)

    def test_empty_marker_click(self):
        self.goto_add_page()
        self.load_widget()

        with self.assert_input_file_clicked(
            input_selector=".iuw-root input[type=file]"
        ):
            empty_marker = self.find_empty_marker()
            self.assertTrue(empty_marker.is_visible())
            empty_marker.click()

    def test_non_required_file_input(self):
        self.assertEqual(models.TestNonRequired.objects.count(), 0)
        self.goto_add_page()
        self.load_widget()

        form_row = self.page.query_selector(".iuw-root")
        preview = self.find_widget_preview(form_row)
        self.assertFalse(preview.is_visible())

        file_input = form_row.query_selector("input[type=file]")
        file_input.set_input_files(self.image1)

        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)

        img = preview.query_selector("img")
        preview_button = self.find_preview_icon()
        delete_button = self.find_delete_icon()
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertIsNotNone(preview_button)
        self.assertIsNotNone(delete_button)

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        items = models.TestNonRequired.objects.all()
        self.assertEqual(len(items), 1)
        self.assertIsNotNone(items[0].image)

    def test_remove_button_with_non_saved_image(self):
        self.assertEqual(models.TestNonRequired.objects.count(), 0)
        self.goto_add_page()
        self.load_widget()

        form_row = self.page.query_selector(".iuw-root")
        file_input = form_row.query_selector("input[type=file]")
        file_input.set_input_files(self.image2)

        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)
        delete_button = self.find_delete_icon(preview)
        delete_button.click()

        preview = self.find_widget_preview(form_row)
        self.assertFalse(preview.is_visible())

    def test_image_with_database_data(self):
        item = self.goto_change_page()
        self.load_widget()

        root = self.page.query_selector(".iuw-root")

        preview = self.find_widget_preview(root)
        self.assertIsNotNone(preview)
        self.assertEqual(root.get_attribute("data-raw"), item.image.url)

        empty_marker = self.find_empty_marker(root)
        self.assertFalse(empty_marker.is_visible())

        img = preview.query_selector("img")
        preview_button = self.find_preview_icon(preview)
        delete_button = self.find_delete_icon(preview)
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertTrue(item.image.url in img.get_attribute("src"))
        self.assertIsNotNone(preview_button)
        self.assertIsNotNone(delete_button)

    def test_delete_saved_image(self):
        self.goto_change_page()
        self.load_widget()

        form_row = self.page.query_selector(".iuw-root")
        checkbox = form_row.query_selector("[type=checkbox]")
        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)

        self.assertFalse(checkbox.is_checked())

        delete_button = self.find_delete_icon(preview)
        delete_button.click()

        preview = self.find_widget_preview(form_row)
        self.assertFalse(preview.is_visible())

        self.assertTrue(checkbox.is_checked())

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        items = models.TestNonRequired.objects.all()
        self.assertEqual(len(items), 1)
        self.assertFalse(bool(items[0].image))

    def test_click_on_the_preview_image(self):
        self.goto_add_page()
        self.load_widget()

        form_row = self.page.query_selector(".iuw-root")
        preview = self.find_widget_preview(form_row)
        self.assertFalse(preview.is_visible())
        file_input = form_row.query_selector("input[type=file]")
        file_input.set_input_files(self.image1)

        with self.assert_input_file_clicked(
            input_selector=".iuw-root input[type=file]"
        ):
            preview = self.find_widget_preview(form_row)
            self.assertIsNotNone(preview)
            img = preview.query_selector("img")
            img.click()

    def test_click_on_the_preview_button(self):
        self.goto_add_page()
        self.load_widget()

        form_row = self.page.query_selector(".iuw-root")
        preview = self.find_widget_preview(form_row)
        self.assertFalse(preview.is_visible())
        file_input = form_row.query_selector("input[type=file]")
        file_input.set_input_files(self.image2)

        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)
        preview_img = preview.query_selector("img")
        preview_button = self.find_preview_icon(form_row)
        preview_button.click()

        self.assert_preview_modal(preview_img)

    def test_click_on_the_preview_button_and_image_on_modal(self):
        self.goto_add_page()
        self.load_widget()

        form_row = self.page.query_selector(".iuw-root")
        preview = self.find_widget_preview(form_row)
        self.assertFalse(preview.is_visible())

        file_input = form_row.query_selector("input[type=file]")
        file_input.set_input_files(self.image2)

        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)
        preview_img = preview.query_selector("img")
        preview_button = self.find_preview_icon(form_row)
        preview_button.click()

        self.assert_preview_modal(preview_img)
        preview_modal = self.get_preview_modal()
        img = preview_modal.query_selector("img")
        img.click()

        self.wait(0.5)
        self.assertEqual(preview_modal.get_attribute("class"), "iuw-modal visible")

    def test_click_on_the_preview_button_and_close_on_modal(self):
        self.goto_add_page()
        self.load_widget()

        form_row = self.page.query_selector(".iuw-root")
        preview = self.find_widget_preview(form_row)
        self.assertFalse(preview.is_visible())

        file_input = form_row.query_selector("input[type=file]")
        file_input.set_input_files(self.image2)

        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)
        preview_img = preview.query_selector("img")
        preview_button = self.find_preview_icon(form_row)
        preview_button.click()

        self.assert_preview_modal(preview_img)
        self.assert_preview_modal_close()

    def test_drop_label_leave(self):
        self.goto_add_page()
        self.load_widget()

        root = self.page.query_selector(".iuw-root")
        drop_label = self.find_drop_label()

        self.assertFalse(drop_label.is_visible())

        data_transfer = self.page.evaluate_handle("() => new DataTransfer()")
        root.dispatch_event("dragenter", {"dataTransfer": data_transfer})
        self.wait(0.5)

        self.assertTrue(drop_label.is_visible())

        root.dispatch_event("dragleave", {"dataTransfer": data_transfer})
        self.wait(0.5)

        self.assertFalse(drop_label.is_visible())

    def test_drop_label_drop(self):
        self.goto_add_page()
        self.load_widget()

        root = self.page.query_selector(".iuw-root")
        drop_label = self.find_drop_label()

        self.assertFalse(drop_label.is_visible())

        data_transfer = self.page.evaluate_handle("() => new DataTransfer()")
        root.dispatch_event("dragenter", {"dataTransfer": data_transfer})
        self.wait(0.5)

        self.assertTrue(drop_label.is_visible())

        root.dispatch_event("drop", {"dataTransfer": data_transfer})
        self.wait(0.5)

        self.assertFalse(drop_label.is_visible())

    def test_drop_label_end(self):
        self.goto_add_page()
        self.load_widget()

        root = self.page.query_selector(".iuw-root")
        drop_label = self.find_drop_label()

        self.assertFalse(drop_label.is_visible())

        data_transfer = self.page.evaluate_handle("() => new DataTransfer()")
        root.dispatch_event("dragenter", {"dataTransfer": data_transfer})
        self.wait(0.5)

        self.assertTrue(drop_label.is_visible())

        root.dispatch_event("dragend", {"dataTransfer": data_transfer})
        self.wait(0.5)

        self.assertFalse(drop_label.is_visible())
