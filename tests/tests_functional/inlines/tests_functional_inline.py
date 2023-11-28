from django.test import tag
from django.core.files import File
from tests import models, TestCase

@tag('functional', "playwright", 'AAAQ')
class InlineEditorTestCase(TestCase):
    model = "inline"

    def init_item(self):
        inline = models.Inline.objects.create()
        
        self.item1 = models.InlineItem()
        self.item1.parent = inline
        with open(self.image1, 'rb') as f:
            self.item1.image.save("image.png", File(f))
        self.item1.save()
        
        self.item2 = models.InlineItem()
        self.item2.parent = inline
        with open(self.image2, 'rb') as f:
            self.item2.image.save("image2.png", File(f))
        self.item2.save()

        return inline
    
    def goto_change_page(self):
        item = self.init_item()
        super().goto_change_page(item.id)
        return item

    def test_should_have_visible_empty_marker_when_no_images_inline(self):
        """
        Should have a visible empty marker when no images on inline.

        The test flow is:
            - Navigate to Inline Add Page.
            - Assert if add button is hidden.
            - Assert if empty marker is visible.
        """
        self.goto_add_page()

        root = self.find_inline_root()
        empty = self.find_empty_marker(root)
        add_button = self.find_add_button(root)
        self.wait(0.1)

        self.assertIsNotNone(root)
        self.assertFalse(add_button.is_visible())
        self.assertIsNotNone(empty)
        self.assertTrue(empty.is_visible())

    def test_should_fire_click_on_temporary_input_when_click_empty_marker(self):
        """
        Should fire click on the temporary input when click on empty marker.
        
        The test flow is:
            - Navigate to Inline Add Page.
            - Click on the empty marker.
            - Assert if click event is fired on temporary input file.
        """
        self.goto_add_page()

        root = self.find_inline_root()
        empty = self.find_empty_marker(root)
        with self.assert_input_file_clicked('.temp_file'):
            empty.click()

    def test_should_create_preview_when_select_and_upload_when_submit(self):
        """
        Should create a preview when select file and upload it when submit.

        The test flow is:
            - Assert if None item is present on database.
            - Navigate to Inline Add Page.
            - Assert if None preview item is present on page.
            - Select first file.
            - Assert if One preview item is present on page.
            - Select second file.
            - Assert if Two preview items is present on page.
            - Assert image, preview and delete icon on each of preview itens.
            - Submit the form.
            - Assert admin success message.
            - Assert the itens on the database.
        """
        self.assertEqual(len(models.InlineItem.objects.all()), 0)
        self.goto_add_page()

        root = self.find_inline_root()
        temp_file = root.query_selector('.temp_file')

        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 0)

        temp_file.set_input_files(self.image1)
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)

        temp_file.set_input_files(self.image2)
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 2)
        
        for preview in previews:
            img = preview.query_selector('img')
            preview_button = self.find_preview_icon(preview)
            remove_button = self.find_delete_icon(preview)
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

        self.submit_form('#inline_form')
        self.assert_success_message()

        items = models.InlineItem.objects.all()
        self.assertEqual(len(items), 2)
        for item in items:
            self.assertIsNotNone(item.image)

    def test_should_remove_preview_and_not_save_when_not_saved(self):
        """
        Should remove preview and not save item when not saved.

        The test flow is:
            - Go to add page.
            - Assert if One preview item is present on page.
            - Find delete icon.
            - Click on the delete icon
            - Assert if none preview item is present on page.
            - Submit the form.
            - Assert if none item is saved.
        """
        self.assertEqual(len(models.InlineItem.objects.all()), 0)
        self.goto_add_page()

        root = self.find_inline_root()
        temp_file = root.query_selector('.temp_file')
        temp_file.set_input_files(self.image1)

        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 1)
        
        self.find_delete_icon(previews[0]).click()
        self.assertEqual(len(self.find_inline_previews(root)), 0)

        self.submit_form('#inline_form')
        self.assert_success_message()
        self.assertEqual(len(models.InlineItem.objects.all()), 0)

    def test_should_have_intiialized_with_data_when_go_to_edit_page(self):
        """
        Should have initialized with data when go to edit page.

        The test flow is:
            - Go to Edit Page.
            - Assert if two items is present on page.
            - Assert image, preview and remove icon on each item.
        """
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 2)

        for index, preview in enumerate(previews):
            img = preview.query_selector('img')
            preview_button = self.find_preview_icon(preview)
            remove_button = self.find_delete_icon(preview)
            self.assertIsNotNone(img)
            self.assertIsNotNone(preview_button)
            self.assertIsNotNone(remove_button)

            src = img.get_attribute('src')
            if index == 0:
                self.assertTrue(self.item1.image.url in src)
            else:
                self.assertTrue(self.item2.image.url in src)

    def test_should_remove_saved_items_when_edit(self):
        """
        Should remove saved items when editing.

        The test flow is:
            - Go to Edit Page.
            - Assert if two previews is displayed.
            - Click on the Delete Icon of each Preview Item.
            - Assert if none preview is visible.
            - Assert if the hidden preview is present.
            - Assert if the checkboxes are checked.
            - Submit form.
            - Assert success message.
            - Assert if the itens are removed from database.
        """
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 2)

        for preview in previews:
            self.find_delete_icon(preview).click()

        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 0)
        previews = self.find_deleted_inline_previews(root)
        self.assertEqual(len(previews), 2)

        for preview in previews:
            self.assertTrue(preview.query_selector('input[type=checkbox]').is_checked())

        self.submit_form('#inline_form')
        self.assert_success_message()

        self.assertEqual(len(models.InlineItem.objects.all()), 0)

    def test_should_fire_input_click_when_click_on_preview_image(self):
        """
        Should fire input click when click on the preview image.

        The test flow is:
            - Go to change page.
            - Assert if the two previews is present.
            - Click on the first preview image.
            - Assert if the click event is fired.
            - Click on the second preview image.
            - Assert if the click event is fired.
        """
        self.goto_change_page()

        root = self.find_inline_root()
        previews = self.find_inline_previews(root)
        self.assertEqual(len(previews), 2)

        with self.assert_input_file_clicked(".inline-related:not(.empty-form):not(.deleted) input[type=file]", 0):
            preview = previews[0]
            img = preview.query_selector('img')
            img.click()

        with self.assert_input_file_clicked(".inline-related:not(.empty-form):not(.deleted) input[type=file]", 1):
            preview = previews[1]
            img = preview.query_selector('img')
            img.click()

    # def test_click_on_add_image(self):
    #     """
    #     when click on the add image button should emit the click event of the temporary file
    #     input of the inline editor.
    #     """
    #     inline = models.Inline.objects.create()
        
    #     item1 = models.InlineItem()
    #     item1.parent = inline
    #     with open(self.image1, 'rb') as f:
    #         item1.image.save("image.png", File(f))
    #     item1.save()
        
    #     self.selenium.get(self.get_edit_url(inline.id))

    #     root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
    #     previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
    #     self.assertEqual(len(previews), 1)

    #     injected_javascript = (
    #         'const callback = arguments[0];'
    #         'const input = document.querySelector(".temp_file");'
    #         'input.addEventListener("click", (e) => { e.preventDefault(); alert("CLICKED"); });'
    #         'callback();'
    #     )
    #     self.selenium.execute_async_script(injected_javascript)

    #     add_button = root.find_element(By.CSS_SELECTOR, '.iuw-add-image-btn')
    #     self.assertTrue(add_button.is_displayed())
    #     add_button.click()

    #     self.assertEqual(self.selenium.switch_to.alert.text, "CLICKED")
    #     self.selenium.switch_to.alert.accept()

    # def test_click_on_preview_button(self):
    #     """
    #     when click on the preview button of an item, should open the preview modal
    #     with an img tag with the same src of the preview item.
    #     """
    #     inline = models.Inline.objects.create()
        
    #     item1 = models.InlineItem()
    #     item1.parent = inline
    #     with open(self.image1, 'rb') as f:
    #         item1.image.save("image.png", File(f))
    #     item1.save()
        
    #     self.selenium.get(self.get_edit_url(inline.id))

    #     root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
    #     previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
    #     self.assertEqual(len(previews), 1)

    #     preview = previews[0]
    #     preview_img = preview.find_element(By.TAG_NAME, 'img')
    #     preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
    #     preview_button.click()
        
    #     preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))
    #     self.assertIsNotNone(preview_modal)
    #     self.assertEqual(preview_modal.get_attribute('class'), 'iuw-modal visible')

    #     img = preview_modal.find_element(By.TAG_NAME, 'img')
    #     self.assertIsNotNone(img)
    #     self.assertEqual(img.get_attribute("src"), preview_img.get_attribute("src"))

    # def test_click_on_preview_button_and_image_on_modal(self):
    #     """
    #     when click on the preview button and open the preview modal, click on the image
    #     should not close the image preview modal.
    #     """
    #     inline = models.Inline.objects.create()
        
    #     item1 = models.InlineItem()
    #     item1.parent = inline
    #     with open(self.image1, 'rb') as f:
    #         item1.image.save("image.png", File(f))
    #     item1.save()
        
    #     self.selenium.get(self.get_edit_url(inline.id))

    #     root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
    #     previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
    #     self.assertEqual(len(previews), 1)

    #     preview = previews[0]
    #     preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
    #     preview_button.click()
        
    #     preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))

    #     img = preview_modal.find_element(By.TAG_NAME, 'img')
    #     img.click()

    #     self.selenium.implicitly_wait(0.5)

    #     self.assertEqual(preview_modal.get_attribute("class"), "iuw-modal visible")

    # def test_click_on_preview_button_and_close_on_modal(self):
    #     """
    #     when click on the preview button and open the preview modal, click on the close
    #     modal button should close the image preview modal.
    #     """
    #     inline = models.Inline.objects.create()
        
    #     item1 = models.InlineItem()
    #     item1.parent = inline
    #     with open(self.image1, 'rb') as f:
    #         item1.image.save("image.png", File(f))
    #     item1.save()
        
    #     self.selenium.get(self.get_edit_url(inline.id))

    #     root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
    #     previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
    #     self.assertEqual(len(previews), 1)

    #     preview = previews[0]
    #     preview_button = preview.find_element(By.CSS_SELECTOR, '.iuw-preview-icon')
    #     preview_button.click()
        
    #     preview_modal = WebDriverWait(self.selenium, timeout=3).until(lambda d: d.find_element(By.CSS_SELECTOR, "#iuw-modal-element.visible"))

    #     close_button = preview_modal.find_element(By.CSS_SELECTOR, '.iuw-modal-close')
    #     close_button.click()

    #     WebDriverWait(self.selenium, timeout=3).until(invisibility_of_element_located((By.CSS_SELECTOR, "#iuw-modal-element")));

    # def test_change_image_of_saved_item(self):
    #     """
    #     Opening the edit page for an item with saved subitens and change
    #     the image of an subitem should save it.
    #     """
    #     inline = models.Inline.objects.create()
        
    #     item1 = models.InlineItem()
    #     item1.parent = inline
    #     with open(self.image1, 'rb') as f:
    #         item1.image.save("image.png", File(f))
    #     item1.save()
        
    #     item2 = models.InlineItem()
    #     item2.parent = inline
    #     with open(self.image2, 'rb') as f:
    #         item2.image.save("image2.png", File(f))
    #     item2.save()

    #     self.selenium.get(self.get_edit_url(inline.id))

    #     root = self.selenium.find_element(By.CSS_SELECTOR, '.iuw-inline-root')
    #     previews = root.find_elements(By.CSS_SELECTOR, '.inline-related:not(.empty-form):not(.deleted)')
    #     self.assertEqual(len(previews), 2)

    #     url1 = item1.image.url

    #     preview = previews[0]
    #     preview_img = preview.find_element(By.TAG_NAME, 'img')
    #     preview_src = preview_img.get_attribute('src')
        
    #     file_input = preview.find_element(By.CSS_SELECTOR, 'input[type=file]')
    #     file_input.send_keys(self.image1)

    #     self.assertNotEqual(preview_src, preview_img.get_attribute('src'))
        
    #     submit = self.selenium.find_element(By.CSS_SELECTOR, '#inline_form [type="submit"]')
    #     submit.click()

    #     item1 = models.InlineItem.objects.filter(pk=item1.pk).first()
    #     self.assertNotEqual(item1.image.url, url1)
