import os
import time
from django.test import tag
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from tests.mixins.admin import AdminMixin
from tests.mixins.playwright import PlaywrightMixin
from tests.mixins.iuw import IUWMixin
from tests.mixins.snapshot import SnapshotMixin

@tag('playwright')
class TestCase(
    PlaywrightMixin,
    AdminMixin,
    IUWMixin,
    SnapshotMixin,
    StaticLiveServerTestCase,
):
    @property
    def image1(self):
        """gets the file path of the image1."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mocks_dir = os.path.join(base_dir, "utils", "tests", "mocks")
        image = os.path.join(mocks_dir, "image.png")
        return image
    
    @property
    def image2(self):
        """gets the file path of the image2."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mocks_dir = os.path.join(base_dir, "utils", "tests", "mocks")
        image = os.path.join(mocks_dir, "image2.png")
        return image
    
    def wait(self, seconds: float) -> None:
        time.sleep(seconds)
