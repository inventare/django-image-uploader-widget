from typing import Callable, List

from playwright.sync_api import ElementHandle, Page

from tests.mixins.image_mock_mixin import ImageMockMixin


class ReorderTestHelper(ImageMockMixin):
    root_selector = ".iuw-inline-root"
    temp_input_selector = ".temp_file"
    previews_selector = ".inline-related:not(.empty-form):not(.deleted)"
    order_input_selector = 'input[name$="order"]'
    preview_icon_selector = ".iuw-preview-icon"
    delete_icon_selector = ".iuw-delete-icon"
    form_selector = 'form[enctype="multipart/form-data"]'
    drop_label_selector = ".iuw-drop-label"

    get_images_to_validate: Callable[[], List[str]] = None

    @property
    def root(self):
        """The widget root element."""
        return self.page.query_selector(self.root_selector)

    @property
    def temp_input(self):
        """The temporary file input, used to upload new images."""
        return self.root.query_selector(self.temp_input_selector)

    @property
    def drop_label(self):
        """The drop label of the widget."""
        return self.root.query_selector(self.drop_label_selector)

    @property
    def previews(self):
        """The widget preview elements."""
        return self.root.query_selector_all(self.previews_selector)

    def __init__(
        self,
        page: Page,
        root_selector: str,
        get_images_to_validate: Callable[[], List[str]],
    ):
        """Creates a new instance of ReorderTestHelper.

        Args:
            page: a playwright `Page`.
            root_selector: a css selector of the widget root.
            get_images_to_validate: a callable function to return the
                images ordered to made assertions.
        """
        self.page = page
        self.root_selector = root_selector
        self.get_images_to_validate = get_images_to_validate

    def upload_file(self, file: str):
        """Upload a file to temp file input."""
        self.temp_input.set_input_files(file)

    def wait_for_success_message(self):
        """Wait and assert for the success message on the django-admin."""
        self.page.wait_for_selector(".messagelist .success", timeout=3000)

    def submit_form(self):
        """Submit the form by clicking on an button or input with type=submit."""
        submit = self.page.query_selector(f'{self.form_selector} [type="submit"]')
        submit.click()
        self.wait_for_success_message()

    def get_order_input(self, preview: ElementHandle):
        """Get the order input of the preview item.

        Args:
            preview: The preview item element.

        Returns:
            a `ElementHandle` that represents the order input, or None if it
            was not found.
        """
        return preview.query_selector(self.order_input_selector)

    def get_preview_icon(self, preview: ElementHandle):
        """Get the preview icon (to open modal) of the preview item.

        Args:
            preview: The preview item element.

        Returns:
            a `ElementHandle` that represents the preview icon, or None if it
            was not found.
        """
        return preview.query_selector(self.preview_icon_selector)

    def get_delete_icon(self, preview: ElementHandle):
        """Get the delete icon of the preview item.

        Args:
            preview: The preview item element.

        Returns:
            a `ElementHandle` that represents the delete icon, or None if it
            was not found.
        """
        return preview.query_selector(self.delete_icon_selector)

    def execute_upload_two_items_and_not_reorder(self):
        """Execute a partial test-case of upload two images and not reorder it.

        Upload the `image1` and `image2` properties and, then, assert if length of
        preview elements is two. Assert if image, preview button, remove button and
        order input is ok. Then, submit the form and validate the saved images and
        the order.
        """
        self.upload_file(self.image1)
        self.upload_file(self.image2)
        assert len(self.previews) == 2

        for index, preview in enumerate(self.previews):
            img = preview.query_selector("img")
            preview_button = self.get_preview_icon(preview)
            remove_button = self.get_delete_icon(preview)
            order_input = self.get_order_input(preview)
            assert order_input.is_visible() == False
            assert order_input.input_value() == str(index + 1)
            assert img is not None
            assert preview_button is not None
            assert remove_button is not None

        self.submit_form()

        images = self.get_images_to_validate()
        assert len(images) == 2
        assert "admin_test/image2" not in images[0]
        assert "admin_test/image2" in images[1]

    def execute_reorder_two_items_from_first_to_last(self):
        """Execute a partial test-case of upload two images and reorder it from first to last.

        Upload the `image1` and `image2` properties and, then, drag the first to the right side
        of the second and assert is the reordering is ok. Then, submit the form and validate the
        saved images and the order.
        """
        self.upload_file(self.image1)
        self.upload_file(self.image2)

        preview1, preview2 = self.previews
        preview1.hover()
        self.page.mouse.down()
        preview2.hover(position={"x": 100, "y": 10})
        self.page.mouse.up()

        preview1_order = self.get_order_input(preview1).input_value()
        preview2_order = self.get_order_input(preview2).input_value()
        assert preview1_order == "2"
        assert preview2_order == "1"

        self.submit_form()

        images = self.get_images_to_validate()
        assert len(images) == 2
        assert "admin_test/image2" in images[0]
        assert "admin_test/image2" not in images[1]

    def execute_reorder_two_items_from_last_to_first(self):
        """Execute a partial test-case of upload two images and reorder it from last to first.

        Upload the `image1` and `image2` properties and, then, drag the second to the left side
        of the first and assert is the reordering is ok. Then, submit the form and validate the
        saved images and the order.
        """
        self.upload_file(self.image1)
        self.upload_file(self.image2)

        preview1, preview2 = self.previews
        preview2.hover()
        self.page.mouse.down()
        preview1.hover(position={"x": 40, "y": 10})
        self.page.mouse.up()

        preview1_order = self.get_order_input(preview1).input_value()
        preview2_order = self.get_order_input(preview2).input_value()
        assert preview1_order == "2"
        assert preview2_order == "1"

        self.submit_form()

        images = self.get_images_to_validate()
        assert len(images) == 2
        assert "admin_test/image2" in images[0]
        assert "admin_test/image2" not in images[1]

    def execute_reorder_three_items(self):
        """Execute a partial test-case of upload three images and reorder it.

        Upload `image1`, `image2` and `image1` properties, then reorder first to second
        and, then, reorder three to first. The last ordering status is: 3, 2, 1. Then
        assert if the reordering is ok. For last, submit the form and validate the
        saved images and the order.
        """
        self.upload_file(self.image1)
        self.upload_file(self.image2)
        self.upload_file(self.image1)

        # Reorder 1 to 2
        preview1, preview2, preview3 = self.previews
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

        preview1_order = self.get_order_input(preview1).input_value()
        preview2_order = self.get_order_input(preview2).input_value()
        preview3_order = self.get_order_input(preview3).input_value()
        assert preview3_order == "1"
        assert preview2_order == "2"
        assert preview1_order == "3"

        self.submit_form()

        images = self.get_images_to_validate()
        assert len(images) == 3
        assert "admin_test/image2" not in images[0]
        assert "admin_test/image2" in images[1]
        assert "admin_test/image2" not in images[2]

    def execute_reorder_with_deleted_item(self):
        """Execute a partial test-case of reorder with deleted image.

        Upload `image1`, `image2` and `image1` properties, then reorder first to second
        and. Then, delete the second image. Reorder three to first. The last ordering
        status is: 3, 1 (2 is deleted). Then assert if the reordering is ok. For last,
        submit the form and validate the saved images and the order.
        """
        self.upload_file(self.image1)
        self.upload_file(self.image2)
        self.upload_file(self.image1)

        # Reorder 1 to 2
        preview1, preview2, preview3 = self.previews
        preview1.hover()
        self.page.mouse.down()
        assert not self.drop_label.is_visible()
        preview2.hover(position={"x": 100, "y": 10})
        self.page.mouse.up()
        # Currently Order Is: 2 1 3
        delete_button = self.get_delete_icon(preview2)
        delete_button.click()
        # Reorder 3 to 1
        preview3.hover()
        self.page.mouse.down()
        assert not self.drop_label.is_visible()
        preview1.hover(position={"x": 40, "y": 10})
        self.page.mouse.up()

        # The currently order is 3, 1 (2 is deleted)

        preview3_order = self.get_order_input(preview3).input_value()
        preview1_order = self.get_order_input(preview1).input_value()
        assert preview3_order == "1"
        assert preview1_order == "2"

        self.submit_form()

        images = self.get_images_to_validate()
        assert len(images), 2
        assert "admin_test/image2" not in images[0]
        assert "admin_test/image2" not in images[1]

    def execute_reorder_and_delete_item(self):
        """Execute a partial test-case of reorder and, then, delete image.

        Upload `image1`, `image2` and `image1` properties, then reorder first to second
        and. Reorder three to first. The last ordering status is: 3, 2, 1. Delete the
        second image. Then assert if the reordering is ok. For last, submit the form
        and validate the saved images and the order.
        """
        self.upload_file(self.image1)
        self.upload_file(self.image2)
        self.upload_file(self.image1)

        # Reorder 1 to 2
        preview1, preview2, preview3 = self.previews
        preview1.hover()
        self.page.mouse.down()
        assert not self.drop_label.is_visible()
        preview2.hover(position={"x": 100, "y": 10})
        self.page.mouse.up()
        # Reorder 3 to 1 (now 2)
        preview3.hover()
        self.page.mouse.down()
        assert not self.drop_label.is_visible()
        preview2.hover(position={"x": 40, "y": 10})
        self.page.mouse.up()

        # The currently order is 3, 2, 1
        delete = self.get_delete_icon(preview2)
        delete.click()

        preview3_order = self.get_order_input(preview3).input_value()
        preview1_order = self.get_order_input(preview1).input_value()
        assert preview3_order == "1"
        assert preview1_order == "2"

        self.submit_form()

        images = self.get_images_to_validate()
        assert len(images) == 2
        assert "admin_test/image2" not in images[0]
        assert "admin_test/image2" not in images[1]

    def execute_initialized_item(self):
        """Execute a partial test of initialized fields of a change form."""
        assert len(self.previews) == 2
        for index, preview in enumerate(self.previews):
            order_input = self.get_order_input(preview)
            assert not order_input.is_visible()
            assert order_input.input_value() == str(index + 1)


class ReorderTestCaseMixin:
    def get_images(self) -> List[str]:
        return []

    def test_reorder_flow(self):
        """Test full reorder flow with various add pages."""
        helper = ReorderTestHelper(self.page, ".iuw-inline-root", self.get_images)
        self.goto_add_page()
        helper.execute_upload_two_items_and_not_reorder()
        self.goto_add_page()
        helper.execute_reorder_two_items_from_first_to_last()
        self.goto_add_page()
        helper.execute_reorder_two_items_from_last_to_first()
        self.goto_add_page()
        helper.execute_reorder_three_items()
        self.goto_add_page()
        helper.execute_reorder_with_deleted_item()
        self.goto_add_page()
        helper.execute_reorder_and_delete_item()
        self.goto_change_page()
        helper.execute_initialized_item()
