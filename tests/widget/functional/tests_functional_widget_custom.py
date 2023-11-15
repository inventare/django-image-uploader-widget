from utils.tests import IUWTestCase
from tests.forms import TestCustomForm

class WidgetCustomTestCase(IUWTestCase):
    def test_render_custom_icons_and_texts(self):
        form = TestCustomForm()
        text = form.as_p()

        self.assertTrue("@drop_icon@" in text)
        self.assertTrue("@drop_text@" in text)
        self.assertTrue("@empty_icon@" in text)
        self.assertTrue("@empty_text@" in text)
