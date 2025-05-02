import time

class WidgetDragPO:
    @property
    def data_transfer(self):
        return self.page.evaluate_handle("() => new DataTransfer()")

    def execute_dragenter(self):
        self.page_elements.root.dispatch_event("dragenter", {"dataTransfer": self.data_transfer})
        time.sleep(0.5)

    def execute_dragleave(self):
        self.page_elements.root.dispatch_event("dragleave", {"dataTransfer": self.data_transfer})
        time.sleep(0.5)

    def execute_drop(self):
        self.page_elements.root.dispatch_event("drop", {"dataTransfer": self.data_transfer})
        time.sleep(0.5)

    def execute_dragend(self):
        self.page_elements.root.dispatch_event("drop", {"dataTransfer": self.data_transfer})
        time.sleep(0.5)

    def is_drop_label_visible(self):
        return self.page_elements.drop_label.is_visible()
