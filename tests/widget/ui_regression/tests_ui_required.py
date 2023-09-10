import django
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
        self.wait(0.4)

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wr_test_ui_empty_marker')

    def test_ui_empty_marker_dark(self):
        self.dark_mode()
        self.selenium.get(self.get_url_from_path(self.admin_add_url))

        self.get_widget_empty_marker()
        self.wait(0.4)

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wr_test_ui_empty_marker_dark')

    def test_ui_empty_marker_hovered(self):
        self.selenium.get(self.get_url_from_path(self.admin_add_url))

        empty = self.get_widget_empty_marker()
        self.hover_and_wait(empty, 0.4)

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wr_test_ui_empty_marker_hovered')

    def test_ui_empty_marker_hovered_dark(self):
        self.dark_mode()
        self.selenium.get(self.get_url_from_path(self.admin_add_url))

        empty = self.get_widget_empty_marker()
        self.hover_and_wait(empty, 0.4)

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wr_test_ui_empty_marker_hovered_dark')

    def test_ui_initialized_with_data(self):
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview = self.get_widget_preview(root)
        self.hover(preview)

        self.assertMatchSnapshot(root, 'wr_test_ui_initialized_with_data')

    def test_ui_initialized_with_data_dark(self):
        self.dark_mode()
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview = self.get_widget_preview(root)
        self.hover(preview)

        self.assertMatchSnapshot(root, 'wr_test_ui_initialized_with_data_dark')

    def test_ui_initialized_with_data_hover_preview(self):
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview_icon = self.get_widget_preview_icon(root)
        self.hover_and_wait(preview_icon, 0.4)

        self.assertMatchSnapshot(root, 'wr_test_ui_initialized_with_data_hover_preview')

    def test_ui_initialized_with_data_hover_preview_dark(self):
        self.dark_mode()
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview_icon = self.get_widget_preview_icon(root)
        self.hover_and_wait(preview_icon, 0.4)

        self.assertMatchSnapshot(root, 'wr_test_ui_initialized_with_data_hover_preview_dark')

    def test_ui_initialized_with_data_preview(self):
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview_icon = self.get_widget_preview_icon(root)
        self.click_and_wait(preview_icon, 0.5)
        
        modal = self.get_preview_modal(black_overlay=True)
        self.assertMatchSnapshot(modal, 'wr_test_ui_initialized_with_data_preview')

    def test_ui_initialized_with_data_preview_dark(self):
        self.dark_mode()
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview_icon = self.get_widget_preview_icon(root)
        self.click_and_wait(preview_icon, 0.5)
        
        modal = self.get_preview_modal(black_overlay=True)
        self.assertMatchSnapshot(modal, 'wr_test_ui_initialized_with_data_preview_dark')

    def test_ui_initialized_toggle_dark_theme(self):
        major, minor, _, _, _ = django.VERSION
        if major < 4 or minor < 2:
            # Theme toggle is added in django 4.2
            # https://docs.djangoproject.com/en/4.2/releases/4.2/#django-contrib-admin
            return

        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wr_test_ui_initialized_toggle_dark_theme')

        toggle = self.selenium.find_element(By.CSS_SELECTOR, '#header button.theme-toggle')
        self.click_and_wait(toggle, 0.3)
        
        self.assertMatchSnapshot(root, 'wr_test_ui_initialized_toggle_dark_theme2')

    def test_ui_initialized_toggle_dark_theme_inverted(self):
        self.dark_mode()

        major, minor, _, _, _ = django.VERSION
        if major < 4 or minor < 2:
            # Theme toggle is added in django 4.2
            # https://docs.djangoproject.com/en/4.2/releases/4.2/#django-contrib-admin
            return

        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wr_test_ui_initialized_toggle_dark_theme_inverted')

        toggle = self.selenium.find_element(By.CSS_SELECTOR, '#header button.theme-toggle')
        self.click_and_wait(toggle, 0.3)
        
        self.assertMatchSnapshot(root, 'wr_test_ui_initialized_toggle_dark_theme_inverted2')
