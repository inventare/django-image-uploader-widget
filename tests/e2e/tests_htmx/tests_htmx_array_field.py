import time

from django.test import tag
from django.urls import reverse
from playwright.sync_api import expect

from tests.app.array_field import models
from tests.e2e.base import BaseDragDropTests
from tests.pom.component import InlinePO
from tests.utils.assert_input_file_clicked import assert_input_file_clicked

from .base import HTMXTestCase


class HTMXArrayFieldWidgetTestCase(BaseDragDropTests, HTMXTestCase):
    input_selector = ".temp_file"

    def setUp(self):
        super().setUp()
        self.inline_po = InlinePO(self.page)

    def goto_page(self):
        base = reverse("htmx-base")
        destination = reverse("array")
        url = f"{base}?destination={destination}"
        self.admin_po.navigations.goto(url)

    def goto_add_page(self):
        self.goto_page()
        self.load_htmx_widget()

    def test_array_field_flow(self):
        # empty marker
        with assert_input_file_clicked(self.page, input_selector=self.input_selector):
            self.assertTrue(self.inline_po.is_empty_marker_visible())
            self.inline_po.execute_click_on_empty_marker()

        # upload file
        self.assertEqual(len(self.inline_po.get_visible_thumbnails()), 0)
        self.inline_po.execute_select_image("image1.png")
        self.inline_po.execute_select_image("image2.png")
        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)
        self.assertTrue(thumbs[0].is_valid(required=False))
        self.assertTrue(thumbs[1].is_valid(required=False))

        # click on thumb image
        selector = ".inline-related:not(.empty-form):not(.deleted) input[type=file]"
        for index, thumb in enumerate(thumbs):
            with assert_input_file_clicked(self.page, selector, index):
                thumb.execute_click_on_image()

        # preview modal
        thumbs[0].execute_click_on_preview()
        modal = self.inline_po.modal.get_visible_modal_for(thumbs[0])
        self.assertIsNotNone(modal)

        # preview modal click on image
        self.inline_po.modal.execute_click_on_image(modal)
        time.sleep(1)
        self.assertEqual(modal.get_attribute("class"), "iuw-modal visible")

        # preview modal click on close button
        self.inline_po.modal.execute_click_on_close_button(modal)
        locator = self.page.locator("#iuw-modal-element")
        expect(locator).not_to_be_visible(timeout=3000)

        # submit form and validate saved
        self.admin_po.change_form.submit_form("#my-widget-form")
        item = models.TestWithArrayField.objects.first()
        self.assertIsNotNone(item)
        self.assertEqual(len(item.images), 2)
        for url in item.images:
            self.assertIsNotNone(url)

        # goto change page
        endpoint = f"{reverse('array')}{item.pk}/"
        url = f"{self.live_server_url}{reverse('htmx-base')}?destination={endpoint}"
        self.page.goto(url)
        self.load_htmx_widget()

        thumbs = self.inline_po.get_visible_thumbnails()
        self.assertEqual(len(thumbs), 2)
        self.assertTrue(thumbs[0].is_valid(required=False))
        self.assertTrue(thumbs[1].is_valid(required=False))
        self.assertTrue(item.images[0] in thumbs[0].src)
        self.assertTrue(item.images[1] in thumbs[1].src)
        self.assertFalse(self.inline_po.is_empty_marker_visible())
