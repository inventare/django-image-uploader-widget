import os, sys
from PIL import Image, ImageChops
from selenium.webdriver.remote.webelement import WebElement

class SnapshotMixin:
    """
    Provides an mixin to assert match screenshot inside unittest
    TestCase and selenium based testes.
    """

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
        if diff.getbbox():
            fail = True
            
        self._delete_compare_image(id)
        if fail:
            self._fail_match_snapshot(element, id)
