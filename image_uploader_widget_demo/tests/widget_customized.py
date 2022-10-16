from django.test import TestCase
from image_uploader_widget_demo.demo_application.forms import TestCustomForm

class WidgetCustomizedTestCase(TestCase):
    def test_render_custom_icons_and_texts(self):
        form = TestCustomForm()
        text = form.as_p()

        self.assertTrue("&lt;drop_icon&gt;" in text)
        self.assertTrue("&lt;drop_text&gt;" in text)
        self.assertTrue("&lt;empty_icon&gt;" in text)
        self.assertTrue("&lt;empty_text&gt;" in text)
