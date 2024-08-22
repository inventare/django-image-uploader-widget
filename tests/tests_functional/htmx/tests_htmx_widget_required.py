from django.core.files import File
from django.test import tag

from tests import models, test_case


@tag("functional", "functional_widget", "widget", "htmx")
class HTMXWidgetRequiredTestCase(test_case.IUWTestCase):
    def goto_add_page(self):
        self.page.goto(f"{self.live_server_url}/test-htmx/")

    def goto_change_page(self):
        item = self.init_item()
        self.page.goto(
            f"{self.live_server_url}/test-htmx/?destination=/test-htmx-image-widget/required/{item.pk}/"
        )
        return item

    def init_item(self):
        item = models.TestRequired()
        with open(self.image1, "rb") as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item

    def load_widget(self):
        button = self.page.query_selector(".btn-load")
        button.click()
        self.wait(0.4)

    def test_should_fire_click_on_file_input_when_click_on_empty_marker(self):
        self.goto_add_page()
        self.load_widget()

        with self.assert_input_file_clicked(
            input_selector=".iuw-root input[type=file]"
        ):
            self.page.query_selector(".iuw-empty").click()

    def test_should_create_preview_and_upload_file(self):
        self.goto_add_page()
        self.load_widget()

        root = self.page.query_selector(".iuw-root")
        preview = root.query_selector(".iuw-image-preview")
        self.assertFalse(preview.is_visible())

        file_input = root.query_selector("input[type=file]")
        self.assertEqual(file_input.get_attribute("value"), None)
        file_input.set_input_files(self.image1)

        preview = root.query_selector(".iuw-image-preview")
        img = preview.query_selector("img")
        preview_button = preview.query_selector(".iuw-preview-icon")
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertIsNotNone(preview_button)

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        itens = models.TestRequired.objects.all()
        self.assertEqual(len(itens), 1)
        item = itens[0]
        self.assertIsNotNone(item.image)

    def test_should_intiialized_with_preview_when_editing(self):
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
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertTrue(item.image.url in img.get_attribute("src"))
        self.assertIsNotNone(preview_button)

    def test_should_fire_click_on_file_input_when_click_on_the_preview_image(self):
        self.goto_add_page()
        self.load_widget()

        root = self.page.query_selector(".iuw-root")
        self.assertFalse(self.find_widget_preview(root).is_visible())

        file_input = root.query_selector("input[type=file]")
        file_input.set_input_files(self.image2)

        with self.assert_input_file_clicked(
            input_selector=".iuw-root input[type=file]"
        ):
            preview = self.find_widget_preview(root)
            self.assertIsNotNone(preview)
            img = preview.query_selector("img")
            img.click()

    def test_should_open_preview_modal_when_click_on_preview_button(self):
        self.goto_add_page()
        self.load_widget()

        root = self.page.query_selector(".iuw-root")
        preview = self.find_widget_preview(root)
        self.assertFalse(preview.is_visible())
        file_input = root.query_selector("input[type=file]")
        file_input.set_input_files(self.image2)

        preview = self.find_widget_preview(root)
        self.assertIsNotNone(preview)
        preview_img = preview.query_selector("img")

        preview_button = self.find_preview_icon(preview)
        preview_button.click()

        self.assert_preview_modal(preview_img)

    def test_should_not_close_preview_modal_when_click_image_inside_it(self):
        self.goto_add_page()
        self.load_widget()

        root = self.page.query_selector(".iuw-root")
        preview = self.find_widget_preview(root)
        self.assertFalse(preview.is_visible())
        file_input = root.query_selector("input[type=file]")
        file_input.set_input_files(self.image1)

        preview = self.find_widget_preview(root)
        self.assertIsNotNone(preview.is_visible)
        preview_img = preview.query_selector("img")

        preview_button = self.find_preview_icon(preview)
        preview_button.click()

        self.assert_preview_modal(preview_img)
        preview_modal = self.get_preview_modal(True, 3000)

        img = preview_modal.query_selector("img")
        img.click()

        self.wait(0.5)

        self.assertEqual(preview_modal.get_attribute("class"), "iuw-modal visible")

    def test_should_close_preview_modal_when_click_on_close_button_inside_it(self):
        self.goto_add_page()
        self.load_widget()

        root = self.page.query_selector(".iuw-root")
        preview = self.find_widget_preview(root)
        self.assertFalse(preview.is_visible())
        file_input = root.query_selector("input[type=file]")
        file_input.set_input_files(self.image1)

        preview = self.find_widget_preview(root)
        self.assertIsNotNone(preview)
        preview_img = preview.query_selector("img")

        preview_button = self.find_preview_icon(preview)
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
