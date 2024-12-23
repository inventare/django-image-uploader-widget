from tests.test_case import IUWTestCase


class HTMXTestCase(IUWTestCase):
    input_selector = ".iuw-root input[type=file]"
    root_selector = ".iuw-root"
    skip_setup = False

    def load_htmx_widget(self):
        """
        Select a button with .btn-load class and click on it and, then, wait for 0.4s.
        """
        button = self.page.query_selector(".btn-load")
        button.click()
        self.wait(0.4)

    def goto_page(self):
        raise NotImplementedError("goto_page() should be implemented.")

    def setUp(self):
        super().setUp()
        if self.skip_setup:
            return

        self.goto_page()
        self.load_htmx_widget()

        self.root = self.page.query_selector(self.root_selector)
