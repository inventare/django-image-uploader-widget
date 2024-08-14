from django.core.files import File
from django.test import tag

from tests import models, test_case


@tag("functional", "inline", "functional_inline", "functional_inline_simple")
class InlineEditorTests(test_case.IUWTestCase):
    model = "inline"

    def init_item(self, only_one=False):
        inline = models.Inline.objects.create()

        self.item1 = models.InlineItem()
        self.item1.parent = inline
        with open(self.image1, "rb") as f:
            self.item1.image.save("image.png", File(f))
        self.item1.save()

        if not only_one:
            self.item2 = models.InlineItem()
            self.item2.parent = inline
            with open(self.image2, "rb") as f:
                self.item2.image.save("image2.png", File(f))
            self.item2.save()

        return inline

    def goto_change_page(self, only_one=False):
        item = self.init_item(only_one)
        super().goto_change_page(item.id)
        return item

    def test_should_have_visible_empty_marker_when_no_images_inline(self):
        """
        Should have a visible empty marker when no images on inline.

        The test flow is:
            - Navigate to Inline Add Page.
            - Assert if add button is hidden.
            - Assert if empty marker is visible.
        """
        self.goto_add_page()

        root = self.find_inline_root()
        empty = self.find_empty_marker(root)
        add_button = self.find_add_button(root)
        self.wait(0.1)

        self.assertIsNotNone(root)
        self.assertFalse(add_button.is_visible())
        self.assertIsNotNone(empty)
        self.assertTrue(empty.is_visible())

    def test_should_fire_click_on_temporary_input_when_click_empty_marker(self):
        """
        Should fire click on the temporary input when click on empty marker.

        The test flow is:
            - Navigate to Inline Add Page.
            - Click on the empty marker.
            - Assert if click event is fired on temporary input file.
        """
        self.goto_add_page()

        root = self.find_inline_root()
        empty = self.find_empty_marker(root)
        with self.assert_input_file_clicked(".temp_file"):
            empty.click()

    def test_should_create_preview_when_select_and_upload_when_submit(self):
        """
        Should create a preview when select file and upload it when submit.

        The test flow is:
            - Assert if None item is present on database.
            - Navigate to Inline Add Page.
            - Assert if None preview item is present on page.
            - Select first file.
            - Assert if One preview item is present on page.
            - Select second file.
            - Assert if Two preview items is present on page.
            - Assert image, preview and delete icon on each of preview itens.
            - Submit the form.
            - Assert admin success message.
            - Assert the itens on the database.
        """
        self.assertEqual(len(models.InlineItem.objects.all()), 0)
        self.goto_add_page()

        root = self.find_inline_root()
        temp_file = root.query_selector(".temp_file")

        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 0)

        temp_file.set_input_files(self.image1)
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        temp_file.set_input_files(self.image2)
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 2)

        for preview in previews:
            img = preview.query_selector("img")
            preview_button = self.find_preview_icon(preview)
            remove_button = self.find_delete_icon(preview)
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

        self.submit_form("#inline_form")
        self.assert_success_message()

        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 2)
        for item in items:
            self.assertIsNotNone(item.image)

    def test_should_remove_preview_and_not_save_when_not_saved(self):
        """
        Should remove preview and not save item when not saved.

        The test flow is:
            - Go to add page.
            - Assert if One preview item is present on page.
            - Find delete icon.
            - Click on the delete icon
            - Assert if none preview item is present on page.
            - Submit the form.
            - Assert if none item is saved.
        """
        self.assertEqual(len(models.InlineItem.objects.all()), 0)
        self.goto_add_page()

        root = self.find_inline_root()
        temp_file = root.query_selector(".temp_file")
        temp_file.set_input_files(self.image1)

        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        self.find_delete_icon(previews[0]).click()
        self.assertEqual(len(self.find_inline_previews(root)), 0)

        self.submit_form("#inline_form")
        self.assert_success_message()
        self.assertEqual(len(models.InlineItem.objects.all()), 0)

    def test_should_have_initialized_with_data_when_go_to_edit_page(self):
        """
        Should have initialized with data when go to edit page.

        The test flow is:
            - Go to Edit Page.
            - Assert if two items is present on page.
            - Assert image, preview and remove icon on each item.
        """
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
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
                self.assertTrue(self.item1.image.url in src)
            else:
                self.assertTrue(self.item2.image.url in src)

    def test_should_remove_saved_items_when_edit(self):
        """
        Should remove saved items when editing.

        The test flow is:
            - Go to Edit Page.
            - Assert if two previews is displayed.
            - Click on the Delete Icon of each Preview Item.
            - Assert if none preview is visible.
            - Assert if the hidden preview is present.
            - Assert if the checkboxes are checked.
            - Submit form.
            - Assert success message.
            - Assert if the itens are removed from database.
        """
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 2)

        for preview in previews:
            self.find_delete_icon(preview).click()

        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 0)
        previews = self.find_deleted_inline_previews(root)
        self.assertEqual(len(previews), 2)

        for preview in previews:
            self.assertTrue(preview.query_selector("input[type=checkbox]").is_checked())

        self.submit_form("#inline_form")
        self.assert_success_message()

        self.assertEqual(len(models.InlineItem.objects.all()), 0)

    def test_should_fire_input_click_when_click_on_preview_image(self):
        """
        Should fire input click when click on the preview image.

        The test flow is:
            - Go to change page.
            - Assert if the two previews is present.
            - Click on the first preview image.
            - Assert if the click event is fired.
            - Click on the second preview image.
            - Assert if the click event is fired.
        """
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 2)

        with self.assert_input_file_clicked(
            ".inline-related:not(.empty-form):not(.deleted) input[type=file]", 0
        ):
            preview = previews[0]
            img = preview.query_selector("img")
            img.click()

        with self.assert_input_file_clicked(
            ".inline-related:not(.empty-form):not(.deleted) input[type=file]", 1
        ):
            preview = previews[1]
            img = preview.query_selector("img")
            img.click()

    def test_should_fire_temp_file_click_when_click_on_add_button(self):
        """
        Should fire temporary file input click when click on the add button.

        The test flow is:
            - Go to change page.
            - Assert if the one preview is present.
            - Assert if the add button is visible.
            - Click on the add button.
            - Assert if the click event is fired on temp input.
        """
        self.goto_change_page(only_one=True)

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        with self.assert_input_file_clicked(".temp_file"):
            add_button = self.find_add_button(root)
            self.assertTrue(add_button.is_visible())
            add_button.click()

    def test_should_open_preview_modal_when_click_preview_button(self):
        """
        Should open the preview modal when click on the preview button.

        The test flow is:
            - Navigate to Change Page.
            - Assert if one preview is present.
            - Click on the preview button on the preview image.
            - Assert if the preview modal is visible.
        """
        self.goto_change_page(only_one=True)

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        preview = previews[0]
        preview_img = preview.query_selector("img")
        self.find_preview_icon(preview).click()
        self.assert_preview_modal(preview_img)

    def test_should_not_close_preview_modal_when_click_image(self):
        """
        Should not close the preview modal when click on the image on preview modal.

        The test flow is:
            - Navigate to Change Page.
            - Assert if one preview is present.
            - Click on the preview button on the preview image.
            - Assert if the preview modal is visible.
            - Click on the image inside preview modal.
            - Wait for 0.5s.
            - Assert if the preview modal is visible.
        """
        self.goto_change_page(only_one=True)

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        preview = previews[0]
        preview_img = preview.query_selector("img")
        self.find_preview_icon(preview).click()
        self.assert_preview_modal(preview_img)

        preview_modal = self.get_preview_modal(True, 3000)
        img = preview_modal.query_selector("img")
        img.click()
        self.wait(0.5)
        self.assertEqual(preview_modal.get_attribute("class"), "iuw-modal visible")

    def test_should_close_preview_modal_when_click_close_button(self):
        """
        Should close the preview modal when click on the close button.

        The test flow is:
            - Navigate to Change Page.
            - Assert if one preview is present.
            - Click on the preview button on the preview image.
            - Assert if the preview modal is visible.
            - Click on the close button of the modal.
            - Assert if the preview modal is hidden.
        """
        self.goto_change_page(only_one=True)

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        preview = previews[0]
        preview_img = preview.query_selector("img")
        self.find_preview_icon(preview).click()
        self.assert_preview_modal(preview_img)
        self.assert_preview_modal_close()

    def test_should_change_image_of_item_when_change_image_on_inline(self):
        """
        Should change the image of a item when change image by inline and save.

        The test flow is:
            - Navigate to Change Page.
            - Assert if two previews is present.
            - Change the image of the first preview item.
            - Assert if the preview src was changed.
            - Submit the form.
            - Assert success message.
            - Assert if the image was changed on model entity.
        """
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 2)

        url1 = self.item1.image.url

        preview = previews[0]
        preview_img = preview.query_selector("img")
        preview_src = preview_img.get_attribute("src")

        file_input = preview.query_selector("input[type=file]")
        file_input.set_input_files(self.image1)

        self.assertNotEqual(preview_src, preview_img.get_attribute("src"))

        self.submit_form("#inline_form")
        self.assert_success_message()

        item1 = models.InlineItem.objects.filter(pk=self.item1.pk).first()
        self.assertNotEqual(item1.image.url, url1)

    def test_drop_label_leave(self):
        self.goto_add_page()

        root = self.find_inline_root()
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

        root = self.find_inline_root()
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

        root = self.find_inline_root()
        drop_label = self.find_drop_label()

        self.assertFalse(drop_label.is_visible())

        data_transfer = self.page.evaluate_handle("() => new DataTransfer()")
        root.dispatch_event("dragenter", {"dataTransfer": data_transfer})
        self.wait(0.5)

        self.assertTrue(drop_label.is_visible())

        root.dispatch_event("dragend", {"dataTransfer": data_transfer})
        self.wait(0.5)

        self.assertFalse(drop_label.is_visible())
