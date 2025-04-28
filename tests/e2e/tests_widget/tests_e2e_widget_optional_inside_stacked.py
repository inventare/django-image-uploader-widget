from django.test import tag
from tests.utils.test_case import TestCase
from tests.app.widget import models
from tests.pom.widget_common import WidgetCommonPO

@tag('new')
class WidgetOptionalInsideStakcedTestCase(TestCase):
    def test_build_new_widget(self):
        self.admin_po.navigations.goto_add_url(models.NonRequiredStackedInline)

        inlines = self.page.query_selector_all(".inline-related:not(.empty-form)")
        self.assertEqual(len(inlines), 0)

        add_row = self.page.query_selector(".add-row a")
        add_row.click()
        add_row.click()

        inlines = self.page.locator(".inline-related:not(.empty-form)").all()
        self.assertEqual(len(inlines), 2)

        for inline in inlines:
            po = WidgetCommonPO(inline)
            self.assertTrue(po.is_input_empty())

            po.send_image_to_input("image1.png")
            previews = po.get_visible_previews()
            preview = previews[0]

            self.assertEqual(len(previews), 1)
            self.assertTrue(po.is_preview_valid(preview, required=False))

        self.admin_po.change_form.submit_form()

        items = models.NonRequiredStackedInlineItem.objects.all()
        self.assertEqual(len(items), 2)
        for item in items:
            self.assertIsNotNone(item.image)
