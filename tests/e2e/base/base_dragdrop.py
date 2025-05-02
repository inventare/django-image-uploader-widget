
class BaseDragDropTests:
    """
    A base class with common drop label test cases.
    """

    @property
    def page_object(self):
        if hasattr(self, 'widget_po'):
            return self.widget_po
        if hasattr(self, 'inline_po'):
            return self.inline_po

    def test_drop_label_with_leave(self):
        self.goto_add_page()

        self.assertFalse(self.page_object.is_drop_label_visible())
        self.page_object.execute_dragenter()
        self.assertTrue(self.page_object.is_drop_label_visible())
        self.page_object.execute_dragleave()
        self.assertFalse(self.page_object.is_drop_label_visible())

    def test_drop_label_with_drop(self):
        self.goto_add_page()

        self.assertFalse(self.page_object.is_drop_label_visible())
        self.page_object.execute_dragenter()
        self.assertTrue(self.page_object.is_drop_label_visible())
        self.page_object.execute_drop()
        self.assertFalse(self.page_object.is_drop_label_visible())

    def test_drop_label_with_dragend(self):
        self.goto_add_page()

        self.assertFalse(self.page_object.is_drop_label_visible())
        self.page_object.execute_dragenter()
        self.assertTrue(self.page_object.is_drop_label_visible())
        self.page_object.execute_dragend()
        self.assertFalse(self.page_object.is_drop_label_visible())
