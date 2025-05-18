import time

from django.test import tag
from django.urls import reverse
from playwright.sync_api import expect

from tests.app.widget import models
from tests.e2e.base import BaseDragDropTests
from tests.pom.component import WidgetPO
from tests.utils.assert_input_file_clicked import assert_input_file_clicked

from .base import HTMXTestCase


class HTMXOptionalWidgetTests(BaseDragDropTests, HTMXTestCase):
    def setUp(self):
        super().setUp()
        self.widget_po = WidgetPO(self.page)

    def goto_page(self):
        base = reverse("htmx-base")
        destination = reverse("optional")
        url = f"{base}?destination={destination}"
        self.admin_po.navigations.goto(url)

    def goto_add_page(self):
        self.goto_page()
        self.load_htmx_widget()

    def test_optional_widget_flow(self):
        # empty marker
        with assert_input_file_clicked(self.page, input_selector=self.input_selector):
            self.assertTrue(self.widget_po.is_empty_marker_visible())
            self.widget_po.execute_click_on_empty_marker()

        # upload file
        self.assertEqual(len(self.widget_po.get_visible_thumbnails()), 0)
        self.widget_po.execute_select_image("image1.png")
        thumbs = self.widget_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 1)
        self.assertTrue(thumbs[0].is_valid(required=False))

        # click on thumb image
        with assert_input_file_clicked(self.page, input_selector=self.input_selector):
            thumbs[0].execute_click_on_image()

        # preview modal
        thumbs[0].execute_click_on_preview()
        modal = self.widget_po.modal.get_visible_modal_for(thumbs[0])
        self.assertIsNotNone(modal)

        # preview modal click on image
        self.widget_po.modal.execute_click_on_image(modal)
        time.sleep(1)
        self.assertEqual(modal.get_attribute("class"), "iuw-modal visible")

        # preview modal click on close button
        self.widget_po.modal.execute_click_on_close_button(modal)
        locator = self.page.locator("#iuw-modal-element")
        expect(locator).not_to_be_visible(timeout=3000)

        # submit form and validate saved
        self.admin_po.change_form.submit_form("#my-widget-form")
        items = models.NonRequired.objects.all()
        self.assertEqual(len(items), 1)
        self.item = items[0]
        self.assertIsNotNone(self.item.image)

        # goto change page
        endpoint = f"{reverse('optional')}{self.item.pk}/"
        url = f"{self.live_server_url}{reverse('htmx-base')}?destination={endpoint}"
        self.page.goto(url)
        self.load_htmx_widget()

        thumb, *_ = self.widget_po.get_visible_thumbnails()
        self.assertEqual(self.widget_po.data_raw, self.item.image.url)
        self.assertFalse(self.widget_po.is_empty_marker_visible())
        self.assertTrue(thumb.is_valid(required=False))
