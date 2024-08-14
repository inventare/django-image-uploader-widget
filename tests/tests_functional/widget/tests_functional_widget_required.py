from django.core.files import File
from django.test import tag

from tests import models, test_case


@tag("functional", "functional_widget", "widget")
class WidgetRequiredTests(test_case.IUWTestCase):
    model = "testrequired"

    def init_item(self):
        item = models.TestRequired()
        with open(self.image1, "rb") as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item

    def goto_change_page(self):
        item = self.init_item()
        super().goto_change_page(item.id)
        return item

    def test_should_fire_click_on_file_input_when_click_on_empty_marker(self):
        """
        Should fire click event on file input when click on the empty marker.

        The test flow is:
            - Navigate to Widget Add Page
            - Click on the empty marker
            - Assert if click event is fired on input file.
        """
        self.goto_add_page()

        with self.assert_input_file_clicked():
            self.page.query_selector(".form-row.field-image .iuw-empty").click()

    def test_should_create_preview_and_upload_file(self):
        """
        Should create a preview when select file and upload it when submit.

        The test flow is:
            - Navigate to Widget Add Page.
            - Assert if none preview is present.
            - Add file to file input.
            - Assert if the preview is added to the widget.
            - Submit the form.
            - Assert if success message is present.
            - Validate created instance.
        """
        self.goto_add_page()

        form_row = self.page.query_selector(".form-row.field-image")
        preview = form_row.query_selector(".iuw-image-preview")
        self.assertFalse(preview.is_visible())

        file_input = form_row.query_selector("input[type=file]")
        self.assertEqual(file_input.get_attribute("value"), None)
        file_input.set_input_files(self.image1)

        preview = form_row.query_selector(".iuw-image-preview")
        img = preview.query_selector("img")
        preview_button = preview.query_selector(".iuw-preview-icon")
        self.assertTrue(preview.is_visible())
        self.assertIsNotNone(img)
        self.assertIsNotNone(preview_button)

        self.submit_form("#testrequired_form")
        self.assert_success_message()

        itens = models.TestRequired.objects.all()
        self.assertEqual(len(itens), 1)
        item = itens[0]
        self.assertIsNotNone(item.image)

    def test_should_intiialized_with_preview_when_editing(self):
        """
        Should initialized with the preview when open the edit page.

        The test flow is:
            - Navigate to Widget Change Page.
            - Assert if preview is found.
            - Assert the preview data-raw attribute.
            - Assert if the empty marker is hidden.
            - Assert if the preview button is visible.
        """
        item = self.goto_change_page()

        root = self.find_widget_root()
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
        """
        Should fire click event on file input when click on the preview image.

        The test flow is:
            - Navigate to Widget Add Page.
            - Assert if Preview is not present.
            - Choice a image.
            - Click on the preview image.
            - Assert if click event is fired on input file.
        """
        self.goto_add_page()

        form_row = self.find_widget_form_row()
        self.assertFalse(self.find_widget_preview(form_row).is_visible())

        file_input = form_row.query_selector("input[type=file]")
        file_input.set_input_files(self.image2)

        with self.assert_input_file_clicked():
            preview = self.find_widget_preview(form_row)
            self.assertIsNotNone(preview)
            img = preview.query_selector("img")
            img.click()

    def test_should_open_preview_modal_when_click_on_preview_button(self):
        """
        Should open the preview modal when click on the preview button.

        The test flow is:
            - Navigate to Widget Add Page.
            - Assert if preview is not present.
            - Choice a image.
            - Assert if preview is present.
            - Click on the preview button on the preview image.
            - Assert if the preview modal is visible.
        """
        self.goto_add_page()

        form_row = self.find_widget_form_row()
        preview = self.find_widget_preview(form_row)
        self.assertFalse(preview.is_visible())
        file_input = form_row.query_selector("input[type=file]")
        file_input.set_input_files(self.image2)

        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)
        preview_img = preview.query_selector("img")

        preview_button = self.find_preview_icon(preview)
        preview_button.click()

        self.assert_preview_modal(preview_img)

    def test_should_not_close_preview_modal_when_click_image_inside_it(self):
        """
        Should not close the preview modal when click on the image inside it.

        The test flow is:
            - Navigate to Widget Add Page.
            - Assert if preview is not present.
            - Choice a image.
            - Assert if preview is present.
            - Click on the preview button on the preview image.
            - Assert if the preview modal is visible.
            - Click on the image inside preview modal.
            - Wait for 0.5 ms.
            - Assert if the preview modal is visible.
        """
        self.goto_add_page()

        form_row = self.find_widget_form_row()
        preview = self.find_widget_preview(form_row)
        self.assertFalse(preview.is_visible())
        file_input = form_row.query_selector("input[type=file]")
        file_input.set_input_files(self.image1)

        preview = self.find_widget_preview(form_row)
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
        """
        Should close the preview modal when click on close button inside it.

        The test flow is:
            - Navigate to Widget Add Page.
            - Assert if preview is not present.
            - Choice a image.
            - Assert if preview is present.
            - Click on the preview button on the preview image.
            - Assert if the preview modal is visible.
            - Click on the image inside preview modal.
            - Click on the close button.
            - Assert if the preview modal is not visible.
        """
        self.goto_add_page()

        form_row = self.find_widget_form_row()
        preview = self.find_widget_preview(form_row)
        self.assertFalse(preview.is_visible())
        file_input = form_row.query_selector("input[type=file]")
        file_input.set_input_files(self.image1)

        preview = self.find_widget_preview(form_row)
        self.assertIsNotNone(preview)
        preview_img = preview.query_selector("img")

        preview_button = self.find_preview_icon(preview)
        preview_button.click()

        self.assert_preview_modal(preview_img)
        self.assert_preview_modal_close()

    def test_drop_label_leave(self):
        self.goto_add_page()

        root = self.find_widget_root()
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

        root = self.find_widget_root()
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

        root = self.find_widget_root()
        drop_label = self.find_drop_label()

        self.assertFalse(drop_label.is_visible())

        data_transfer = self.page.evaluate_handle("() => new DataTransfer()")
        root.dispatch_event("dragenter", {"dataTransfer": data_transfer})
        self.wait(0.5)

        self.assertTrue(drop_label.is_visible())

        root.dispatch_event("dragend", {"dataTransfer": data_transfer})
        self.wait(0.5)

        self.assertFalse(drop_label.is_visible())
