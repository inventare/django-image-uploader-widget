from django.core.files import File
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import invisibility_of_element_located
from image_uploader_widget_demo.demo_application import models
from utils.tests import IUWTestCase

class InlineEditorTestCase(IUWTestCase):
    @property
    def admin_add_url(self):
        return self.get_url_from_path('/admin/demo_application/inline/add/')

    def get_edit_url(self, id):
        return self.get_url_from_path("/admin/demo_application/inline/%s/change/" % id)
    
    def test_have_empty_marker(self):
        """
        The inline editor should have an empty marker when have no images.
        """
        self.selenium.get(self.admin_add_url)

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        empty = root.find_element(By.CSS_SELECTOR, '.iuw-empty')
        add_button = root.find_element(By.CSS_SELECTOR, '.iuw-add-image-btn')
        
        self.selenium.implicitly_wait(1)

        self.assertFalse(add_button.is_displayed())
        self.assertIsNotNone(empty)
        self.assertTrue(empty.is_displayed())

    def test_click_on_empty_marker(self):
        """
        Click on the empty marker should emit click event on the temporary
        file input for choose file.
        """
        self.selenium.get(self.admin_add_url)

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
        """
        Should add itens to the inline editor when change the temporary file input value
        and click on the form submit button should save the itens to the database.
        """
        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 0)

        self.selenium.get(self.admin_add_url)

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        temp_file = root.find_element(By.CSS_SELECTOR, '.temp_file')

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 0)

        temp_file.send_keys(self.image1)

        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 1)
        
        temp_file.send_keys(self.image2)

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
        """
        Add image to the inline editor and click on remove it before saving the form
        should remove it and should not save it to the database when submit the form.
        """
        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 0)

        self.selenium.get(self.admin_add_url)

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        temp_file = root.find_element(By.CSS_SELECTOR, '.temp_file')

        temp_file.send_keys(self.image1)

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
        """
        Opening the edit page for an item with saved subitens the inline editor
        should be initialized with the data of the saved itens.
        """
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
        """
        when click on the remove button for a saved item, should check the delete checkbox
        for the related item and mark the related ite with deleted class and when submit
        the form should be delete the itens from the database.
        """
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
        """
        when click on the preview image should emit the click event on the
        file input of this preview item.
        """
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
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
        """
        when click on the add image button should emit the click event of the temporary file
        input of the inline editor.
        """
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
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
        self.assertTrue(add_button.is_displayed())
        add_button.click()

        self.assertEqual(self.selenium.switch_to.alert.text, "CLICKED")

    def test_click_on_preview_button(self):
        """
        when click on the preview button of an item, should open the preview modal
        with an img tag with the same src of the preview item.
        """
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 1)

        preview = previews[0]
        preview_img = preview.find_element(By.TAG_NAME, 'img')
        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        preview_button.click()
        
        preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))
        self.assertIsNotNone(preview_modal)
        self.assertEqual(preview_modal.get_attribute('class'), 'iuw-modal visible')

        img = preview_modal.find_element(By.TAG_NAME, 'img')
        self.assertIsNotNone(img)
        self.assertEqual(img.get_attribute("src"), preview_img.get_attribute("src"))

    def test_click_on_preview_button_and_image_on_modal(self):
        """
        when click on the preview button and open the preview modal, click on the image
        should not close the image preview modal.
        """
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 1)

        preview = previews[0]
        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        preview_button.click()
        
        preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))

        img = preview_modal.find_element(By.TAG_NAME, 'img')
        img.click()

        self.selenium.implicitly_wait(0.5)

        self.assertEqual(preview_modal.get_attribute("class"), "iuw-modal visible")

    def test_click_on_preview_button_and_close_on_modal(self):
        """
        when click on the preview button and open the preview modal, click on the close
        modal button should close the image preview modal.
        """
        inline = models.Inline.objects.create()
        
        item1 = models.InlineItem()
        item1.parent = inline
        with open(self.image1, 'rb') as f:
            item1.image.save("image.png", File(f))
        item1.save()
        
        self.selenium.get(self.get_edit_url(inline.id))

        root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
        previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
        self.assertEqual(len(previews), 1)

        preview = previews[0]
        preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
        preview_button.click()
        
        preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))

        close_button = preview_modal.find_element(By.CSS_SELECTOR, '.iuw-modal-close')
        close_button.click()

        WebDriverWait(self.selenium, timeout=3).until(invisibility_of_element_located((By.CSS_SELECTOR, "#iuw-modal-element")));

    def test_change_image_of_saved_item(self):
        """
        Opening the edit page for an item with saved subitens and change
        the image of an subitem should save it.
        """
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
        self.assertEqual(len(previews), 2)

        url1 = item1.image.url

        preview = previews[0]
        preview_img = preview.find_element(By.TAG_NAME, 'img')
        preview_src = preview_img.get_attribute('src')
        
        file_input = preview.find_element(By.CSS_SELECTOR, 'input[type=file]')
        file_input.send_keys(self.image1)

        self.assertNotEqual(preview_src, preview_img.get_attribute('src'))
        
        submit = self.selenium.find_element(By.CSS_SELECTOR, '#inline_form [type="submit"]')
        submit.click()

        item1 = models.InlineItem.objects.filter(pk=item1.pk).first()
        self.assertNotEqual(item1.image.url, url1)
