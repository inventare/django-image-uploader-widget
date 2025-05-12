from django.test import tag

from tests.app.widget import models
from tests.pom.component import WidgetPO
from tests.utils.test_case import TestCase


class WidgetOptionalInsideTabularTestCase(TestCase):
    def test_build_new_widget(self):
        self.admin_po.navigations.goto_add_url(models.NonRequiredTabularInline)

        inlines = self.page.query_selector_all(".tabular .form-row:not(.empty-form)")
        self.assertEqual(len(inlines), 0)

        add_row = self.page.query_selector(".add-row a")
        add_row.click()
        add_row.click()

        inlines = self.page.locator(".tabular .form-row:not(.empty-form)").all()
        self.assertEqual(len(inlines), 2)

        for inline in inlines:
            po = WidgetPO(inline)
            self.assertTrue(po.is_input_empty())

            po.execute_select_image("image1.png")
            thumbs = po.get_visible_thumbnails()
            thumb = thumbs[0]
            self.assertEqual(len(thumbs), 1)
            self.assertTrue(thumb.is_valid(required=False))

        self.admin_po.change_form.submit_form()

        items = models.NonRequiredTabularInlineItem.objects.all()
        self.assertEqual(len(items), 2)
        for item in items:
            self.assertIsNotNone(item.image)
