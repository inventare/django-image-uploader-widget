from django.core.files import File
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from image_uploader_widget_demo.demo_application import models
from .base import IUWTestCase

class InlineEditorTestCase(IUWTestCase):
    admin_add_url = '/admin/demo_application/inline/add/'

    def get_edit_url(self, id):
        return self.get_url("/admin/demo_application/inline/%s/change/" % id)
    
    def test_have_empty_marker(self):
        self.selenium.get(self.get_url(self.admin_add_url))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        empty = root.find_element(By.CSS_SELECTOR, '.iuw-empty')

        self.selenium.implicitly_wait(1)

        self.assertIsNotNone(empty)
        self.assertTrue(empty.is_displayed())

    def test_click_on_empty_marker(self):
        self.selenium.get(self.get_url(self.admin_add_url))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        empty = root.find_element(By.CSS_SELECTOR, '.iuw-empty')

        injected_javascript = (
            'const callback = arguments[0];'
            'const input = document.querySelector(".temp_file");'
            'input.addEventListener("click", (e) => { e.preventDefault(); alert("CLICKED"); });'
            'callback();'
        )
        self.selenium.execute_async_script(injected_javascript)

        empty.click()

        self.assertEqual(self.selenium.switch_to.alert.text, "CLICKED")

    def test_send_images(self):
        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 0)

        self.selenium.get(self.get_url(self.admin_add_url))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        temp_file = root.find_element(By.CSS_SELECTOR, '.temp_file')

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 0)

        temp_file.send_keys(self.image_file)

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 1)
        
        temp_file.send_keys(self.image_file2)

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 2)

        for preview in previews:
            img = preview.find_element(By.TAG_NAME, 'img')
            preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
            remove_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

        submit = self.selenium.find_element(By.CSS_SELECTOR, '#inline_form [type="submit"]')
        submit.click()

        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 2)
        for item in items:
            self.assertIsNotNone(item.image)

    def test_remove_not_saved_inline(self):
        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 0)

        self.selenium.get(self.get_url(self.admin_add_url))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        temp_file = root.find_element(By.CSS_SELECTOR, '.temp_file')

        temp_file.send_keys(self.image_file)

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 1)
        preview = previews[0]

        remove_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')
        
        remove_button.click()
        
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 0)

        submit = self.selenium.find_element(By.CSS_SELECTOR, '#inline_form [type="submit"]')
        submit.click()

        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 0)

    def test_initialize_inline_with_saved_data(self):
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image_file, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        item2 = models.InlineItem()
        item2.parent = inline
        with open(self.image_file2, 'rb') as f:
            item2.image.save("image2.png", File(f))
        item2.save()

        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 2)

        index = 0
        for preview in previews:
            img = preview.find_element(By.TAG_NAME, 'img')
            preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
            remove_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

            src = img.get_attribute('src')
            if index == 0:
                self.assertTrue(item1.image.url in src)
            else:
                self.assertTrue(item2.image.url in src)

            index = index + 1

    def test_remove_saved_items(self):
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image_file, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        item2 = models.InlineItem()
        item2.parent = inline
        with open(self.image_file2, 'rb') as f:
            item2.image.save("image2.png", File(f))
        item2.save()

        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 2)

        for preview in previews:
            img = preview.find_element(By.TAG_NAME, 'img')
            remove_button = preview.find_element(By.CSS_SELECTOR, '.iuw-delete-icon')

            remove_button.click()

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form).deleted')
        self.assertEqual(len(previews), 2)

        for preview in previews:
            checkbox = preview.find_element(By.CSS_SELECTOR, '[type="checkbox"]')
            self.assertTrue(checkbox.is_selected())

        submit = self.selenium.find_element(By.CSS_SELECTOR, '#inline_form [type="submit"]')
        submit.click()

        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 0)

    def test_click_on_preview_image(self):
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image_file, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 1)

        injected_javascript = (
            'const callback = arguments[0];'
            'const input = document.querySelector(".inline-related:not(.empty-form):not(.deleted) input[type=file]");'
            'input.addEventListener("click", (e) => { e.preventDefault(); alert("CLICKED"); });'
            'callback();'
        )
        self.selenium.execute_async_script(injected_javascript)

        preview = previews[0]
        img = preview.find_element(By.TAG_NAME, 'img')

        img.click()

        self.assertEqual(self.selenium.switch_to.alert.text, "CLICKED")

    def test_click_on_add_image(self):
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image_file, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 1)

        injected_javascript = (
            'const callback = arguments[0];'
            'const input = document.querySelector(".temp_file");'
            'input.addEventListener("click", (e) => { e.preventDefault(); alert("CLICKED"); });'
            'callback();'
        )
        self.selenium.execute_async_script(injected_javascript)

        add_button = root.find_element(By.CSS_SELECTOR, '.iuw-add-image-btn')
        add_button.click()

        self.assertEqual(self.selenium.switch_to.alert.text, "CLICKED")
