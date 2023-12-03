import os
import uuid
import time
import sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright, expect
from django.test import tag
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class _AssertInputFileClicked:
    def __init__(self, test_case, input_selector=".form-row.field-image input[type=file]", index=0):
        self.test_case = test_case
        self.input_selector = input_selector
        self.index = index

    def __enter__(self):
        injected_javascript = (
            'async () => {'
            '   window.result = false;'
            f'  const inputs = document.querySelectorAll("{self.input_selector}");'
            f'  const input = inputs[{self.index}];'
            '   input.addEventListener("click", (e) => { e.preventDefault(); window.result = true; });'
            '};'
        )
        self.test_case.page.evaluate(injected_javascript)
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        self.test_case.assertEqual(str(self.test_case.page.evaluate_handle('window.result')), 'true')

class _DarkMode:
    def __init__(self, test_case):
        self.test_case = test_case

    def __enter__(self):
        self.test_case.page.emulate_media(color_scheme='dark')
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        self.test_case.page.emulate_media(color_scheme='light')

@tag('playwright')
class IUWTestCase(StaticLiveServerTestCase):
    model = None
    pixel_threshold_red = 5
    pixel_threshold_green = 5
    pixel_threshold_blue = 5

    @property
    def image1(self):
        """Get the file path of the image1."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mocks_dir = os.path.join(base_dir, "mocks")
        image = os.path.join(mocks_dir, "image.png")
        return image
    
    @property
    def image2(self):
        """Get the file path of the image2."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mocks_dir = os.path.join(base_dir, "mocks")
        image = os.path.join(mocks_dir, "image2.png")
        return image

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()
    
    def wait(self, seconds: float) -> None:
        """
        Wait for a time.

        Args:
            - seconds: the time to wait, in seconds.
        """
        time.sleep(seconds)
    
    def goto_add_page(self):
        """
        Navigate the playwright to the add page for the model.
        """
        self.page.goto(f"{self.live_server_url}/admin/tests/{self.model}/add")

    def goto_change_page(self, id: int):
        """
        Navigate the playwright to the change page for the model.

        Args:
            - id: the entity id to change.
        """
        self.page.goto(f"{self.live_server_url}/admin/tests/{self.model}/{id}/change")

    def setUp(self):
        self.page = self.browser.new_page()
        self.login()

    def _create_root_user(self):
        """
        Create an root user to login inside the django-admin.
        """
        User = get_user_model()
        username = str(uuid.uuid4()).replace('-', '')
        email = '%s@example.com' % username
        password = username
        user = User.objects.create_superuser(username, email, password)
        return user, username, password
    
    def login(self):
        """
        Create an root user and login into the django-admin.
        """
        _, username, password = self._create_root_user()

        self.page.goto(f"{self.live_server_url}/admin/login/")
        self.page.wait_for_selector('text=Django administration')
        self.page.fill('[name=username]', username)
        self.page.fill('[name=password]', password)
        self.page.click('text=Log in')

    def submit_form(self, id: str):
        """Submit the form by clicking on an button or input with type=submit."""
        submit = self.page.query_selector(f'{id} [type="submit"]')
        submit.click()

    def assert_success_message(self):
        """Wait and assert for the success message on the django-admin."""
        alert = self.page.wait_for_selector('.messagelist .success', timeout=3000)
        self.assertIsNotNone(alert)

    def assert_input_file_clicked(self, input_selector=".form-row.field-image input[type=file]", index=0):
        return _AssertInputFileClicked(self, input_selector, index)
    
    def dark_theme(self):
        return _DarkMode(self)
    
    def find_widget_form_row(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.form-row.field-image')

    def find_widget_root(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.form-row.field-image .iuw-root')
    
    def find_inline_root(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-inline-root')
    
    def find_widget_preview(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-image-preview')
    
    def find_inline_previews(self, element=None):
        if not element:
            element = self.page
        return element.query_selector_all('.inline-related:not(.empty-form):not(.deleted)')
    
    def find_deleted_inline_previews(self, element=None):
        if not element:
            element = self.page
        return element.query_selector_all('.inline-related:not(.empty-form).deleted')
    
    def find_empty_marker(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-empty')

    def find_preview_icon(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-preview-icon')
    
    def find_delete_icon(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-delete-icon')
    
    def find_add_button(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-add-image-btn')
    
    def find_drop_zone(self, element=None):
        if not element:
            element = self.page
        return element.query_selector('.iuw-drop-label')
    
    def get_preview_modal(self, visible=True, timout=3000, black_overlay=False):
        class_name = ''
        if visible:
            class_name = '.visible'

        preview_modal = self.page.wait_for_selector(f'#iuw-modal-element{class_name}', timeout=timout)

        if black_overlay:
            self.page.evaluate("document.getElementById('iuw-modal-element').style.background = '#000';")

        return preview_modal

    def assert_preview_modal(self, preview_img):
        preview_modal = self.get_preview_modal(True, 3000)
        self.assertIsNotNone(preview_modal)
        self.assertEqual(preview_modal.get_attribute('class'), 'iuw-modal visible')

        img = preview_modal.query_selector('img')
        self.assertIsNotNone(img)
        self.assertEqual(img.get_attribute("src"), preview_img.get_attribute("src"))

    def assert_preview_modal_close(self):
        preview_modal = self.get_preview_modal(True, 0)
        close_button = preview_modal.query_selector('.iuw-modal-close')
        close_button.click()

        locator = self.page.locator('#iuw-modal-element')
        expect(locator).not_to_be_visible(timeout=3000)
    
    def wait_for_empty_marker(self, element=None, timeout=3000):
        if not element:
            element = self.page
        return element.wait_for_selector('.iuw-empty', timeout=timeout)

    def _get_snapshot_filename(self, id: str) -> str:
        """
        Returns the snapshot file name to an unique id.

        :Args:
            - id: an unique id to gets the snapshot file name.
        """
        snapshots_dir = './snapshots'
        return os.path.join(snapshots_dir, "snapshot_%s.png" % id)
    
    def _get_compare_filename(self, id: str) -> str:
        """
        Returns the comparison file name to an unique id.

        :Args:
            - id: an unique id to gets the comparison file name.
        """
        snapshots_dir = './snapshots'
        return os.path.join(snapshots_dir, "compare_%s.png" % id)
    
    def _get_failure_filename(self, id: str) -> str:
        """
        Returns the comparison file name to an unique id.

        :Args:
            - id: an unique id to gets the comparison file name.
        """
        snapshots_dir = './failures'
        return os.path.join(snapshots_dir, "compare_%s.png" % id)
    
    def _create_snapshot_image(self, element, id: str):
        """
        Takes an screenshot of the element and stores it as snaptshot.

        :Args:
            - element: the element to takes the screenshot.
            - id: an unique id to gets the snapshot file name.
        """
        file = self._get_snapshot_filename(id)
        element.screenshot(path=file)

    def _create_compare_image(self, element, id: str):
        """
        Takes an screenshot of the element and stores it as comparison.

        :Args:
            - element: the element to takes the screenshot.
            - id: an unique id to gets the comparison file name.
        """
        file = self._get_compare_filename(id)
        element.screenshot(path=file)
    
    def _get_snapshot_image(self, element, id: str) -> (Image, bool):
        """
        Gets, or create, the snapshot image from the element.

        :Args:
            - element: the element to create the snapshot.
            - id: an unique id to gets the snapshot file name.
        
        :Returns:
            Returns the snapshot image and an boolean indicating
            if the file was created.
        """
        file = self._get_snapshot_filename(id)
        created = False
        
        if not os.path.exists(file):
            self._create_snapshot_image(element, id)
            created = True

        return Image.open(file).convert('RGB'), created
    
    def _get_compare_image(self, element, id: str) -> Image:
        """
        Gets, or create, the comparison image from the element.

        :Args:
            - element: the element to create the comparison.
            - id: an unique id to gets the comparison file name.
        
        :Returns:
            Returns the comparison image.
        """
        self._create_compare_image(element, id)
        file = self._get_compare_filename(id)
        return Image.open(file).convert('RGB')
    
    def _delete_compare_image(self, id: str):
        """
        Delete the comparison image file.

        :Args:
            - id: an unique id to gets the comparison file name.
        """
        file = self._get_compare_filename(id)

        if not os.path.exists(file):
            return
        
        os.remove(file)

    def _delete_snapshot(self, id: str):
        """
        Delete the snapshot image file.
        
        :Args:
            - id: an unique id to gets the snapshot file name.
        """
        file = self._get_snapshot_filename(id)

        if not os.path.exists(file):
            return
        
        os.remove(file)

    def _fail_match_snapshot(self, element, id: str):
        """
        Check if operational system is in an tty, ask for updating the snapshot.
        If user anwser to update the snapshot, it will be updated. Otherwise, 
        it will fail the test.
        """
        if not os.isatty(sys.stdout.fileno()):
            return self.fail("The UI screenshot not matches snapshot")
        
        value = input("The UI screenshot not matches snaptshot. You want to update snapshot? (Y)es, (N)o: ")
        if value != "Y":
            return self.fail("The UI screenshot not matches snapshot")
        
        self._delete_snapshot(id)
        self._create_snapshot_image(element, id)

    def _validate_difference_threshold(self, diff: Image):
        """
        Check pixel-by-pixel if the difference image has more difference
        that the threshold's defined at the class.

        :Args:
            - diff: the difference image, gots from ImageChops.difference(img1, img2)
        """
        data = diff.load()

        for x in range(0, diff.width):
            for y in range(0, diff.height):
                pixel = data[x, y]
                r, g, b = pixel
                if r > self.pixel_threshold_red:
                    print("Difference in RED: %s at X: %s, Y: %s" % (r, x, y))
                    return False
                if g > self.pixel_threshold_green:
                    print("Difference in GREEN: %s at X: %s, Y: %s" % (g, x, y))
                    return False
                if b > self.pixel_threshold_blue:
                    print("Difference in BLUE: %s at X: %s, Y: %s" % (b, x, y))
                    return False

        return True
    
    def assertMatchSnapshot(self, element, id: str) -> str:
        """
        Takes an screenshot and compare with saved, or save at first time, an
        snapshot image. Fail if two screenshots are not equal using Pillow 
        ImageChops.difference.

        :Args:
            - element: the element to take screenshots.
            - id: an unique id to gets and create snapshot and comparison.
        """
        image, created = self._get_snapshot_image(element, id)

        if created:
            return
        
        comparation_image = self._get_compare_image(element, id)

        fail = False
        diff = ImageChops.difference(image, comparation_image)
        if diff.getbbox() and not self._validate_difference_threshold(diff):
            fail = True

        if fail:
            self._fail_match_snapshot(element, id)

        self._delete_compare_image(id)
