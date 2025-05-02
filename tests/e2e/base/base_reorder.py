from django.test import tag
from typing import List
from tests.pom.django_admin import DjangoAdminPO
from tests.pom.component import InlinePO

class BaseReorderTests:
    inline_po: InlinePO
    admin_po: DjangoAdminPO

    def get_images_to_validate(self) -> List[str]:
        raise NotImplementedError()

    def goto_add_page():
        raise NotImplementedError()

    def test_upload_images_validate_order(self):
        self.goto_add_page()
        self.inline_po.execute_select_image("image1.png")
        self.inline_po.execute_select_image("image2.png")

        thumbs = self.inline_po.get_visible_thumbnails()

        self.assertEqual(len(thumbs), 2)

        for index, thumb in enumerate(thumbs):
            self.assertTrue(thumb.is_order_input_valid(index + 1))

        self.admin_po.change_form.submit_form()

        images = self.get_images_to_validate()
        self.assertEqual(len(images), 2)
        self.assertTrue("admin_test/image2" not in images[0])
        self.assertTrue("admin_test/image2" in images[1])

    def test_reorder_from_first_to_last(self):
        self.goto_add_page()
        self.inline_po.execute_select_image("image1.png")
        self.inline_po.execute_select_image("image2.png")

        thumb1, thumb2 = self.inline_po.get_visible_thumbnails()
        src1 = thumb1.src
        src2 = thumb2.src

        thumb1.execute_move_to(thumb2, to_left=False)

        self.assertTrue(thumb1.is_order_input_valid("1"))
        self.assertTrue(thumb2.is_order_input_valid("2"))
        self.assertEqual(src1, thumb2.src)
        self.assertEqual(src2, thumb1.src)

        self.admin_po.change_form.submit_form()

        images = self.get_images_to_validate()
        self.assertEqual(len(images), 2)
        self.assertTrue("admin_test/image2" in images[0])
        self.assertTrue("admin_test/image2" not in images[1])

    def test_reorder_from_last_to_first(self):
        self.goto_add_page()
        self.inline_po.execute_select_image("image1.png")
        self.inline_po.execute_select_image("image2.png")

        thumb1, thumb2 = self.inline_po.get_visible_thumbnails()
        src1 = thumb1.src
        src2 = thumb2.src
        thumb2.execute_move_to(thumb1, to_left=True)

        self.assertTrue(thumb1.is_order_input_valid("1"))
        self.assertTrue(thumb2.is_order_input_valid("2"))
        self.assertEqual(src1, thumb2.src)
        self.assertEqual(src2, thumb1.src)

        self.admin_po.change_form.submit_form()

        images = self.get_images_to_validate()
        assert len(images) == 2
        assert "admin_test/image2" in images[0]
        assert "admin_test/image2" not in images[1]

    def test_reorder_three_items(self):
        self.goto_add_page()
        self.inline_po.execute_select_image("image1.png")
        self.inline_po.execute_select_image("image2.png")
        self.inline_po.execute_select_image("image3.png")

        thumb1, thumb2, thumb3 = self.inline_po.get_visible_thumbnails()
        src1 = thumb1.src
        src2 = thumb2.src
        src3 = thumb3.src

        # Reorder 1 to 2
        thumb1.execute_move_to(thumb2, to_left=False)
        # Reorder 3 to 2
        thumb3.execute_move_to(thumb2, to_left=True)

        thumb1.is_order_input_valid(1)
        thumb2.is_order_input_valid(2)
        thumb3.is_order_input_valid(3)

        self.assertEqual(src1, thumb3.src)
        self.assertEqual(src2, thumb1.src)
        self.assertEqual(src3, thumb2.src)

        self.admin_po.change_form.submit_form()

        images = self.get_images_to_validate()
        self.assertEqual(len(images), 3)
        self.assertTrue("admin_test/image1" in images[2])
        self.assertTrue("admin_test/image2" in images[0])
        self.assertTrue("admin_test/image3" in images[1])

    def test_reorder_with_deleted_item(self):
        self.goto_add_page()
        self.inline_po.execute_select_image("image1.png")
        self.inline_po.execute_select_image("image2.png")
        self.inline_po.execute_select_image("image3.png")

        thumb1, thumb2, thumb3 = self.inline_po.get_visible_thumbnails()
        src1 = thumb1.src
        src3 = thumb3.src

        thumb1.execute_move_to(thumb2, to_left=False)
        thumb1.execute_click_on_delete()

        thumb1, thumb2 = self.inline_po.get_visible_thumbnails()
        thumb2.execute_move_to(thumb1, to_left=True)

        self.assertTrue(thumb1.is_order_input_valid(1))
        self.assertTrue(thumb2.is_order_input_valid(2))

        self.assertEqual(src3, thumb1.src)
        self.assertEqual(src1, thumb2.src)

        self.admin_po.change_form.submit_form()

        images = self.get_images_to_validate()
        self.assertEqual(len(images), 2)
        self.assertTrue("admin_test/image1" in images[1])
        self.assertTrue("admin_test/image3" in images[0])

    def test_reorder_and_delete_item(self):
        self.goto_add_page()
        self.inline_po.execute_select_image("image1.png")
        self.inline_po.execute_select_image("image2.png")
        self.inline_po.execute_select_image("image3.png")

        thumb1, thumb2, thumb3 = self.inline_po.get_visible_thumbnails()
        src1 = thumb1.src
        src3 = thumb3.src

        thumb1.execute_move_to(thumb2, to_left=False)
        thumb3.execute_move_to(thumb1, to_left=True)

        thumb2.execute_click_on_delete()

        self.assertTrue(thumb1.is_order_input_valid(1))
        self.assertTrue(thumb2.is_order_input_valid(2))
        self.assertEqual(thumb1.src, src3)
        self.assertEqual(thumb2.src, src1)

        self.admin_po.change_form.submit_form()

        images = self.get_images_to_validate()
        self.assertEqual(len(images), 2)
        self.assertTrue("admin_test/image3" in images[0])
        self.assertTrue("admin_test/image1" in images[1])

    def test_initialized_order_inputs(self):
        self.goto_change_page()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)
        for index, thumb in enumerate(thumbs):
            self.assertTrue(thumb.is_order_input_valid(index + 1))
