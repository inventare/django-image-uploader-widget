import os, sys, time
from PIL import Image, ImageChops
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

class SnapshotMixin:
    """
    Provides an mixin to assert match screenshot inside unittest
    TestCase and selenium based testes.
    """

    pixel_threshold_red = 3
    pixel_threshold_green = 3
    pixel_threshold_blue = 3

    def _get_snapshot_filename(self, id: str) -> str:
        """
        Returns the snapshot file name to an unique id.

        :Args:
            - id: an unique id to gets the snapshot file name.
        """
        base_dir = os.path.dirname(__file__)
        snapshots_dir = os.path.join(base_dir, "snapshots")
        return os.path.join(snapshots_dir, "snapshot_%s.png" % id)
    
    def _get_compare_filename(self, id: str) -> str:
        """
        Returns the comparison file name to an unique id.

        :Args:
            - id: an unique id to gets the comparison file name.
        """
        base_dir = os.path.dirname(__file__)
        snapshots_dir = os.path.join(base_dir, "snapshots")
        return os.path.join(snapshots_dir, "compare_%s.png" % id)
    
    def _create_snapshot_image(self, element: WebElement, id: str):
        """
        Takes an screenshot of the element and stores it as snaptshot.

        :Args:
            - element: the element to takes the screenshot.
            - id: an unique id to gets the snapshot file name.
        """
        file = self._get_snapshot_filename(id)
        element.screenshot(file)

    def _create_compare_image(self, element: WebElement, id: str):
        """
        Takes an screenshot of the element and stores it as comparison.

        :Args:
            - element: the element to takes the screenshot.
            - id: an unique id to gets the comparison file name.
        """
        file = self._get_compare_filename(id)
        element.screenshot(file)
    
    def _get_snapshot_image(self, element: WebElement, id: str) -> (Image, bool):
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
    
    def _get_compare_image(self, element: WebElement, id: str) -> Image:
        """
        Gets, or create, the comparison image from the element.

        :Args:
            - element: the element to create the comparison.
            - id: an unique id to gets the comparison file name.
        
        :Returns:
            Returns the comparison image.
        """
        file = self._get_compare_filename(id)
        
        if not os.path.exists(file):
            self._create_compare_image(element, id)

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

    def _fail_match_snapshot(self, element: WebElement, id: str):
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
    
    def wait(self, seconds: float) -> None:
        time.sleep(seconds)

    def hover(self, element: WebElement) -> None:
        ActionChains(self.selenium).move_to_element(element).perform()

    def click(self, element: WebElement) -> None:
        ActionChains(self.selenium).click(element).perform()

    def hover_and_wait(self, element: WebElement, seconds: float) -> None:
        self.hover(element)
        if seconds > 0:
            self.wait(seconds)

    def click_and_wait(self, element: WebElement, seconds: float) -> None:
        self.click(element)
        if seconds > 0:
            self.wait(seconds)

    def assertMatchSnapshot(self, element: WebElement, id: str) -> str:
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
