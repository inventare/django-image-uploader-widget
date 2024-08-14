from django.test import tag

from tests import test_case


@tag("functional", "inline", "functional_inline")
class CustomizedInlineEditorTestCase(test_case.IUWTestCase):
    model = "custominline"

    def test_have_customized_itens(self):
        self.goto_add_page()

        root = self.find_inline_root()
        empty = self.find_empty_marker(root)
        dropzone = self.find_drop_zone(root)
        add = self.find_add_button(root)

        empty_text = empty.text_content().strip().replace(" ", "").replace("\n", "")
        dropzone_text = (
            dropzone.text_content().strip().replace(" ", "").replace("\n", "")
        )
        add_text = add.text_content().strip().replace(" ", "").replace("\n", "")

        self.assertEqual(empty_text, "empty_icon" + "empty_text")
        self.assertEqual(dropzone_text, "drop_icon" + "drop_text")
        self.assertEqual(add_text, "add_icon" + "add_image_text")
