from django.contrib.auth import get_user_model
from django.core.files import File
from selenium.webdriver.common.by import By
from image_uploader_widget_demo.demo_application import models
from utils.tests import IUWTestCase

User = get_user_model()

class RequiredWidgetTestCase(IUWTestCase):
    admin_add_url = '/admin/demo_application/testrequired/add/'

    def get_edit_url(self, id):
        return self.get_url_from_path("/admin/demo_application/testrequired/%s/change/" % id)
    
    def init_item(self):
        item = models.TestRequired()
        with open(self.image1, 'rb') as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item
    
    def test_ui_empty_marker(self):
        self.selenium.get(self.get_url_from_path(self.admin_add_url))

        self.get_widget_empty_marker()
        self.waitFor(0.4)

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'required_widget_empty')

    def test_ui_empty_marker_hovered(self):
        self.selenium.get(self.get_url_from_path(self.admin_add_url))

        empty = self.get_widget_empty_marker()
        self.hoverAndWait(empty, 0.4)

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'required_widget_empty_hovered')

    def test_ui_initialized_with_data(self):
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview = self.get_widget_preview(root)
        self.hover(preview)

        self.assertMatchSnapshot(root, 'required_widget_init_with_data')

    def test_ui_initialized_with_data_hover_preview(self):
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image .iuw-root')
        preview_icon = root.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        self.hoverAndWait(preview_icon, 0.4)

        self.assertMatchSnapshot(root, 'required_widget_init_with_data_preview_hovered')

    def test_ui_initialized_with_data_preview(self):
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.form-row.field-image .iuw-root')
        preview_icon = root.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        preview_icon.click()

        self.waitFor(0.5)
        
        modal = self.get_preview_modal(black_overlay=True)
        self.assertMatchSnapshot(modal, 'test_ui_initialized_with_data_preview')
