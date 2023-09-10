import django
from django.core.files import File
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import invisibility_of_element_located
from image_uploader_widget_demo.demo_application import models
from utils.tests import IUWTestCase

class InlineEditorUIRegressionTestCase(IUWTestCase):
    @property
    def admin_add_url(self):
        return self.get_url_from_path('/admin/demo_application/inline/add/')

    def get_edit_url(self, id):
        return self.get_url_from_path("/admin/demo_application/inline/%s/change/" % id)
    
    def test_empty_marker(self):
        self.selenium.get(self.admin_add_url)

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        
        self.wait(0.4)

        self.assertMatchSnapshot(root, 'in_test_empty_marker')

    def test_empty_marker_hover(self):
        self.selenium.get(self.admin_add_url)

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        empty = root.find_element(By.CSS_SELECTOR, '.iuw-empty')

        self.hover_and_wait(empty, 0.4)

        self.assertMatchSnapshot(root, 'in_test_empty_marker_hover')

    def test_with_images_data(self):
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        item2 = models.InlineItem()
        item2.parent = inline
        with open(self.image2, 'rb') as f:
            item2.image.save("image2.png", File(f))
        item2.save()

        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        self.assertMatchSnapshot(root, 'in_test_with_images_data')

    def test_with_images_hover_preview(self):
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        item2 = models.InlineItem()
        item2.parent = inline
        with open(self.image2, 'rb') as f:
            item2.image.save("image2.png", File(f))
        item2.save()

        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        preview = previews[0]

        self.hover_and_wait(preview, 0.4)
        
        self.assertMatchSnapshot(root, 'in_test_with_images_hover_preview')
    
    def test_hover_preview_icon(self):
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        item2 = models.InlineItem()
        item2.parent = inline
        with open(self.image2, 'rb') as f:
            item2.image.save("image2.png", File(f))
        item2.save()

        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        preview = previews[0]

        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')

        self.hover_and_wait(preview_button, 0.4)
        
        self.assertMatchSnapshot(root, 'in_test_hover_preview_icon')

    def test_show_preview_modal(self):
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        item2 = models.InlineItem()
        item2.parent = inline
        with open(self.image2, 'rb') as f:
            item2.image.save("image2.png", File(f))
        item2.save()

        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        preview = previews[0]

        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        self.click_and_wait(preview_button, 0.5)

        modal = self.get_preview_modal(black_overlay=True)
        
        self.assertMatchSnapshot(modal, 'in_test_show_preview_modal')

    def test_hover_delete_icon(self):
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        item2 = models.InlineItem()
        item2.parent = inline
        with open(self.image2, 'rb') as f:
            item2.image.save("image2.png", File(f))
        item2.save()

        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        preview = previews[0]

        remove_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')

        self.hover_and_wait(remove_button, 0.4)
        
        self.assertMatchSnapshot(root, 'in_test_hover_delete_icon')

    def test_hover_add_button(self):
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        item2 = models.InlineItem()
        item2.parent = inline
        with open(self.image2, 'rb') as f:
            item2.image.save("image2.png", File(f))
        item2.save()

        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        add_button = root.find_element(By.CSS_SELECTOR, '.iuw-add-image-btn')
        self.hover_and_wait(add_button, 0.4)
        
        self.assertMatchSnapshot(root, 'in_test_hover_add_button')

    def test_ui_initialized_toggle_dark_theme(self):
        major, minor, _, _, _ = django.VERSION
        if major < 4 or minor < 2:
            # Theme toggle is added in django 4.2
            # https://docs.djangoproject.com/en/4.2/releases/4.2/#django-contrib-admin
            return

        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        item2 = models.InlineItem()
        item2.parent = inline
        with open(self.image2, 'rb') as f:
            item2.image.save("image2.png", File(f))
        item2.save()

        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        self.assertMatchSnapshot(root, 'in_test_ui_initialized_toggle_dark_theme')

        toggle = self.selenium.find_element(By.CSS_SELECTOR, '#header button.theme-toggle')
        self.click_and_wait(toggle, 0.3)
        
        self.assertMatchSnapshot(root, 'in_test_ui_initialized_toggle_dark_theme2')

    def test_ui_initialized_toggle_dark_theme_inverted(self):
        self.dark_mode()

        major, minor, _, _, _ = django.VERSION
        if major < 4 or minor < 2:
            # Theme toggle is added in django 4.2
            # https://docs.djangoproject.com/en/4.2/releases/4.2/#django-contrib-admin
            return

        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        item2 = models.InlineItem()
        item2.parent = inline
        with open(self.image2, 'rb') as f:
            item2.image.save("image2.png", File(f))
        item2.save()

        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        self.assertMatchSnapshot(root, 'in_test_ui_initialized_toggle_dark_theme_inverted')

        toggle = self.selenium.find_element(By.CSS_SELECTOR, '#header button.theme-toggle')
        self.click_and_wait(toggle, 0.3)
        
        self.assertMatchSnapshot(root, 'in_test_ui_initialized_toggle_dark_theme_inverted2')
