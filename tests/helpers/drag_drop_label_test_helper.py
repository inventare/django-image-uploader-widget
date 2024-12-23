import time

from playwright.sync_api import Page


class DragDropLabelTestHelper:
    root_selector = ".iuw-root"
    drop_label_selector = ".iuw-drop-label"

    @property
    def root(self):
        """The widget root element."""
        return self.page.query_selector(self.root_selector)

    @property
    def data_transfer(self):
        """A empty DataTransfer created using using evaluate_handle()."""
        return self.page.evaluate_handle("() => new DataTransfer()")

    @property
    def drop_label(self):
        """The drop label of the widget."""
        return self.page.query_selector(self.drop_label_selector)

    def __init__(self, page: Page, root_selector: str):
        """Creates a new instance of DragDropLabelTestHelper.

        Args:
            page: a playwright `Page`.
            root_selector: a css selector of the widget root.
        """
        self.page = page
        self.root_selector = root_selector

    def execute_drag_leave_event(self):
        """Executes a partial test-case of drop label using drag leave event.

        Assert if drop_label is hidden, then dispatch a dragenter event, assert if drop_label
        is visible, and, for last, dispatch dragleave and assert if drop_label is hidden.
        """
        # is hidden
        assert not self.drop_label.is_visible()
        # enter
        self.root.dispatch_event("dragenter", {"dataTransfer": self.data_transfer})
        time.sleep(0.5)
        # goes to visible
        assert self.drop_label.is_visible()
        # leave
        self.root.dispatch_event("dragleave", {"dataTransfer": self.data_transfer})
        time.sleep(0.5)
        # goes to hidden
        assert not self.drop_label.is_visible()

    def execute_drag_end_event(self):
        """Executes a partial test-case of drop label using drag end event.

        Assert if drop_label is hidden, then dispatch a dragenter event, assert if drop_label
        is visible, and, for last, dispatch dragend and assert if drop_label is hidden.
        """
        # is hidden
        assert not self.drop_label.is_visible()
        # enter
        self.root.dispatch_event("dragenter", {"dataTransfer": self.data_transfer})
        time.sleep(0.5)
        # goes to visible
        assert self.drop_label.is_visible()
        # end
        self.root.dispatch_event("dragend", {"dataTransfer": self.data_transfer})
        time.sleep(0.5)
        # goes to hidden
        assert not self.drop_label.is_visible()

    def execute_drop_event(self):
        """Executes a partial test-case of drop label using drop event.

        Assert if drop_label is hidden, then dispatch a dragenter event, assert if drop_label
        is visible, and, for last, dispatch drop and assert if drop_label is hidden.
        """
        # is hidden
        assert not self.drop_label.is_visible()
        # enter
        self.root.dispatch_event("dragenter", {"dataTransfer": self.data_transfer})
        time.sleep(0.5)
        # goes to visible
        assert self.drop_label.is_visible()
        # drop
        self.root.dispatch_event("drop", {"dataTransfer": self.data_transfer})
        time.sleep(0.5)
        # goes to hidden
        assert not self.drop_label.is_visible()


class DragDropLabelTestCaseMixin:
    def test_drag_drop_label_flow(self):
        """Test full drag and drop label flow."""
        helper = DragDropLabelTestHelper(self.page, self.root_selector)

        self.goto_add_page()
        helper.execute_drag_leave_event()
        helper.execute_drag_end_event()
        helper.execute_drop_event()
