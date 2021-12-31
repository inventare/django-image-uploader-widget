import re
from django.test import TestCase
from .forms import get_form

class RenderWidgetTestCase(TestCase):
    """
    Test widget with required field.
    """
    root_class_name = 'iuw-root'
    drop_label_class_name = 'iuw-drop-label'
    empty_label_class_name = 'iuw-empty'

    def setUp(self):
        self.form = get_form(True)
        self.rendered = str(self.form)

        self.root_regex = 'class=".*%s.*"' % self.root_class_name
        self.drop_label_regex = 'class=".*%s.*"' % self.drop_label_class_name
        self.empty_label_regex = 'class=".*%s.*"' % self.empty_label_class_name
        self.file_input_regex = '<input.*type="file".*'
        self.checkbox_input_regex = '<input.*type="checkbox".*'
    
    def test_render_widget_elements(self):
        """
        Test if rendered widget contains the needed elements.
        """
        self.assertEqual(1, len(re.findall(self.root_regex, self.rendered)))
        self.assertEqual(1, len(re.findall(self.drop_label_regex, self.rendered)))
        self.assertEqual(1, len(re.findall(self.empty_label_regex, self.rendered)))
        self.assertEqual(1, len(re.findall(self.file_input_regex, self.rendered)))
        self.assertEqual(0, len(re.findall(self.checkbox_input_regex, self.rendered)))
