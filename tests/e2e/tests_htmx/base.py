import time

from tests.utils.test_case import TestCase


class HTMXTestCase(TestCase):
    skip_setup = False
    input_selector = ".iuw-root input[type=file]"

    def load_htmx_widget(self):
        button = self.page.query_selector(".btn-load")
        button.click()
        time.sleep(0.4)

    def goto_page(self):
        raise NotImplementedError()

    def setUp(self):
        super().setUp()

        if self.skip_setup:
            return

        self.goto_page()
        self.load_htmx_widget()
