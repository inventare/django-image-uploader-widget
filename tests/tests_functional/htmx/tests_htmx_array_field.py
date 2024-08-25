import uuid

from django.core.files import File
from django.test.utils import tag

from tests import models, test_case


@tag("functional", "array_field", "htmx")
class HTMXWidgetOptionalTestCase(test_case.IUWTestCase):
    def goto_add_page(self):
        self.page.goto(
            f"{self.live_server_url}/test-htmx/?destination=/test-htmx-image-widget/array_field/"
        )

    def goto_change_page(self, *, reverse=False, only_one=False):
        self.item = self.init_item(reverse, only_one)
        self.page.goto(
            f"{self.live_server_url}/test-htmx/?destination=/test-htmx-image-widget/array_field/{self.item.pk}/"
        )
        return self.item

    def init_item(self, reverse=False, only_one=False):
        images = []

        if reverse:
            only_one = False

        instance = None
        with open(self.image1, "rb") as f1:
            self.image1_name = f"{uuid.uuid4()}.png"
            images = [*images, File(f1, self.image1_name)]

            if not only_one:
                with open(self.image2, "rb") as f2:
                    self.image2_name = f"{uuid.uuid4()}.png"
                    if reverse:
                        images = [File(f2, self.image2_name), *images]
                    else:
                        images = [*images, File(f2, self.image2_name)]

                    instance = models.TestWithArrayField.objects.create(images=images)

            else:
                instance = models.TestWithArrayField.objects.create(images=images)

        return instance

    def load_widget(self):
        button = self.page.query_selector(".btn-load")
        button.click()
        self.wait(0.4)

    def test_should_have_visible_empty_marker_when_no_images_array_field(self):
        self.goto_add_page()
        self.load_widget()

        root = self.find_inline_root()
        empty = self.find_empty_marker(root)
        add_button = self.find_add_button(root)
        self.wait(0.1)

        self.assertIsNotNone(root)
        self.assertFalse(add_button.is_visible())
        self.assertIsNotNone(empty)
        self.assertTrue(empty.is_visible())

    def test_should_fire_click_on_temporary_input_when_click_empty_marker(self):
        self.goto_add_page()
        self.load_widget()

        root = self.find_inline_root()
        empty = self.find_empty_marker(root)
        with self.assert_input_file_clicked(".temp_file"):
            empty.click()

    def test_should_create_preview_when_select_and_upload_when_submit(self):
        self.assertEqual(len(models.TestWithArrayField.objects.all()), 0)
        self.goto_add_page()
        self.load_widget()

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

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        item = models.TestWithArrayField.objects.first()
        self.assertIsNotNone(item)
        self.assertEqual(len(item.images), 2)
        for url in item.images:
            self.assertIsNotNone(url)

    def test_should_remove_preview_and_not_save_when_not_saved(self):
        self.assertEqual(len(models.TestWithArrayField.objects.all()), 0)
        self.goto_add_page()
        self.load_widget()

        root = self.find_inline_root()
        temp_file = root.query_selector(".temp_file")
        temp_file.set_input_files(self.image1)

        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        self.find_delete_icon(previews[0]).click()
        self.assertEqual(len(self.find_inline_previews(root)), 0)

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        item = models.TestWithArrayField.objects.first()
        self.assertIsNotNone(item)
        self.assertEqual(len(item.images), 0)

    def test_should_have_initialized_with_data_when_go_to_edit_page(self):
        self.goto_change_page()
        self.load_widget()

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
                self.assertTrue(self.item.images[0] in src)
            else:
                self.assertTrue(self.item.images[1] in src)

    def test_should_remove_saved_items_when_edit(self):
        self.goto_change_page()
        self.load_widget()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 2)

        for preview in previews:
            self.find_delete_icon(preview).click()

        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 0)

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        item = models.TestWithArrayField.objects.get(pk=self.item.pk)
        self.assertEqual(len(item.images), 0)

    def test_should_fire_input_click_when_click_on_preview_image(self):
        self.goto_change_page()
        self.load_widget()

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
        self.goto_change_page(only_one=True)
        self.load_widget()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        with self.assert_input_file_clicked(".temp_file"):
            add_button = self.find_add_button(root)
            self.assertTrue(add_button.is_visible())
            add_button.click()

    def test_should_open_preview_modal_when_click_preview_button(self):
        self.goto_change_page(only_one=True)
        self.load_widget()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        preview = previews[0]
        preview_img = preview.query_selector("img")
        self.find_preview_icon(preview).click()
        self.assert_preview_modal(preview_img)

    def test_should_not_close_preview_modal_when_click_image(self):
        self.goto_change_page(only_one=True)
        self.load_widget()

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
        self.goto_change_page(only_one=True)
        self.load_widget()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        preview = previews[0]
        preview_img = preview.query_selector("img")
        self.find_preview_icon(preview).click()
        self.assert_preview_modal(preview_img)
        self.assert_preview_modal_close()

    def test_should_change_image_of_item_when_change_image_on_inline(self):
        self.goto_change_page()
        self.load_widget()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
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

    def test_drop_label_leave(self):
        self.goto_add_page()
        self.load_widget()

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
        self.load_widget()

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
        self.load_widget()

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

    def test_should_initialize_order_inputs_on_page(self):
        self.goto_change_page(reverse=True)
        self.load_widget()

        root = self.find_inline_root()

        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 2)
        for index, preview in enumerate(previews):
            order_input = self.find_inline_order(preview)
            self.assertFalse(order_input.is_visible())
            self.assertEqual(order_input.input_value(), str(index + 1))

        elements = root.query_selector_all(
            ".inline-related:not(.empty-form):not(.deleted), .iuw-add-image-btn"
        )
        classes = list(map(lambda x: x.get_attribute("class"), elements))
        self.assertEqual(classes.pop(), "iuw-add-image-btn visible-by-number")

    def test_should_reorder_two_items_from_first_to_last(self):
        self.goto_add_page()
        self.load_widget()

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
        for index, preview in enumerate(previews):
            img = preview.query_selector("img")
            preview_button = self.find_preview_icon(preview)
            remove_button = self.find_delete_icon(preview)
            order_input = self.find_inline_order(preview)
            self.assertFalse(order_input.is_visible())
            self.assertEqual(order_input.input_value(), str(index + 1))
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

        # Reorder
        preview1, preview2 = previews
        preview1.hover()
        self.page.mouse.down()
        preview2.hover(position={"x": 100, "y": 10})
        self.page.mouse.up()

        order_input = self.find_inline_order(preview1)
        self.assertEqual(order_input.input_value(), "2")
        order_input = self.find_inline_order(preview2)
        self.assertEqual(order_input.input_value(), "1")

        elements = root.query_selector_all(
            ".inline-related:not(.empty-form):not(.deleted), .iuw-add-image-btn"
        )
        classes = list(map(lambda x: x.get_attribute("class"), elements))
        self.assertEqual(classes.pop(), "iuw-add-image-btn visible-by-number")

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        item = models.TestWithArrayField.objects.first()
        self.assertEqual(len(item.images), 2)
        first, second = item.images
        self.assertTrue("admin_test/image2" in first)
        self.assertFalse("admin_test/image2" in second)

    def test_should_reorder_two_items_from_last_to_first(self):
        self.goto_add_page()
        self.load_widget()

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
        for index, preview in enumerate(previews):
            img = preview.query_selector("img")
            preview_button = self.find_preview_icon(preview)
            remove_button = self.find_delete_icon(preview)
            order_input = self.find_inline_order(preview)
            self.assertFalse(order_input.is_visible())
            self.assertEqual(order_input.input_value(), str(index + 1))
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

        # Reorder
        preview1, preview2 = previews
        preview2.hover()
        self.page.mouse.down()
        preview1.hover(position={"x": 40, "y": 10})
        self.page.mouse.up()

        order_input = self.find_inline_order(preview1)
        self.assertEqual(order_input.input_value(), "2")
        order_input = self.find_inline_order(preview2)
        self.assertEqual(order_input.input_value(), "1")

        elements = root.query_selector_all(
            ".inline-related:not(.empty-form):not(.deleted), .iuw-add-image-btn"
        )
        classes = list(map(lambda x: x.get_attribute("class"), elements))
        self.assertEqual(classes.pop(), "iuw-add-image-btn visible-by-number")

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        item = models.TestWithArrayField.objects.first()
        self.assertEqual(len(item.images), 2)
        first, second = item.images
        self.assertTrue("admin_test/image2" in first)
        self.assertFalse("admin_test/image2" in second)

    def test_should_reorder_three_items(self):
        self.goto_add_page()
        self.load_widget()

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

        temp_file.set_input_files(self.image1)
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 3)

        for index, preview in enumerate(previews):
            img = preview.query_selector("img")
            preview_button = self.find_preview_icon(preview)
            remove_button = self.find_delete_icon(preview)
            order_input = self.find_inline_order(preview)
            self.assertFalse(order_input.is_visible())
            self.assertEqual(order_input.input_value(), str(index + 1))
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

        # Reorder 1 to 2
        preview1, preview2, preview3 = previews
        preview1.hover()
        self.page.mouse.down()
        preview2.hover(position={"x": 100, "y": 10})
        self.page.mouse.up()
        # Reorder 3 to 1 (now 2)
        preview3.hover()
        self.page.mouse.down()
        preview2.hover(position={"x": 40, "y": 10})
        self.page.mouse.up()

        # The currently order is 3, 2, 1

        order_input = self.find_inline_order(preview3)
        self.assertEqual(order_input.input_value(), "1")
        order_input = self.find_inline_order(preview2)
        self.assertEqual(order_input.input_value(), "2")
        order_input = self.find_inline_order(preview1)
        self.assertEqual(order_input.input_value(), "3")

        elements = root.query_selector_all(
            ".inline-related:not(.empty-form):not(.deleted), .iuw-add-image-btn"
        )
        classes = list(map(lambda x: x.get_attribute("class"), elements))
        self.assertEqual(classes.pop(), "iuw-add-image-btn visible-by-number")

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        item = models.TestWithArrayField.objects.first()
        self.assertEqual(len(item.images), 3)
        first, second, third = item.images
        self.assertFalse("admin_test/image2" in first)
        self.assertTrue("admin_test/image2" in second)
        self.assertFalse("admin_test/image2" in third)

    def test_should_reorder_with_deleted_item(self):
        self.goto_add_page()
        self.load_widget()

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

        temp_file.set_input_files(self.image1)
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 3)

        for index, preview in enumerate(previews):
            img = preview.query_selector("img")
            preview_button = self.find_preview_icon(preview)
            remove_button = self.find_delete_icon(preview)
            order_input = self.find_inline_order(preview)
            self.assertFalse(order_input.is_visible())
            self.assertEqual(order_input.input_value(), str(index + 1))
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

        # Reorder 1 to 2
        preview1, preview2, preview3 = previews
        preview1.hover()
        self.page.mouse.down()
        self.assertFalse(self.find_drop_label().is_visible())
        preview2.hover(position={"x": 100, "y": 10})
        self.page.mouse.up()

        # Currently Order Is: 2 1 3
        delete_button = self.find_delete_icon(preview2)
        delete_button.click()

        # Reorder 3 to 1
        preview3.hover()
        self.page.mouse.down()
        self.assertFalse(self.find_drop_label().is_visible())
        preview1.hover(position={"x": 40, "y": 10})
        self.page.mouse.up()

        # The currently order is 3, 1 (2 is deleted)

        order_input = self.find_inline_order(preview3)
        self.assertEqual(order_input.input_value(), "1")
        order_input = self.find_inline_order(preview1)
        self.assertEqual(order_input.input_value(), "2")

        elements = root.query_selector_all(
            ".inline-related:not(.empty-form):not(.deleted), .iuw-add-image-btn"
        )
        classes = list(map(lambda x: x.get_attribute("class"), elements))
        self.assertEqual(classes.pop(), "iuw-add-image-btn visible-by-number")

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        item = models.TestWithArrayField.objects.first()
        self.assertEqual(len(item.images), 2)
        first, second = item.images
        self.assertFalse("admin_test/image2" in first)
        self.assertFalse("admin_test/image2" in second)

    def test_should_reorder_and_delete_item(self):
        self.goto_add_page()
        self.load_widget()

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

        temp_file.set_input_files(self.image1)
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 3)

        for index, preview in enumerate(previews):
            img = preview.query_selector("img")
            preview_button = self.find_preview_icon(preview)
            remove_button = self.find_delete_icon(preview)
            order_input = self.find_inline_order(preview)
            self.assertFalse(order_input.is_visible())
            self.assertEqual(order_input.input_value(), str(index + 1))
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

        # Reorder 1 to 2
        preview1, preview2, preview3 = previews
        preview1.hover()
        self.page.mouse.down()
        self.assertFalse(self.find_drop_label().is_visible())
        preview2.hover(position={"x": 100, "y": 10})
        self.page.mouse.up()
        # Reorder 3 to 1 (now 2)
        preview3.hover()
        self.page.mouse.down()
        self.assertFalse(self.find_drop_label().is_visible())
        preview2.hover(position={"x": 40, "y": 10})
        self.page.mouse.up()

        # The currently order is 3, 2, 1

        delete = self.find_delete_icon(preview2)
        delete.click()

        order_input = self.find_inline_order(preview3)
        self.assertEqual(order_input.input_value(), "1")
        order_input = self.find_inline_order(preview1)
        self.assertEqual(order_input.input_value(), "2")

        elements = root.query_selector_all(
            ".inline-related:not(.empty-form):not(.deleted), .iuw-add-image-btn"
        )
        classes = list(map(lambda x: x.get_attribute("class"), elements))
        self.assertEqual(classes.pop(), "iuw-add-image-btn visible-by-number")

        self.submit_form("#my-widget-form")
        self.assert_success_message()

        item = models.TestWithArrayField.objects.first()
        self.assertEqual(len(item.images), 2)
        first, second = item.images
        self.assertFalse("admin_test/image2" in first)
        self.assertFalse("admin_test/image2" in second)
