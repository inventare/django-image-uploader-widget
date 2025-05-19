from tests.utils.assert_input_file_clicked import assert_input_file_clicked


class BaseEmptyMarkerTests:
    """
    A base class with common empty marker test cases.
    """

    empty_marker_file_input_selector = "input[type=file]"

    @property
    def page_object(self):
        if hasattr(self, "widget_po"):
            return self.widget_po
        if hasattr(self, "inline_po"):
            return self.inline_po

    def test_empty_marker_click(self):
        """
        click on empty marker should fire file input click.
        """
        self.goto_add_page()

        self.assertTrue(self.page_object.is_empty_marker_visible())
        with assert_input_file_clicked(
            self.page, self.empty_marker_file_input_selector
        ):
            self.page_object.execute_click_on_empty_marker()
