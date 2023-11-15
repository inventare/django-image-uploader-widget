import django
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test.utils import tag
from selenium.webdriver.common.by import By
from tests import models
from utils.tests import IUWTestCase

User = get_user_model()

@tag("ui-regression")
class OptionaldWidgetTestCase(IUWTestCase):
    admin_add_url = '/testnonrequired/add/'

    def get_edit_url(self, id):
        return self.get_url_from_path("/testnonrequired/%s/change/" % id)
    
    def init_item(self):
        item = models.TestNonRequired()
        with open(self.image2, 'rb') as f:
            item.image.save("image.png", File(f), False)
        item.save()
        return item
    
    def test_ui_empty_marker(self):
        self.selenium.get(self.get_url_from_path(self.admin_add_url))

        self.get_widget_empty_marker()
        self.wait(0.4)

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wo_test_ui_empty_marker')

    def test_ui_empty_marker_dark(self):
        self.dark_mode()
        self.selenium.get(self.get_url_from_path(self.admin_add_url))

        self.get_widget_empty_marker()
        self.wait(0.4)

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wo_test_ui_empty_marker_dark')
        self.light_mode()

    def test_ui_empty_marker_hovered(self):
        self.selenium.get(self.get_url_from_path(self.admin_add_url))

        empty = self.get_widget_empty_marker()
        self.hover_and_wait(empty, 0.4)

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wo_test_ui_empty_marker_hovered')

    def test_ui_empty_marker_hovered_dark(self):
        self.dark_mode()
        self.selenium.get(self.get_url_from_path(self.admin_add_url))

        empty = self.get_widget_empty_marker()
        self.hover_and_wait(empty, 0.4)

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wo_test_ui_empty_marker_hovered_dark')
        self.light_mode()

    def test_ui_initialized_with_data(self):
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview = self.get_widget_preview(root)
        self.hover(preview)

        self.assertMatchSnapshot(root, 'wo_test_ui_initialized_with_data')

    def test_ui_initialized_with_data_dark(self):
        self.dark_mode()
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview = self.get_widget_preview(root)
        self.hover(preview)

        self.assertMatchSnapshot(root, 'wo_test_ui_initialized_with_data_dark')
        self.light_mode()

    def test_ui_initialized_with_data_hover_preview(self):
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview_icon = self.get_widget_preview_icon(root)
        self.hover_and_wait(preview_icon, 0.4)

        self.assertMatchSnapshot(root, 'wo_test_ui_initialized_with_data_hover_preview')

    def test_ui_initialized_with_data_hover_preview_dark(self):
        self.dark_mode()
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview_icon = self.get_widget_preview_icon(root)
        self.hover_and_wait(preview_icon, 0.4)

        self.assertMatchSnapshot(root, 'wo_test_ui_initialized_with_data_hover_preview_dark')
        self.light_mode()

    def test_ui_initialized_with_data_hover_remove(self):
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        delete_icon = self.get_widget_delete_icon(root)
        self.hover_and_wait(delete_icon, 0.4)

        self.assertMatchSnapshot(root, 'wo_test_ui_initialized_with_data_hover_remove')

    def test_ui_initialized_with_data_hover_remove_dark(self):
        self.dark_mode()
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        delete_icon = self.get_widget_delete_icon(root)
        self.hover_and_wait(delete_icon, 0.4)

        self.assertMatchSnapshot(root, 'wo_test_ui_initialized_with_data_hover_remove_dark')
        self.light_mode()

    def test_ui_initialized_with_data_preview(self):
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview_icon = self.get_widget_preview_icon(root)
        self.click_and_wait(preview_icon, 0.5)
        
        modal = self.get_preview_modal(black_overlay=True)
        self.assertMatchSnapshot(modal, 'wo_test_ui_initialized_with_data_preview')

    def test_ui_initialized_with_data_preview_dark(self):
        self.dark_mode()
        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        preview_icon = self.get_widget_preview_icon(root)
        self.click_and_wait(preview_icon, 0.5)
        
        modal = self.get_preview_modal(black_overlay=True)
        self.assertMatchSnapshot(modal, 'wo_test_ui_initialized_with_data_preview_dark')
        self.light_mode()

    def test_ui_initialized_toggle_dark_theme(self):
        self.light_mode()
        major, minor, _, _, _ = django.VERSION
        if major < 4 or minor < 2:
            # Theme toggle is added in django 4.2
            # https://docs.djangoproject.com/en/4.2/releases/4.2/#django-contrib-admin
            return

        item = self.init_item()
        self.selenium.get(self.get_edit_url(item.id))

        root = self.get_widget_root()
        self.assertMatchSnapshot(root, 'wo_test_ui_initialized_toggle_dark_theme')

        toggle = self.selenium.find_element(By.CSS_SELECTOR, '#header button.theme-toggle')
        self.click_and_wait(toggle, 0.3)
        
        self.assertMatchSnapshot(root, 'wo_test_ui_initialized_toggle_dark_theme2')

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
        self.assertMatchSnapshot(root, 'wo_test_ui_initialized_toggle_dark_theme_inverted')

        toggle = self.selenium.find_element(By.CSS_SELECTOR, '#header button.theme-toggle')
        self.click_and_wait(toggle, 0.3)
        
        self.assertMatchSnapshot(root, 'wo_test_ui_initialized_toggle_dark_theme_inverted2')
        self.light_mode()
